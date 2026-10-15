#!/usr/bin/env python3
"""/web <url>: fetch a web page as readable text, PDF, or screenshot (owner only).
Light renderers only (wkhtmltopdf/wkhtmltoimage, WeasyPrint fallback): no JS-heavy sites."""
import asyncio
import ipaddress
import os
import socket
import tempfile
from urllib.parse import urlparse

import requests
from pyrogram.filters import command, regex
from pyrogram.handlers import CallbackQueryHandler, MessageHandler
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from bot import LOGGER, bot
from bot.helper.telegram_helper.filters import CustomFilters

UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/124.0 Safari/537.36"
)
HEADERS = {"User-Agent": UA, "Accept": "text/html,application/xhtml+xml,*/*;q=0.8", "Accept-Language": "he,en;q=0.8"}
MAX_HTML = 15 * 1024 * 1024
SLICE_H = 4000
MAX_SLICES = 6
_lock = asyncio.Lock()  # one render at a time (512MB host)


def _check_url(url):
    p = urlparse(url)
    if p.scheme not in ("http", "https") or not p.hostname:
        raise ValueError("כתובת לא תקינה")
    for info in socket.getaddrinfo(p.hostname, None):
        ip = ipaddress.ip_address(info[4][0])
        if ip.is_private or ip.is_loopback or ip.is_link_local or ip.is_reserved:
            raise ValueError("כתובת פנימית לא מותרת")


def _fetch(url):
    _check_url(url)
    r = requests.get(url, headers=HEADERS, timeout=30, stream=True)
    r.raise_for_status()
    data = b""
    for chunk in r.iter_content(65536):
        data += chunk
        if len(data) > MAX_HTML:
            raise ValueError("הדף גדול מדי")
    enc = r.encoding or r.apparent_encoding or "utf-8"
    return data.decode(enc, errors="replace"), r.url


def _text(url):
    from readability import Document
    from lxml import html as lh

    page, final = _fetch(url)
    doc = Document(page)
    title = doc.short_title()
    body = lh.fromstring(doc.summary()).text_content() if doc.summary() else ""
    lines = [ln.strip() for ln in body.splitlines()]
    out = "\n".join(ln for ln in lines if ln)
    if len(out) < 80:
        out = "\n".join(ln.strip() for ln in lh.fromstring(page).text_content().splitlines() if ln.strip())
    return title, f"{title}\n{final}\n\n{out}".strip()


def _run(cmd, timeout=90):
    import subprocess

    return subprocess.run(cmd, capture_output=True, timeout=timeout)


def _pdf(url, path):
    _check_url(url)
    from shutil import which

    if which("wkhtmltopdf"):
        r = _run(
            ["wkhtmltopdf", "--quiet", "--load-error-handling", "ignore", "--load-media-error-handling", "ignore",
             "--javascript-delay", "1500", "--custom-header", "User-Agent", UA, "--custom-header-propagation", "--page-size", "A4", url, path]
        )
        if os.path.exists(path) and os.path.getsize(path) > 0:
            return
        LOGGER.error(f"wkhtmltopdf: {r.stderr[-300:]!r}")
    page, final = _fetch(url)
    from weasyprint import HTML

    HTML(string=page, base_url=final).write_pdf(path)


