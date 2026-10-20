#!/usr/bin/env python3
# Yemot (ימות המשיח) management for @linked123_bot. Owner-only, Hebrew UI.
# Destructive/outbound actions require in-chat confirmation (buttons).
from os import environ
from time import time
from datetime import datetime
from zoneinfo import ZoneInfo
from uuid import uuid4
from io import BytesIO
from html import escape

from aiohttp import ClientSession, ClientTimeout, FormData
from pyrogram.handlers import MessageHandler, CallbackQueryHandler
from pyrogram.filters import command, regex
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from bot import bot, OWNER_ID, LOGGER
from bot.helper.telegram_helper.filters import CustomFilters
from bot.helper.telegram_helper.bot_commands import BotCommands
from bot.helper.telegram_helper.message_utils import sendMessage, editMessage

YM_SYSTEM = environ.get("YM_SYSTEM", "")
YM_PASS = environ.get("YM_PASS", "")
YM_TOKEN = f"{YM_SYSTEM}:{YM_PASS}"
YM_API = "https://www.call2all.co.il/ym/api"
YM_BRIDGE = environ.get("YM_BRIDGE", "https://yemot-ai-voice-54ab.onbelmo.uk").rstrip("/")

_TIMEOUT = ClientTimeout(total=30)
_PENDING = {}  # token -> (created_at, description, func, args)
PENDING_TTL = 300


def _ready():
    return bool(YM_SYSTEM and YM_PASS)


def _ymp(p):
    p = (p or "").strip()
    return p if p.startswith("ivr2:") else "ivr2:" + (p if p.startswith("/") else "/" + p)


async def _ym_json(action, **params):
    params["token"] = YM_TOKEN
    async with ClientSession(timeout=_TIMEOUT) as s:
        async with s.get(f"{YM_API}/{action}", params=params) as r:
            try:
                j = await r.json(content_type=None)
            except Exception:
                txt = await r.text()
                return {"_raw": txt[:3000]}
            return j if isinstance(j, dict) else {"_data": j}


async def _ym_download(path):
    async with ClientSession(timeout=ClientTimeout(total=60)) as s:
        async with s.get(f"{YM_API}/DownloadFile", params={"token": YM_TOKEN, "path": _ymp(path)}) as r:
            data = await r.read()
            ct = r.headers.get("content-type", "")
            if "json" in ct:
                try:
                    j = await r.json(content_type=None)
                    raise RuntimeError(str(j)[:200])
                except RuntimeError:
                    raise
                except Exception:
                    pass
            return data


async def _ym_upload(data_bytes, filename, ym_path):
    form = FormData()
    form.add_field("token", YM_TOKEN)
    form.add_field("path", _ymp(ym_path))
    form.add_field("file", data_bytes, filename=filename)
    async with ClientSession(timeout=ClientTimeout(total=120)) as s:
        async with s.post(f"{YM_API}/UploadFile", data=form) as r:
            try:
                return await r.json(content_type=None)
            except Exception:
                return {"_raw": (await r.text())[:500]}


def _ok(j):
    if not isinstance(j, dict):
        return True
    if j.get("responseStatus") not in (None, "OK"):
        return False
    if j.get("success") is False:
        return False
    return True


def _err(j):
    if isinstance(j, dict):
        return str(j.get("message") or j.get("responseStatus") or j.get("_raw") or j)[:200]
    return str(j)[:200]


def _fmt_size(n):
    try:
        n = int(n)
    except Exception:
        return ""
    for u in ["B", "KB", "MB", "GB"]:
        if n < 1024 or u == "GB":
            return f"{n:.0f}{u}" if u == "B" else f"{n:.1f}{u}"
        n /= 1024
    return ""


def _pretty(j, cap=3400):
    from json import dumps
    try:
        t = dumps(j, ensure_ascii=False, indent=1)
    except Exception:
        t = str(j)
    if len(t) > cap:
        t = t[:cap] + "\n... (קוצר)"
    return f"<blockquote expandable><pre>{escape(t)}</pre></blockquote>"


