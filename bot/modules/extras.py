#!/usr/bin/env python3
# Extras batch 1 for @linked123_bot: Hebrew calendar & learning, small
# utilities, reminders/tasks/notes and RSS. Owner-only, Hebrew UI, additive.
# State persists via drive_state (Drive JSON in the bot's own upload folder);
# without Drive the features work memory-only until the next restart.
# Reminders and RSS are best-effort while the free host restarts hourly:
# overdue reminders fire on boot with an explicit late note.
from re import fullmatch, sub as re_sub
from time import time
from uuid import uuid4
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from html import escape
from asyncio import to_thread

from aiohttp import ClientSession, ClientTimeout
from pyrogram.handlers import MessageHandler, CallbackQueryHandler
from pyrogram.filters import command, regex
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from bot import bot, OWNER_ID, LOGGER, scheduler
from bot.helper.telegram_helper.filters import CustomFilters
from bot.helper.telegram_helper.bot_commands import BotCommands
from bot.helper.telegram_helper.message_utils import sendMessage, editMessage
from bot.helper import drive_state

TZ = ZoneInfo("Asia/Jerusalem")
_HTTP = ClientTimeout(total=30)
RSS_INTERVAL = 3600          # hourly, no rapid polling
REM_INTERVAL = 30
MAX_FEEDS = 20

_PENDING = {}
PENDING_TTL = 300

_WEEKDAYS = ["שני", "שלישי", "רביעי", "חמישי", "שישי", "שבת", "ראשון"]

_CITIES = {
    "ירושלים": 281184, "תל אביב": 293397, "חיפה": 294801, "באר שבע": 295530,
    "בני ברק": 295514, "נתניה": 294071, "אשדוד": 295629, "אשקלון": 295620,
    "ראשון לציון": 293703, "פתח תקווה": 293918, "חולון": 294751,
    "רמת גן": 293788, "רחובות": 293807, "בית שמש": 295432, "כפר סבא": 294622,
    "הרצליה": 294778, "חדרה": 294946, "מודיעין": 282926, "צפת": 293100,
    "טבריה": 293322, "נצרת": 294098, "עכו": 295721, "אילת": 295277,
}
_DEFAULT_CITY = 281184  # ירושלים

_WMO = {
    0: "בהיר", 1: "בעיקר בהיר", 2: "מעונן חלקית", 3: "מעונן",
    45: "ערפל", 47: "ערפל", 51: "טפטוף קל", 53: "טפטוף", 55: "טפטוף כבד",
    56: "טפטוף קפוא", 57: "טפטוף קפוא", 61: "גשם קל", 63: "גשם", 65: "גשם כבד",
    66: "גשם קפוא", 67: "גשם קפוא", 71: "שלג קל", 73: "שלג", 75: "שלג כבד",
    77: "גבישי שלג", 80: "ממטרים קלים", 81: "ממטרים", 82: "ממטרים כבדים",
    85: "ממטרי שלג", 86: "ממטרי שלג", 95: "סופת רעמים",
    96: "סופת רעמים עם ברד", 99: "סופת רעמים עם ברד",
}


async def _json(url, params=None, timeout=_HTTP):
    async with ClientSession(timeout=timeout) as s:
        async with s.get(url, params=params) as r:
            return await r.json(content_type=None)


async def _notify(text):
    try:
        await bot.send_message(OWNER_ID, text, disable_web_page_preview=True)
    except Exception as e:
        LOGGER.error(f"extras: notify failed: {e}")


# ---------- confirmations (same pattern as yemot) ----------

def _confirm_kb(tok):
    return InlineKeyboardMarkup([[
        InlineKeyboardButton("✅ אשר", callback_data=f"xcf|{tok}|y"),
        InlineKeyboardButton("❌ בטל", callback_data=f"xcf|{tok}|n"),
    ]])


def _new_pending(desc, func, *args):
    for k in [k for k, v in _PENDING.items() if time() - v[0] > PENDING_TTL]:
        _PENDING.pop(k, None)
    tok = uuid4().hex[:8]
    _PENDING[tok] = (time(), desc, func, args)
    return tok