def _shot(url, tmp):
    _check_url(url)
    from shutil import which
    from PIL import Image

    Image.MAX_IMAGE_PIXELS = None
    if not which("wkhtmltoimage"):
        raise RuntimeError("wkhtmltoimage לא מותקן")
    full = os.path.join(tmp, "full.jpg")
    _run(
        ["wkhtmltoimage", "--quiet", "--load-error-handling", "ignore", "--load-media-error-handling", "ignore",
         "--javascript-delay", "1500", "--width", "1100", "--quality", "70", "--format", "jpg",
         "--custom-header", "User-Agent", UA, "--custom-header-propagation", url, full]
    )
    if not os.path.exists(full) or os.path.getsize(full) == 0:
        raise RuntimeError("לא הצלחתי לצלם את הדף")
    im = Image.open(full)
    w, h = im.size
    files = []
    for i in range(min(MAX_SLICES, -(-h // SLICE_H))):
        part = im.crop((0, i * SLICE_H, w, min(h, (i + 1) * SLICE_H)))
        p = os.path.join(tmp, f"shot{i + 1}.jpg")
        part.convert("RGB").save(p, quality=75)
        files.append(p)
    return files, h > MAX_SLICES * SLICE_H


ARCHIVE_HOSTS = ["archive.ph", "archive.li", "archive.today"]


def _archive_shot(url, tmp):
    """Full-page screenshot via archive.today. Returns (image_path, permalink) or raises."""
    import re, time

    _check_url(url)
    last = None
    for host in ARCHIVE_HOSTS:
        try:
            s = requests.Session()
            s.headers.update(HEADERS)
            r = s.post(f"https://{host}/submit/", data={"url": url, "anyway": "1"}, timeout=(8, 40), allow_redirects=True)
            snap = r.url
            deadline = time.time() + 120
            while ("/wip/" in snap or "/submit" in snap) and time.time() < deadline:
                time.sleep(6)
                r = s.get(snap, timeout=(8, 30), allow_redirects=True)
                snap = r.url
            if r.status_code != 200 or "/wip/" in snap or "/submit" in snap or "captcha" in r.text.lower()[:5000]:
                raise RuntimeError(f"{host}: not ready ({r.status_code})")
            m = re.search(r'(https?:)?//[^"\']*?/[A-Za-z0-9]+/scr\.png|property="og:image" content="([^"]+)"', r.text)
            img_url = None
            if m:
                img_url = m.group(0) if m.group(0).startswith(("http", "//")) else m.group(2)
                if img_url.startswith("//"):
                    img_url = "https:" + img_url
            else:
                img_url = snap.rstrip("/") + "/scr.png"
            ir = s.get(img_url, timeout=(8, 60))
            if ir.status_code != 200 or not ir.headers.get("content-type", "").startswith("image"):
                raise RuntimeError(f"{host}: no image ({ir.status_code})")
            path = os.path.join(tmp, "archive.png")
            open(path, "wb").write(ir.content)
            return path, snap
        except Exception as e:
            last = e
            LOGGER.error(f"archive {host}: {e}")
    raise RuntimeError(f"archive failed: {last}")


async def web_cmd(_, message):
    args = message.text.split(maxsplit=1)
    url = args[1].strip() if len(args) > 1 else ""
    if not url and message.reply_to_message and message.reply_to_message.text:
        url = message.reply_to_message.text.strip().split()[0]
    if not url.startswith(("http://", "https://")):
        await message.reply_text("שלח: /web קישור-לדף")
        return
    kb = InlineKeyboardMarkup(
        [[
            InlineKeyboardButton("📝 טקסט", callback_data=f"web t {message.id}"),
            InlineKeyboardButton("📄 PDF", callback_data=f"web p {message.id}"),
            InlineKeyboardButton("🖼 צילום מסך", callback_data=f"web s {message.id}"),
        ]]
    )
    await message.reply_text(f"איך להביא את הדף?\n{url}", reply_markup=kb, disable_web_page_preview=True)


async def web_cb(client, query):
    _, mode, mid = query.data.split()
    src = await client.get_messages(query.message.chat.id, int(mid))
    parts = (src.text or "").split(maxsplit=1)
    url = parts[1].strip() if len(parts) > 1 else ""
    if not url and src.reply_to_message and src.reply_to_message.text:
        url = src.reply_to_message.text.strip().split()[0]
    await query.answer("מביא...")
    status = query.message
    await status.edit_text(f"מביא את הדף ({ {'t': 'טקסט', 'p': 'PDF', 's': 'צילום מסך'}[mode] })...\n{url}", disable_web_page_preview=True)
    chat = query.message.chat.id
    loop = asyncio.get_running_loop()
    async with _lock:
        try:
            with tempfile.TemporaryDirectory() as tmp:
                if mode == "t":
                    title, text = await loop.run_in_executor(None, _text, url)
                    p = os.path.join(tmp, "page.txt")
                    open(p, "w", encoding="utf-8").write(text)
                    await client.send_document(chat, p, caption=(title or url)[:200])
                elif mode == "p":
                    p = os.path.join(tmp, "page.pdf")
                    await loop.run_in_executor(None, _pdf, url, p)
                    await client.send_document(chat, p, caption=url[:200])
                else:
                    try:
                        img, link = await loop.run_in_executor(None, _archive_shot, url, tmp)
                        await client.send_document(chat, img, caption=link[:200])
                        await status.delete()
                        return
                    except Exception as e:
                        LOGGER.error(f"archive failed, local fallback: {e}")
                        await status.edit_text("archive.today לא זמין, מצלם מקומית...")
                    files, cut = await loop.run_in_executor(None, _shot, url, tmp)
                    for i, f in enumerate(files, 1):
                        await client.send_document(chat, f, caption=f"{i}/{len(files)}" + (" (נחתך)" if cut and i == len(files) else ""))
            await status.delete()
        except Exception as e:
            LOGGER.error(f"web {mode} {url}: {e}")
            await status.edit_text(f"לא הצלחתי להביא את הדף: {str(e)[:200]}")


bot.add_handler(MessageHandler(web_cmd, filters=command("web") & CustomFilters.authorized))
bot.add_handler(CallbackQueryHandler(web_cb, filters=regex(r"^web [tps] \d+$") & CustomFilters.owner))