def _confirm_kb(tok):
    return InlineKeyboardMarkup([[
        InlineKeyboardButton("✅ אשר", callback_data=f"ymcf|{tok}|y"),
        InlineKeyboardButton("❌ בטל", callback_data=f"ymcf|{tok}|n"),
    ]])


def _new_pending(desc, func, *args):
    for k in [k for k, v in _PENDING.items() if time() - v[0] > PENDING_TTL]:
        _PENDING.pop(k, None)
    tok = uuid4().hex[:8]
    _PENDING[tok] = (time(), desc, func, args)
    return tok


def _menu_kb():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📊 סטטוס הקו", callback_data="ymenu|stat"),
         InlineKeyboardButton("📞 שיחות פעילות", callback_data="ymenu|calls")],
        [InlineKeyboardButton("📁 קבצים", callback_data="ymenu|files"),
         InlineKeyboardButton("🗂 שלוחות", callback_data="ymenu|ext")],
        [InlineKeyboardButton("📢 קמפיינים", callback_data="ymenu|camp"),
         InlineKeyboardButton("❓ פקודות", callback_data="ymenu|cmds")],
    ])


MENU_TXT = (
    "🎛 <b>ניהול ימות המשיח</b>\n\n"
    "בחר פעולה או שלח פקודה ישירה (רשימה מלאה בכפתור ❓).\n"
    "מחיקות ושינויים מבקשים אישור לפני ביצוע."
)

CMDS_TXT = (
    "<b>פקודות ימות:</b>\n<blockquote>"
    "/ymstat - סטטוס הקו והשרת\n"
    "/ymcalls - שיחות פעילות עכשיו\n"
    "/ymfiles [נתיב] - רשימת קבצים (ברירת מחדל: /)\n"
    "/ymtxt &lt;נתיב&gt; - הצגת קובץ טקסט/הגדרות\n"
    "/ymdl &lt;נתיב&gt; - הורדת קובץ לטלגרם\n"
    "/ymup &lt;נתיב יעד&gt; - בתגובה לקובץ: העלאה לקו\n"
    "/ymwrite &lt;נתיב&gt; &lt;טקסט&gt; - כתיבת קובץ טקסט\n"
    "/ymdel &lt;נתיב&gt; - מחיקת קובץ (עם אישור)\n"
    "/ymext - הגדרות השלוחות\n"
    "/ymset &lt;נתיב שלוחה&gt; מפתח=ערך ... - שינוי שלוחה (עם אישור)\n"
    "/ymsms &lt;טלפון&gt; &lt;הודעה&gt; - שליחת SMS (עם אישור)\n"
    "/ymtz &lt;טלפון&gt; - צינתוק (עם אישור)\n"
    "/ymcamp - קמפיינים ותבניות</blockquote>"
    "נתיבים: בלי קידומת (למשל /AI/in) או עם ivr2: - שניהם עובדים."
)


_STAT_LABELS = {
    "calls": "סה״כ שיחות שטופלו",
    "errors": "שגיאות",
    "turns": "תורות שיחה (שאלה ותשובה)",
    "started": "השרת רץ מאז",
}


def _fmt_started(v):
    try:
        return datetime.fromtimestamp(float(v), ZoneInfo("Asia/Jerusalem")).strftime("%d.%m.%Y %H:%M")
    except Exception:
        return str(v)


async def _do_stat():
    out = ["📊 <b>סטטוס הקו</b>"]
    try:
        async with ClientSession(timeout=ClientTimeout(total=15)) as s:
            async with s.get(f"{YM_BRIDGE}/status") as r:
                b = await r.json(content_type=None)
        st = b.get("stats") or {}
        out.append(f"🟢 השרת פעיל · שיחות פעילות לפי הגשר: <b>{b.get('active_calls', 0)}</b>")
        parts = []
        for k, v in st.items():
            label = _STAT_LABELS.get(k, str(k))
            val = _fmt_started(v) if k == "started" else str(v)
            parts.append(f"{escape(label)}: <code>{escape(val)}</code>")
        if parts:
            out.append("<blockquote>" + "\n".join(parts) + "</blockquote>")
        out.append("<i>שיחות פעילות בפועל בקו עצמו: /ymcalls</i>")
    except Exception as e:
        out.append(f"🔴 השרת לא עונה: {escape(str(e)[:150])}")
    return "\n".join(out)