async def extras_confirm_cb(client, query):
    data = query.data.split("|")
    if len(data) != 3:
        return await query.answer()
    tok, ans = data[1], data[2]
    if query.from_user.id != OWNER_ID:
        return await query.answer("רק הבעלים!", show_alert=True)
    pend = _PENDING.pop(tok, None)
    if not pend:
        return await query.answer("פג התוקף או שכבר בוצע", show_alert=True)
    if ans == "n":
        await query.answer("בוטל")
        return await editMessage(query.message, "❎ בוטל.")
    _, desc, func, args = pend
    await query.answer()
    try:
        await func(*args)
        await editMessage(query.message, f"✅ {desc} - בוצע.")
    except Exception as e:
        LOGGER.error(f"extras confirm: {e}")
        await editMessage(query.message, f"⚠️ {desc} - נכשל: {escape(str(e)[:150])}")


# ---------- Hebrew calendar & learning ----------

async def hebdate_cmd(client, message):
    args = message.command[1:]
    now = datetime.now(TZ)
    gy, gm, gd = now.year, now.month, now.day
    if args:
        m = fullmatch(r"(\d{1,2})[/\-.](\d{1,2})[/\-.](\d{4})", args[0])
        m2 = fullmatch(r"(\d{4})-(\d{1,2})-(\d{1,2})", args[0])
        if m:
            gd, gm, gy = int(m[1]), int(m[2]), int(m[3])
        elif m2:
            gy, gm, gd = int(m2[1]), int(m2[2]), int(m2[3])
        else:
            return await sendMessage(message, "פורמט: /hebdate או /hebdate 30/10/2026")
    try:
        j = await _json("https://www.hebcal.com/converter",
                        {"cfg": "json", "gy": gy, "gm": gm, "gd": gd, "g2h": 1, "lg": "h"})
    except Exception as e:
        return await sendMessage(message, f"⚠️ שגיאה בחיבור ל-Hebcal: {escape(str(e)[:120])}")
    heb = j.get("hebrew") or "?"
    d = datetime(gy, gm, gd)
    wd = _WEEKDAYS[d.weekday()]
    out = [f"📅 <b>{escape(heb)}</b>",
           f"{d.day}/{d.month}/{d.year}, יום {wd}"]
    events = [e for e in (j.get("events") or []) if isinstance(e, str)]
    if events:
        out.append("🎉 " + ", ".join(escape(e) for e in events))
    await sendMessage(message, "\n".join(out))


async def shabbat_cmd(client, message):
    args = message.command[1:]
    geo = None
    if args:
        name = " ".join(args).strip()
        geo = _CITIES.get(name)
        if geo is None:
            cities = ", ".join(sorted(_CITIES))
            return await sendMessage(
                message,
                f"לא מכיר את \"{escape(name)}\". ערים זמינות:\n<blockquote>{escape(cities)}</blockquote>")
        await drive_state.put("shabbat_city", geo)
    else:
        geo = await drive_state.get("shabbat_city", _DEFAULT_CITY)
    city_name = next((k for k, v in _CITIES.items() if v == geo), "ירושלים")
    try:
        j = await _json("https://www.hebcal.com/shabbat",
                        {"cfg": "json", "geonameid": geo, "M": "on", "lg": "h", "b": 18})
    except Exception as e:
        return await sendMessage(message, f"⚠️ שגיאה בחיבור ל-Hebcal: {escape(str(e)[:120])}")
    parasha, candles, havdalah = None, None, None
    for it in j.get("items") or []:
        cat = it.get("category")
        if cat == "parashat":
            parasha = it.get("hebrew") or it.get("title")
        elif cat == "candles":
            candles = it.get("title")
        elif cat == "havdalah":
            havdalah = it.get("title")
    out = [f"🕯 <b>שבת ב{escape(city_name)}</b>"]
    if parasha:
        out.append(f"📜 {escape(parasha)}")
    if candles:
        out.append(f"🕯 {escape(candles)}")
    if havdalah:
        out.append(f"✨ {escape(havdalah)}")
    if len(out) == 1:
        out.append("לא נמצאו נתוני שבת לשבוע הקרוב.")
    out.append("<i>מקור: Hebcal. לשינוי עיר: /shabbat ושם העיר (נשמר כברירת מחדל).</i>")
    await sendMessage(message, "\n".join(out))


def _strip_html(t):
    t = re_sub(r"<[^>]+>", "", t)
    return re_sub(r"\s+", " ", t).strip()


async def sefaria_cmd(client, message):
    args = message.command[1:]
    if not args:
        return await sendMessage(
            message,
            "פורמט: /sefaria <מראה מקום>\n"
            "דוגמאות: <code>/sefaria בראשית א א</code>, <code>/sefaria Genesis 1:1</code>, "
            "<code>/sefaria תהילים כג</code>, <code>/sefaria משנה ברכות א:א</code>")
    ref = " ".join(args).strip()
    try:
        j = await _json(f"https://www.sefaria.org/api/texts/{ref}",
                        {"lang": "he", "context": 0, "commentary": 0})
    except Exception as e:
        return await sendMessage(message, f"⚠️ שגיאה בחיבור לספריא: {escape(str(e)[:120])}")
    if not isinstance(j, dict) or ("he" not in j and "text" not in j):
        return await sendMessage(message, f"לא נמצא: \"{escape(ref)}\". נסה ניסוח אחר של המראה מקום.")
    he = j.get("he") or j.get("text") or []
    if isinstance(he, str):
        he = [he]
    text = "\n".join(_strip_html(str(x)) for x in he if str(x).strip())
    if not text:
        return await sendMessage(message, f"אין טקסט זמין בעברית עבור \"{escape(ref)}\".")
    link = "https://www.sefaria.org/" + re_sub(r"\s+", "_", j.get("ref") or ref)
    cap = 3500
    suffix = ""
    if len(text) > cap:
        text = text[:cap] + "..."
        suffix = "\n(קוצר)"
    await sendMessage(
        message,
        f"📖 <b>{escape(j.get('heRef') or j.get('ref') or ref)}</b>\n"
        f"<blockquote>{escape(text)}</blockquote>{suffix}\n"
        f"<a href='{link}'>המשך בספריא</a>",
    )


# ---------- small utilities ----------

def _safe_calc(expr):
    import ast
    import operator as op
    ops = {ast.Add: op.add, ast.Sub: op.sub, ast.Mult: op.mul,
           ast.Div: op.truediv, ast.FloorDiv: op.floordiv,
           ast.Mod: op.mod, ast.Pow: op.pow}
    def ev(node):
        if isinstance(node, ast.Expression):
            return ev(node.body)
        if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
            return node.value
        if isinstance(node, ast.BinOp) and type(node.op) in ops:
            l, r = ev(node.left), ev(node.right)
            if isinstance(node.op, ast.Pow) and abs(r) > 1000:
                raise ValueError("חזקה גדולה מדי")
            return ops[type(node.op)](l, r)
        if isinstance(node, ast.UnaryOp) and isinstance(node.op, (ast.UAdd, ast.USub)):
            v = ev(node.operand)
            return v if isinstance(node.op, ast.UAdd) else -v
        raise ValueError("ביטוי לא נתמך")
    tree = ast.parse(expr, mode="eval")
    return ev(tree)


async def calc_cmd(client, message):
    args = message.command[1:]
    if not args:
        return await sendMessage(message, "פורמט: /calc 2+3*4")
    expr = " ".join(args)
    try:
        res = _safe_calc(expr)
        if isinstance(res, float) and res.is_integer():
            res = int(res)
        elif isinstance(res, float):
            res = round(res, 6)
        await sendMessage(message, f"🧮 <code>{escape(expr)}</code> = <b>{res}</b>")
    except ZeroDivisionError:
        await sendMessage(message, "⚠️ חילוק באפס.")
    except Exception:
        await sendMessage(message, "⚠️ ביטוי לא תקין. נתמכים: + - * / // % ** וסוגריים.")


async def weather_cmd(client, message):
    args = message.command[1:]
    city = " ".join(args).strip() if args else "ירושלים"
    try:
        g = await _json("https://geocoding-api.open-meteo.com/v1/search",
                        {"name": city, "count": 1, "language": "he", "format": "json"})
        results = g.get("results") or []
        if not results:
            return await sendMessage(message, f"לא נמצאה עיר בשם \"{escape(city)}\".")
        loc = results[0]
        w = await _json("https://api.open-meteo.com/v1/forecast", {
            "latitude": loc["latitude"], "longitude": loc["longitude"],
            "current": "temperature_2m,apparent_temperature,relative_humidity_2m,weather_code,wind_speed_10m",
            "daily": "temperature_2m_max,temperature_2m_min,precipitation_probability_max",
            "timezone": "Asia/Jerusalem", "forecast_days": 1,
        })
    except Exception as e:
        return await sendMessage(message, f"⚠️ שגיאה בחיבור לשירות מזג האוויר: {escape(str(e)[:120])}")
    cur = w.get("current") or {}
    daily = w.get("daily") or {}
    desc = _WMO.get(cur.get("weather_code"), "?")
    name = loc.get("name", city)
    country = loc.get("country", "")
    out = [f"🌤 <b>{escape(name)}{', ' + escape(country) if country else ''}</b>",
           f"{desc} · <b>{cur.get('temperature_2m')}°</b> (מרגיש כמו {cur.get('apparent_temperature')}°)",
           f"לחות {cur.get('relative_humidity_2m')}% · רוח {cur.get('wind_speed_10m')} קמ\"ש"]
    try:
        out.append(f"היום: {daily['temperature_2m_min'][0]}° - {daily['temperature_2m_max'][0]}°"
                   f" · סיכוי למשקעים {daily['precipitation_probability_max'][0]}%")
    except Exception:
        pass
    await sendMessage(message, "\n".join(out))