async def _do_calls():
    j = await _ym_json("GetIncomingCalls")
    if not _ok(j):
        return f"⚠️ שגיאה מימות: {escape(_err(j))}"
    calls = j.get("calls") or j.get("data") or j.get("_data") or []
    if isinstance(calls, list) and not calls:
        return "📞 אין שיחות פעילות כרגע."
    return "📞 <b>שיחות פעילות:</b>\n" + _pretty(j)


async def _do_files(path):
    path = (path or "/").strip() or "/"
    j = await _ym_json("GetIVR2Dir", path=_ymp(path))
    if not _ok(j):
        return f"⚠️ שגיאה מימות: {escape(_err(j))}"
    dirs = j.get("dirs") or []
    files = j.get("files") or []
    lines = [f"📁 <b>{escape(path)}</b>"]
    for d in dirs[:40]:
        nm = d.get("name") if isinstance(d, dict) else str(d)
        lines.append(f"├ 📂 {escape(str(nm))}")
    for f in files[:60]:
        if not isinstance(f, dict):
            lines.append(f"├ 📄 {escape(str(f))}")
            continue
        nm = f.get("name", "?")
        sz = _fmt_size(f.get("size") or f.get("bytes") or f.get("fileSize") or "")
        lines.append(f"├ 📄 {escape(str(nm))}" + (f" <code>{sz}</code>" if sz else ""))
    extra = len(dirs) + len(files)
    lines.append(f"<i>סה״כ {extra} פריטים</i>" + (" (מוצגים חלק)" if extra > 100 else ""))
    if extra == 0:
        lines.append("<i>ריק</i>")
    return "\n".join(lines)[:3900]


async def _do_ext():
    j = await _ym_json("GetIIVRSettings")
    if not _ok(j):
        return f"⚠️ שגיאה מימות: {escape(_err(j))}"
    return "🗂 <b>שלוחות המערכת:</b>\n" + _pretty(j)


async def _do_camp():
    j = await _ym_json("GetTemplates")
    if not _ok(j):
        return f"⚠️ שגיאה מימות: {escape(_err(j))}"
    return "📢 <b>תבניות קמפיין:</b>\n" + _pretty(j) + "\n\n<i>הפעלת קמפיין תתווסף בעתיד — דרושה בדיקת פרמטרים נוספת.</i>"


async def ym_menu(client, message):
    if not _ready():
        await sendMessage(message, "⚠️ חסרים פרטי חיבור לימות בשרת (YM_SYSTEM/YM_PASS).")
        return
    await sendMessage(message, MENU_TXT, _menu_kb())


async def ym_menu_cb(client, query):
    if query.from_user.id != OWNER_ID:
        await query.answer("רק הבעלים.", show_alert=True)
        return
    key = query.data.split("|", 1)[1] if "|" in query.data else ""
    try:
        if key == "stat":
            await editMessage(query.message, await _do_stat(), _menu_kb())
        elif key == "calls":
            await editMessage(query.message, await _do_calls(), _menu_kb())
        elif key == "files":
            await editMessage(query.message, await _do_files("/"), _menu_kb())
        elif key == "ext":
            await editMessage(query.message, await _do_ext(), _menu_kb())
        elif key == "camp":
            await editMessage(query.message, await _do_camp(), _menu_kb())
        elif key == "cmds":
            await editMessage(query.message, CMDS_TXT, _menu_kb())
        else:
            await query.answer()
            return
    except Exception as e:
        LOGGER.error(f"yemot menu cb: {e}")
        await editMessage(query.message, f"⚠️ שגיאה: {escape(str(e)[:200])}", _menu_kb())
    await query.answer()