async def qr_cmd(client, message):
    args = message.command[1:]
    text = " ".join(args).strip()
    if not text:
        return await sendMessage(message, "פורמט: /qr <טקסט או קישור>")
    try:
        import qrcode
        from io import BytesIO
        img = qrcode.make(text)
        buf = BytesIO()
        img.save(buf, "PNG")
        buf.seek(0)
        buf.name = "qr.png"
        await message.reply_photo(photo=buf, caption=f"🔳 QR עבור: {escape(text[:200])}")
    except ImportError:
        await sendMessage(message, "⚠️ ספריית QR לא מותקנת בשרת (qrcode).")
    except Exception as e:
        await sendMessage(message, f"⚠️ יצירת QR נכשלה: {escape(str(e)[:120])}")


# ---------- notes / tasks / reminders ----------

async def note_cmd(client, message):
    text = message.text.split(maxsplit=1)[1].strip() if len(message.command) > 1 or " " in message.text else ""
    if not text:
        return await sendMessage(message, "פורמט: /note <טקסט הפתק>")
    notes = list(await drive_state.get("notes", []))
    notes.append({"text": text[:1000], "created": int(time())})
    saved = await drive_state.put("notes", notes)
    warn = "" if saved else "\n<i>(לא נשמר ב-Drive - יימחק באתחול הבא)</i>"
    await sendMessage(message, f"📝 נשמר פתק מס׳ {len(notes)}.{warn}")


async def notes_cmd(client, message):
    notes = await drive_state.get("notes", [])
    if not notes:
        return await sendMessage(message, "אין פתקים שמורים. /note להוספה.")
    lines = ["📝 <b>פתקים:</b>"]
    for i, n in enumerate(notes[:50], 1):
        lines.append(f"{i}. {escape(n['text'][:120])}")
    if len(notes) > 50:
        lines.append(f"<i>(עוד {len(notes) - 50})</i>")
    lines.append("מחיקה: /notedel <מספר>")
    await sendMessage(message, "\n".join(lines))


async def notedel_cmd(client, message):
    args = message.command[1:]
    notes = list(await drive_state.get("notes", []))
    if not args or not args[0].isdigit() or not (1 <= int(args[0]) <= len(notes)):
        return await sendMessage(message, f"פורמט: /notedel <מספר 1-{len(notes)}>")
    idx = int(args[0]) - 1
    text = notes[idx]["text"][:60]

    async def _do(i):
        ns = list(await drive_state.get("notes", []))
        if 0 <= i < len(ns):
            ns.pop(i)
            await drive_state.put("notes", ns)

    tok = _new_pending(f"מחיקת פתק {idx + 1}", _do, idx)
    await sendMessage(message, f"למחוק את הפתק \"{escape(text)}\"?", _confirm_kb(tok))


async def task_cmd(client, message):
    text = message.text.split(maxsplit=1)[1].strip() if " " in message.text else ""
    if not text:
        return await sendMessage(message, "פורמט: /task <משימה חדשה>")
    tasks = list(await drive_state.get("tasks", []))
    tasks.append({"text": text[:500], "done": False, "created": int(time())})
    saved = await drive_state.put("tasks", tasks)
    warn = "" if saved else "\n<i>(לא נשמר ב-Drive - יימחק באתחול הבא)</i>"
    await sendMessage(message, f"✅ נוספה משימה מס׳ {len(tasks)}.{warn}")


def _task_lines(tasks, show_done=False):
    lines = []
    n = 0
    for i, t in enumerate(tasks, 1):
        if t.get("done") and not show_done:
            continue
        n += 1
        mark = "☑️" if t.get("done") else "⬜️"
        lines.append(f"{i}. {mark} {escape(t['text'][:120])}")
    return lines, n


async def tasks_cmd(client, message):
    tasks = await drive_state.get("tasks", [])
    open_count = sum(1 for t in tasks if not t.get("done"))
    if open_count == 0:
        extra = f" (ושהושלמו {len(tasks)})" if tasks else ""
        return await sendMessage(message, f"אין משימות פתוחות{extra}. /task להוספה.")
    lines, _ = _task_lines(tasks)
    out = ["📋 <b>משימות פתוחות:</b>"] + lines
    out.append("סיום: /done <מספר> · מחיקה: /taskdel <מספר>")
    await sendMessage(message, "\n".join(out))


async def done_cmd(client, message):
    args = message.command[1:]
    tasks = list(await drive_state.get("tasks", []))
    if not args or not args[0].isdigit() or not (1 <= int(args[0]) <= len(tasks)):
        return await sendMessage(message, f"פורמט: /done <מספר 1-{len(tasks)}>")
    idx = int(args[0]) - 1
    tasks[idx]["done"] = True
    await drive_state.put("tasks", tasks)
    await sendMessage(message, f"🎉 סומנה כבוצעה: {escape(tasks[idx]['text'][:100])}")


async def taskdel_cmd(client, message):
    args = message.command[1:]
    tasks = list(await drive_state.get("tasks", []))
    if not args or not args[0].isdigit() or not (1 <= int(args[0]) <= len(tasks)):
        return await sendMessage(message, f"פורמט: /taskdel <מספר 1-{len(tasks)}>")
    idx = int(args[0]) - 1
    text = tasks[idx]["text"][:60]

    async def _do(i):
        ts = list(await drive_state.get("tasks", []))
        if 0 <= i < len(ts):
            ts.pop(i)
            await drive_state.put("tasks", ts)

    tok = _new_pending(f"מחיקת משימה {idx + 1}", _do, idx)
    await sendMessage(message, f"למחוק את המשימה \"{escape(text)}\"?", _confirm_kb(tok))


_REM_UNITS = {
    "דקה": 60, "דקות": 60, "שעה": 3600, "שעות": 3600,
    "יום": 86400, "ימים": 86400, "שבוע": 604800, "שבועות": 604800,
}


def _parse_remind(args):
    now = datetime.now(TZ)
    if not args:
        return None
    if args[0] == "בעוד":
        rest = args[1:]
        if not rest:
            return None
        if rest[0] in _REM_UNITS:
            n, unit = 1, rest[0]
        elif len(rest) >= 2 and rest[0].isdigit() and rest[1] in _REM_UNITS:
            n, unit = int(rest[0]), rest[1]
        else:
            return None
        return now + timedelta(seconds=n * _REM_UNITS[unit])
    if args[0] == "מחר" and len(args) >= 2:
        m = fullmatch(r"(?:ב-?)?(\d{1,2}):(\d{2})", args[1])
        if not m:
            return None
        return now.replace(hour=int(m[1]), minute=int(m[2]),
                           second=0, microsecond=0) + timedelta(days=1)
    m = fullmatch(r"(\d{1,2}):(\d{2})", args[0])
    if m:
        due = now.replace(hour=int(m[1]), minute=int(m[2]), second=0, microsecond=0)
        if due <= now:
            due += timedelta(days=1)
        return due
    m = fullmatch(r"(\d{1,2})/(\d{1,2})(?:/(\d{2,4}))?", args[0])
    if m:
        y = int(m[3]) if m[3] else now.year
        if y < 100:
            y += 2000
        try:
            if len(args) >= 2:
                m2 = fullmatch(r"(\d{1,2}):(\d{2})", args[1])
                if not m2:
                    return None
                due = datetime(y, int(m[2]), int(m[1]), int(m2[1]), int(m2[2]), tzinfo=TZ)
            else:
                due = datetime(y, int(m[2]), int(m[1]), 9, 0, tzinfo=TZ)
        except ValueError:
            return None
        return due if due > now else None
    return None


def _rem_skip(args):
    if not args:
        return 0
    if args[0] == "בעוד":
        return 3 if len(args) >= 2 and args[0 + 1].isdigit() else 2
    if args[0] == "מחר":
        return 2
    if fullmatch(r"(\d{1,2})/(\d{1,2})(?:/(\d{2,4}))?", args[0]):
        return 2 if len(args) >= 2 and fullmatch(r"(\d{1,2}):(\d{2})", args[1]) else 1
    return 1