async def ym_stat(client, message):
    m = await sendMessage(message, "⏳ בודק...")
    await editMessage(m, await _do_stat())


async def ym_calls(client, message):
    m = await sendMessage(message, "⏳ בודק...")
    await editMessage(m, await _do_calls())


async def ym_files(client, message):
    path = message.command[1] if len(message.command) > 1 else "/"
    m = await sendMessage(message, "⏳ טוען רשימה...")
    await editMessage(m, await _do_files(path))


async def ym_txt(client, message):
    if len(message.command) < 2:
        await sendMessage(message, "שימוש: /ymtxt <נתיב>")
        return
    path = message.command[1]
    m = await sendMessage(message, "⏳ קורא...")
    try:
        data = await _ym_download(path)
        txt = data.decode("utf-8", errors="replace")
        if len(txt) > 3500:
            txt = txt[:3500] + "\n... (קוצר)"
        await editMessage(m, f"📄 <b>{escape(path)}</b>\n<blockquote expandable><pre>{escape(txt)}</pre></blockquote>")
    except Exception as e:
        await editMessage(m, f"⚠️ שגיאה: {escape(str(e)[:200])}")


async def ym_dl(client, message):
    if len(message.command) < 2:
        await sendMessage(message, "שימוש: /ymdl <נתיב>")
        return
    path = message.command[1]
    m = await sendMessage(message, "⏳ מוריד מהקו...")
    try:
        data = await _ym_download(path)
        if len(data) > 45 * 1024 * 1024:
            await editMessage(m, "⚠️ הקובץ גדול מדי לשליחה בטלגרם (מעל 45MB).")
            return
        name = path.rstrip("/").rsplit("/", 1)[-1] or "file"
        bio = BytesIO(data)
        bio.name = name
        if name.lower().endswith((".wav", ".mp3", ".m4a", ".ogg")):
            await message.reply_audio(bio, file_name=name, caption=f"📥 {name}")
        else:
            await message.reply_document(bio, file_name=name, caption=f"📥 {name}")
        await m.delete()
    except Exception as e:
        await editMessage(m, f"⚠️ שגיאה: {escape(str(e)[:200])}")


async def _path_exists(path):
    parent = path.rstrip("/").rsplit("/", 1)[0] or "/"
    name = path.rstrip("/").rsplit("/", 1)[-1]
    j = await _ym_json("GetIVR2Dir", path=_ymp(parent))
    files = j.get("files") or []
    return any(isinstance(f, dict) and f.get("name") == name for f in files)


async def _exec_upload(client, message, data_bytes, filename, target):
    j = await _ym_upload(data_bytes, filename, target)
    if _ok(j):
        await editMessage(message, f"✅ הועלה ל־<code>{escape(target)}</code>")
    else:
        await editMessage(message, f"⚠️ ההעלאה נדחתה: {escape(_err(j))}")


async def ym_up(client, message):
    reply = message.reply_to_message
    doc = reply and (reply.document or reply.audio or reply.voice or reply.video)
    if not doc:
        await sendMessage(message, "שלח /ymup <נתיב יעד> בתגובה לקובץ. לדוגמה: /ymup /bot-up/song.wav")
        return
    fname = getattr(doc, "file_name", None) or "file.bin"
    target = message.command[1] if len(message.command) > 1 else f"/bot-up/{fname}"
    if target.endswith("/"):
        target += fname
    size = getattr(doc, "file_size", 0) or 0
    if size > 19 * 1024 * 1024:
        await sendMessage(message, "⚠️ הקובץ גדול מדי להורדה מהטלגרם (מעל 19MB).")
        return
    m = await sendMessage(message, "⏳ מוריד מהטלגרם...")
    try:
        buf = await reply.download(in_memory=True)
        data_bytes = bytes(buf.getbuffer()) if hasattr(buf, "getbuffer") else bytes(buf)
    except Exception as e:
        await editMessage(m, f"⚠️ ההורדה מהטלגרם נכשלה: {escape(str(e)[:200])}")
        return
    try:
        exists = await _path_exists(target)
    except Exception:
        exists = False
    if exists:
        tok = _new_pending(f"דריסת {target}", _exec_upload, m, data_bytes, fname, target)
        await editMessage(m, f"⚠️ הקובץ <code>{escape(target)}</code> כבר קיים בקו.\nלדרוס?", _confirm_kb(tok))
    else:
        await editMessage(m, "⏳ מעלה לקו...")
        await _exec_upload(client, m, data_bytes, fname, target)


async def _exec_write(client, message, path, text):
    j = await _ym_json("UploadTextFile", path=_ymp(path), contents=text)
    if _ok(j):
        await editMessage(message, f"✅ נכתב <code>{escape(path)}</code>")
    else:
        await editMessage(message, f"⚠️ הכתיבה נדחתה: {escape(_err(j))}")


async def ym_write(client, message):
    if len(message.command) < 3:
        await sendMessage(message, "שימוש: /ymwrite <נתיב> <טקסט>")
        return
    path = message.command[1]
    text = message.text.split(None, 2)[2]
    try:
        exists = await _path_exists(path)
    except Exception:
        exists = False
    if exists:
        m = await sendMessage(message, "…")
        tok = _new_pending(f"דריסת {path}", _exec_write, m, path, text)
        await editMessage(m, f"⚠️ הקובץ <code>{escape(path)}</code> כבר קיים.\nלדרוס?", _confirm_kb(tok))
    else:
        m = await sendMessage(message, "⏳ כותב...")
        await _exec_write(client, m, path, text)


async def _exec_delete(client, message, path):
    j = await _ym_json("FileAction", action="delete", path=_ymp(path))
    if _ok(j) and (j.get("success") is not False):
        await editMessage(message, f"🗑 נמחק <code>{escape(path)}</code>")
    else:
        await editMessage(message, f"⚠️ המחיקה נדחתה: {escape(_err(j))}")


async def ym_del(client, message):
    if len(message.command) < 2:
        await sendMessage(message, "שימוש: /ymdel <נתיב>")
        return
    path = message.command[1]
    tok = _new_pending(f"מחיקת {path}", _exec_delete, None, path)
    await sendMessage(message, f"🗑 <b>למחוק מהקו?</b>\n<code>{escape(path)}</code>\nהפעולה בלתי הפיכה.", _confirm_kb(tok))


async def _exec_setext(client, message, path, params):
    j = await _ym_json("UpdateExtension", path=_ymp(path), **params)
    if _ok(j):
        await editMessage(message, f"✅ השלוחה <code>{escape(path)}</code> עודכנה.")
    else:
        await editMessage(message, f"⚠️ העדכון נדחה: {escape(_err(j))}")


async def ym_set(client, message):
    if len(message.command) < 3:
        await sendMessage(message, "שימוש: /ymset <נתיב שלוחה> מפתח=ערך ...\nלדוגמה: /ymset /5 type=playfile playfile=/000.wav")
        return
    path = message.command[1]
    params = {}
    for kv in message.command[2:]:
        if "=" in kv:
            k, v = kv.split("=", 1)
            params[k] = v
    if not params:
        await sendMessage(message, "לא נמצאו זוגות מפתח=ערך.")
        return
    body = "\n".join(f"{escape(k)} = {escape(v)}" for k, v in params.items())
    tok = _new_pending(f"שינוי שלוחה {path}", _exec_setext, None, path, params)
    await sendMessage(message, f"🗂 <b>לשנות את השלוחה <code>{escape(path)}</code>?</b>\n<blockquote>{body}</blockquote>", _confirm_kb(tok))


async def _exec_sms(client, message, phone, text):
    j = await _ym_json("SendSms", phones=phone, message=text)
    if _ok(j):
        await editMessage(message, f"✅ SMS נשלח ל־<code>{escape(phone)}</code>")
    else:
        await editMessage(message, f"⚠️ השליחה נדחתה: {escape(_err(j))}")