def _fmt_due(due):
    return f"יום {_WEEKDAYS[due.weekday()]}, {due.strftime('%d/%m %H:%M')}"


async def remind_cmd(client, message):
    args = message.command[1:]
    if not args:
        return await sendMessage(
            message,
            "פורמטים:\n<blockquote>"
            "/remind בעוד 30 דקות <טקסט>\n"
            "/remind בעוד 2 שעות <טקסט>\n"
            "/remind 18:30 <טקסט>\n"
            "/remind מחר 08:00 <טקסט>\n"
            "/remind 15/11 09:00 <טקסט></blockquote>"
            "רשימה: /reminders · ביטול: /remdel <מספר>")
    due = _parse_remind(args)
    skip = _rem_skip(args)
    text = " ".join(args[skip:]).strip()
    if due is None or not text:
        return await sendMessage(message, "⚠️ לא הבנתי את הזמן או שחסר טקסט. נסה לפי הדוגמאות ב-/remind")
    rems = list(await drive_state.get("reminders", []))
    rems.append({"due": int(due.timestamp()), "text": text[:500], "created": int(time())})
    saved = await drive_state.put("reminders", rems)
    warn = "" if saved else "\n<i>(לא נשמר ב-Drive - אם הבוט יאתחל התזכורת תאבד)</i>"
    await sendMessage(
        message,
        f"⏰ נקבע ל-{_fmt_due(due)}: {escape(text)}{warn}\n"
        "<i>התזכורת נשלחת כשהשרת פעיל; אם הוא מאתחל ברגע היעד היא תגיע מיד עם החזרה לאוויר.</i>")


async def reminders_cmd(client, message):
    rems = await drive_state.get("reminders", [])
    now = int(time())
    pending = [(i, r) for i, r in enumerate(rems, 1) if r["due"] > now]
    if not pending:
        return await sendMessage(message, "אין תזכורות פעילות. /remind לקביעה.")
    lines = ["⏰ <b>תזכורות פעילות:</b>"]
    for i, r in pending[:30]:
        due = datetime.fromtimestamp(r["due"], TZ)
        lines.append(f"{i}. {_fmt_due(due)} - {escape(r['text'][:80])}")
    lines.append("ביטול: /remdel <מספר>")
    await sendMessage(message, "\n".join(lines))


async def remdel_cmd(client, message):
    args = message.command[1:]
    rems = list(await drive_state.get("reminders", []))
    if not args or not args[0].isdigit() or not (1 <= int(args[0]) <= len(rems)):
        return await sendMessage(message, f"פורמט: /remdel <מספר 1-{len(rems)}>")
    idx = int(args[0]) - 1
    text = rems[idx]["text"][:60]

    async def _do(i):
        rs = list(await drive_state.get("reminders", []))
        if 0 <= i < len(rs):
            rs.pop(i)
            await drive_state.put("reminders", rs)

    tok = _new_pending(f"ביטול תזכורת {idx + 1}", _do, idx)
    await sendMessage(message, f"לבטל את התזכורת \"{escape(text)}\"?", _confirm_kb(tok))


async def _fire_due_reminders():
    rems = list(await drive_state.get("reminders", []))
    now = int(time())
    due = [r for r in rems if r["due"] <= now]
    if not due:
        return
    rems = [r for r in rems if r["due"] > now]
    await drive_state.put("reminders", rems)
    for r in due:
        await _notify(f"⏰ <b>תזכורת:</b> {escape(r['text'])}")


async def _boot_catchup():
    try:
        rems = list(await drive_state.get("reminders", []))
        now = int(time())
        late = [r for r in rems if r["due"] <= now]
        if late:
            rems = [r for r in rems if r["due"] > now]
            await drive_state.put("reminders", rems)
            lines = ["⏰ <b>תזכורות שהגיעו באיחור בגלל אתחול השרת:</b>"]
            for r in late:
                due = datetime.fromtimestamp(r["due"], TZ)
                lines.append(f"• ({_fmt_due(due)}) {escape(r['text'])}")
            await _notify("\n".join(lines))
        st = await drive_state.status()
        LOGGER.info(f"extras boot: drive={st['available']} account={st['account']}")
    except Exception as e:
        LOGGER.error(f"extras boot catchup: {e}")


# ---------- RSS ----------

async def _fetch_feed(url):
    import feedparser
    async with ClientSession(timeout=ClientTimeout(total=45)) as s:
        async with s.get(url, headers={"User-Agent": "linked123-bot/1.0"}) as r:
            raw = await r.read()
    return await to_thread(feedparser.parse, raw)


def _entry_id(e):
    return str(e.get("id") or e.get("link") or e.get("title") or "")[:300]


async def rss_cmd(client, message):
    args = message.command[1:]
    sub = args[0].lower() if args else "list"
    feeds = list(await drive_state.get("rss_feeds", []))

    if sub == "add":
        if len(args) < 2:
            return await sendMessage(message, "פורמט: /rss add <קישור לפיד> [שם]")
        if len(feeds) >= MAX_FEEDS:
            return await sendMessage(message, f"הגעת למגבלת {MAX_FEEDS} פידים.")
        url = args[1]
        name = " ".join(args[2:]).strip() if len(args) > 2 else ""
        wait = await sendMessage(message, "⏳ בודק את הפיד...")
        try:
            d = await _fetch_feed(url)
        except Exception as e:
            return await editMessage(wait, f"⚠️ לא הצלחתי לקרוא את הפיד: {escape(str(e)[:150])}")
        if getattr(d, "bozo", 0) and not d.entries:
            return await editMessage(wait, "⚠️ הקישור לא נראה כמו פיד RSS/Atom תקין.")
        title = name or (d.feed.get("title") if hasattr(d, "feed") else "") or url
        seen = [_entry_id(e) for e in d.entries[:200]]
        feeds.append({"url": url, "title": str(title)[:100],
                      "seen": seen, "added": int(time())})
        saved = await drive_state.put("rss_feeds", feeds)
        warn = "" if saved else "\n(לא נשמר ב-Drive - יימחק באתחול הבא)"
        await editMessage(
            wait,
            f"📰 נוסף הפיד <b>{escape(str(title))}</b> ({len(d.entries)} פריטים קיימים).\n"
            f"פריטים חדשים יישלחו לכאן, בדיקה פעם בשעה. {warn}")

    elif sub == "del":
        if len(args) < 2 or not args[1].isdigit() or not (1 <= int(args[1]) <= len(feeds)):
            return await sendMessage(message, f"פורמט: /rss del <מספר 1-{len(feeds)}>")
        idx = int(args[1]) - 1
        title = feeds[idx]["title"]

        async def _do(i):
            fs = list(await drive_state.get("rss_feeds", []))
            if 0 <= i < len(fs):
                fs.pop(i)
                await drive_state.put("rss_feeds", fs)

        tok = _new_pending(f"הסרת הפיד \"{title}\"", _do, idx)
        await sendMessage(message, f"להסיר את הפיד \"{escape(str(title))}\"?", _confirm_kb(tok))

    elif sub == "now":
        if not args or len(args) < 2 or not args[1].isdigit() or not (1 <= int(args[1]) <= len(feeds)):
            return await sendMessage(message, f"פורמט: /rss now <מספר 1-{len(feeds)}>")
        f = feeds[int(args[1]) - 1]
        wait = await sendMessage(message, f"⏳ מושך את \"{escape(str(f['title']))}\"...")
        try:
            d = await _fetch_feed(f["url"])
        except Exception as e:
            return await editMessage(wait, f"⚠️ שגיאה: {escape(str(e)[:150])}")
        lines = [f"📰 <b>{escape(str(f['title']))}</b> - 5 אחרונים:"]
        for e in d.entries[:5]:
            t = escape(str(e.get("title", "?"))[:150])
            link = e.get("link", "")
            lines.append(f"• <a href='{link}'>{t}</a>")
        if not d.entries:
            lines.append("(ריק)")
        await editMessage(wait, "\n".join(lines))

    else:
        if not feeds:
            return await sendMessage(
                message,
                "אין פידים. הוספה: /rss add <קישור> [שם]\n"
                "פריטים חדשים נשלחים אוטומטית, בדיקה פעם בשעה.")
        lines = ["📰 <b>פידים רשומים:</b>"]
        for i, f in enumerate(feeds, 1):
            lines.append(f"{i}. {escape(str(f['title']))}")
        lines.append("<i>הוספה: /rss add · הסרה: /rss del · עכשיו: /rss now</i>")
        await sendMessage(message, "\n".join(lines))