async def ym_sms(client, message):
    if len(message.command) < 3:
        await sendMessage(message, "שימוש: /ymsms <טלפון> <הודעה>")
        return
    phone = message.command[1]
    text = message.text.split(None, 2)[2]
    tok = _new_pending(f"SMS ל־{phone}", _exec_sms, None, phone, text)
    await sendMessage(message, f"✉️ <b>לשלוח SMS?</b>\nאל: <code>{escape(phone)}</code>\n<blockquote>{escape(text)}</blockquote>", _confirm_kb(tok))


async def _exec_tz(client, message, phone):
    j = await _ym_json("RunTzintuk", phones=phone)
    if _ok(j):
        await editMessage(message, f"✅ צינתוק יצא ל־<code>{escape(phone)}</code>")
    else:
        await editMessage(message, f"⚠️ נדחה: {escape(_err(j))}")


async def ym_tz(client, message):
    if len(message.command) < 2:
        await sendMessage(message, "שימוש: /ymtz <טלפון>")
        return
    phone = message.command[1]
    tok = _new_pending(f"צינתוק ל־{phone}", _exec_tz, None, phone)
    await sendMessage(message, f"🔔 <b>לשלוח צינתוק (שיחה מתנתקת) ל־<code>{escape(phone)}</code>?</b>", _confirm_kb(tok))


async def ym_ext(client, message):
    m = await sendMessage(message, "⏳ טוען שלוחות...")
    await editMessage(m, await _do_ext())


async def ym_camp(client, message):
    m = await sendMessage(message, "⏳ טוען קמפיינים...")
    await editMessage(m, await _do_camp())


async def ym_confirm_cb(client, query):
    if query.from_user.id != OWNER_ID:
        await query.answer("רק הבעלים יכול לאשר.", show_alert=True)
        return
    try:
        _, tok, ans = query.data.split("|", 2)
    except ValueError:
        await query.answer()
        return
    entry = _PENDING.pop(tok, None)
    if not entry:
        await query.answer("פג תוקף הבקשה — שלח שוב.", show_alert=True)
        return
    _, desc, func, args = entry
    if ans == "n":
        await editMessage(query.message, f"❌ בוטל: {escape(desc)}")
        await query.answer()
        return
    await editMessage(query.message, f"⏳ מבצע: {escape(desc)}...")
    await query.answer()
    try:
        target_msg = args[0] if args and args[0] is not None else query.message
        rest = args[1:] if args else ()
        await func(client, target_msg, *rest)
    except Exception as e:
        LOGGER.error(f"yemot confirm exec: {e}")
        await editMessage(query.message, f"⚠️ שגיאה בביצוע: {escape(str(e)[:200])}")


_H = [
    (BotCommands.YemotCommand, ym_menu),
    (BotCommands.YmStatCommand, ym_stat),
    (BotCommands.YmCallsCommand, ym_calls),
    (BotCommands.YmFilesCommand, ym_files),
    (BotCommands.YmTxtCommand, ym_txt),
    (BotCommands.YmDlCommand, ym_dl),
    (BotCommands.YmUpCommand, ym_up),
    (BotCommands.YmWriteCommand, ym_write),
    (BotCommands.YmDelCommand, ym_del),
    (BotCommands.YmExtCommand, ym_ext),
    (BotCommands.YmSetCommand, ym_set),
    (BotCommands.YmSmsCommand, ym_sms),
    (BotCommands.YmTzCommand, ym_tz),
    (BotCommands.YmCampCommand, ym_camp),
]
for _cmd, _fn in _H:
    bot.add_handler(MessageHandler(_fn, filters=command(_cmd) & CustomFilters.owner))
bot.add_handler(CallbackQueryHandler(ym_menu_cb, filters=regex(r"^ymenu\|")))
bot.add_handler(CallbackQueryHandler(ym_confirm_cb, filters=regex(r"^ymcf\|")))