async def _rss_check():
    feeds = list(await drive_state.get("rss_feeds", []))
    if not feeds:
        return
    changed = False
    for f in feeds:
        try:
            d = await _fetch_feed(f["url"])
        except Exception as e:
            LOGGER.error(f"rss fetch {f['url']}: {e}")
            continue
        seen = list(f.get("seen") or [])
        new = [e for e in d.entries if _entry_id(e) and _entry_id(e) not in seen]
        if not new:
            continue
        for e in new[:5]:
            t = escape(str(e.get("title", "?"))[:200])
            link = e.get("link", "")
            await _notify(f"📰 <b>{escape(str(f['title']))}</b>\n<a href='{link}'>{t}</a>")
            seen.append(_entry_id(e))
        if len(new) > 5:
            await _notify(f"📰 {escape(str(f['title']))}: עוד {len(new) - 5} פריטים חדשים (נכנסו לרשימת הידועים).")
            for e in new[5:]:
                if _entry_id(e):
                    seen.append(_entry_id(e))
        f["seen"] = seen[-200:]
        changed = True
    if changed:
        await drive_state.put("rss_feeds", feeds)


# ---------- state diagnostics ----------

async def mystate_cmd(client, message):
    st = await drive_state.status()
    notes = await drive_state.get("notes", [])
    tasks = await drive_state.get("tasks", [])
    rems = await drive_state.get("reminders", [])
    feeds = await drive_state.get("rss_feeds", [])
    open_tasks = sum(1 for t in tasks if not t.get("done"))
    now = int(time())
    active_rems = sum(1 for r in rems if r["due"] > now)
    if st["available"]:
        persist = f"✅ Drive ({escape(st['account'] or '?')})"
    else:
        persist = "⚠️ זיכרון בלבד - הנתונים נמחקים באתחול"
    city_id = await drive_state.get("shabbat_city", _DEFAULT_CITY)
    city_name = next((k for k, v in _CITIES.items() if v == city_id), "ירושלים")
    await sendMessage(
        message,
        "🔧 <b>מצב הבוט</b>\n"
        f"שמירה קבועה: {persist}\n"
        f"עיר לזמני שבת: {escape(city_name)}\n"
        f"פתקים: {len(notes)} · משימות פתוחות: {open_tasks} · "
        f"תזכורות: {active_rems} · פידים: {len(feeds)}\n"
        f"מתזמן פעיל: {'כן' if scheduler.running else 'לא'}")


# ---------- registration ----------

_CMDS = [
    (BotCommands.HebDateCommand, hebdate_cmd),
    (BotCommands.ShabbatCommand, shabbat_cmd),
    (BotCommands.SefariaCommand, sefaria_cmd),
    (BotCommands.CalcCommand, calc_cmd),
    (BotCommands.WeatherCommand, weather_cmd),
    (BotCommands.QrCommand, qr_cmd),
    (BotCommands.NoteCommand, note_cmd),
    (BotCommands.NotesCommand, notes_cmd),
    (BotCommands.NoteDelCommand, notedel_cmd),
    (BotCommands.TaskCommand, task_cmd),
    (BotCommands.TasksCommand, tasks_cmd),
    (BotCommands.DoneCommand, done_cmd),
    (BotCommands.TaskDelCommand, taskdel_cmd),
    (BotCommands.RemindCommand, remind_cmd),
    (BotCommands.RemindersCommand, reminders_cmd),
    (BotCommands.RemindDelCommand, remdel_cmd),
    (BotCommands.RssCommand, rss_cmd),
    (BotCommands.MyStateCommand, mystate_cmd),
]

for _cmd, _fn in _CMDS:
    bot.add_handler(MessageHandler(_fn, filters=command(_cmd) & CustomFilters.owner))
bot.add_handler(CallbackQueryHandler(extras_confirm_cb, filters=regex(r"^xcf\|")))

async def start_extras():
    # Call once the event loop runs (scheduler.start needs a running loop).
    scheduler.add_job(_fire_due_reminders, "interval", seconds=REM_INTERVAL,
                      id="extras_remind", replace_existing=True, misfire_grace_time=120)
    scheduler.add_job(_rss_check, "interval", seconds=RSS_INTERVAL,
                      id="extras_rss", replace_existing=True, misfire_grace_time=600)
    scheduler.add_job(_boot_catchup, "date",
                      run_date=datetime.now(TZ) + timedelta(seconds=45),
                      id="extras_boot", replace_existing=True)
    if not scheduler.running:
        scheduler.start()
    LOGGER.info("extras started: calendar, tools, reminders, RSS")
