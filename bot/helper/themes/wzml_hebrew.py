#!/usr/bin/env python3
# Hebrew theme: overrides user-facing text, keeps all placeholders and layout.
from bot.helper.themes.wzml_minimal import WZMLStyle as _Base


class WZMLStyle(_Base):
    ST_BN1_NAME = "אתר 🌵"
    ST_BN2_NAME = "קבוצה 🧲"
    ST_MSG = """<i>הבוט הזה מוריד קישורים וקבצים ומעלה אותם לטלגרם או לגוגל דרייב.</i>

<blockquote><b>שלח {help_command} כדי לראות את רשימת הפקודות</b></blockquote>"""
    ST_BOTPM = """<b><i>מעכשיו הבוט ישלח לכאן את כל הקבצים והקישורים שלך...</i></b>"""
    ST_UNAUTH = """<i>אין לך הרשאה להשתמש בבוט הזה.</i>"""
    OWN_TOKEN_GENERATE = """<b>הטוקן הזמני הזה לא שלך!</b>\n\n<i>צור טוקן משלך.</i>"""
    USED_TOKEN = """<b>הטוקן הזמני כבר נוצל!</b>\n\n<i>צור טוקן חדש.</i>"""
    LOGGED_PASSWORD = """<b>הבוט כבר מחובר באמצעות סיסמה</b>\n\n<i>אין צורך בטוקן זמני.</i>"""
    ACTIVATE_BUTTON = "הפעל טוקן זמני"
    TOKEN_MSG = """<b><u>נוצר טוקן כניסה זמני!</u></b>
<b>טוקן:</b> <code>{token}</code>
<b>תוקף:</b> {validity}"""
    ACTIVATED = "✅️ הופעל ✅"
    LOGGED_IN = "<b>כבר מחובר!</b>"
    INVALID_PASS = "<b>סיסמה שגויה!</b>\n\nהזן את הסיסמה הנכונה."
    PASS_LOGGED = "<b>התחברת לבוט באופן קבוע!</b>"
    LOGIN_USED = "<b>שימוש בהתחברות:</b>\n\n<code>/cmd [סיסמה]</code>"
    LOG_DISPLAY_BT = "📑 הצג לוג"
    WEB_PASTE_BT = "📨 הדבק באינטרנט"
    BASIC_BT = "בסיסי"
    USER_BT = "משתמשים"
    MICS_BT = "שונות"
    O_S_BT = "בעלים וסודו"
    HELP_HEADER = "㊂ <b><i>תפריט עזרה</i></b>\n\n<b>לחץ על פקודה כדי לראות פרטים נוספים.</b>"

    BOT_STATS = """⌬ <b><i>סטטיסטיקת הבוט:</i></b>
╰ <b>זמן פעילות:</b> {bot_uptime}

<blockquote>╭ <b><i>זיכרון (RAM):</i></b>
┊ {ram_bar} {ram}%
╰ <b>בשימוש:</b> {ram_u} | <b>פנוי:</b> {ram_f} | <b>סה"כ:</b> {ram_t}</blockquote>

<blockquote>╭ <b><i>זיכרון SWAP:</i></b>
┊ {swap_bar} {swap}%
╰ <b>בשימוש:</b> {swap_u} | <b>פנוי:</b> {swap_f} | <b>סה"כ:</b> {swap_t}</blockquote>

<blockquote>╭ <b><i>דיסק:</i></b>
┊ {disk_bar} {disk}%
┊ <b>קריאה:</b> {disk_read}
┊ <b>כתיבה:</b> {disk_write}
╰ <b>בשימוש:</b> {disk_u} | <b>פנוי:</b> {disk_f} | <b>סה"כ:</b> {disk_t}</blockquote>
    """
    RESTARTING = "<i>מפעיל מחדש...</i>"
    RESTART_SUCCESS = """⌬ <b><i>הבוט הופעל מחדש בהצלחה!</i></b>
<blockquote>╭ <b>תאריך:</b> {date}
┊ <b>שעה:</b> {time}
┊ <b>אזור זמן:</b> {timz}
╰ <b>גרסה:</b> {version}</blockquote>"""
    RESTARTED = """⌬ <b><i>הבוט הופעל מחדש!</i></b>"""
    PING = "<i>בודק תגובה..</i>"
    PING_VALUE = "<b>פונג</b>\n╰ <code>{value} מ״ש..</code>"

    LINKS_START = """<b><i>המשימה התחילה</i></b>
<blockquote>┊ <b>מצב:</b> {Mode}
╰ <b>על ידי:</b> {Tag}\n\n"""
    LINKS_SOURCE = """➲ <b>מקור:</b>
╰ <b>נוסף ב:</b> {On}</blockquote>
------------------------------------------
{Source}
------------------------------------------\n\n"""
    PM_START = "➲ <b><u>המשימה התחילה </u></b>🏁\n┊\n╰ <b>קישור:</b> <a href='{msg_link}'>לחץ כאן</a>"
    L_LOG_START = "➲ <b><u>ההורדה התחילה </u></b>🏁\n┊\n┊ <b>משתמש:</b> {mention} ( #ID{uid} )\n╰ <b>מקור:</b> <a href='{msg_link}'>לחץ כאן</a>"

    NAME = "<blockquote>╭ <b>שם:</b> <code>{Name}</code>\n"
    SIZE = "┊ <b>גודל: </b>{Size}\n"
    ELAPSE = "┊ <b>זמן: </b>{Time}\n"
    MODE = "┊ <b>מצב: </b>{Mode}\n"
    L_TOTAL_FILES = "┊ <b>סה״כ קבצים: </b>{Files}\n"
    L_CORRUPTED_FILES = "┊ <b>קבצים פגומים: </b>{Corrupt}\n"
    L_CC = "╰ <b>על ידי: </b>{Tag}</blockquote>\n\n"
    PM_BOT_MSG = "➲ <b><i>הקבצים נשלחו למעלה</i></b>"
    L_BOT_MSG = "➲ <b><i>הקבצים נשלחו לצ'אט הפרטי עם הבוט</i></b>"
    L_LL_MSG = "➲ <b><i>הקבצים נשלחו. הגישה דרך הקישורים...</i></b>\n"
    N_BOT_MSG = "➲ <i><b>קבצים:</b></i>"
    M_TYPE = "┊ <b>סוג: </b>{Mimetype}\n"
    M_SUBFOLD = "┊ <b>תיקיות משנה: </b>{Folder}\n"
    TOTAL_FILES = "┊ <b>קבצים: </b>{Files}\n"
    RCPATH = "┊ <b>נתיב: </b><code>{RCpath}</code>\n"
    M_CC = "╰ <b>על ידי: </b>{Tag}\n\n</blockquote>"
    M_BOT_MSG = "➲ <b><i>הקישורים נשלחו לצ'אט הפרטי עם הבוט</i></b>"
    CLOUD_LINK = "☁️ קישור לענן"
    SAVE_MSG = "📨 שמור הודעה"
    RCLONE_LINK = "♻️ קישור RClone"
    DDL_LINK = "📎 קישור {Serv}"
    SOURCE_URL = "🔐 קישור מקור"
    INDEX_LINK_F = "🗂 קישור אינדקס"
    INDEX_LINK_D = "⚡ קישור אינדקס"
    VIEW_LINK = "🌐 צפייה"
    CHECK_PM = "📥 צפייה בצ'אט הפרטי"
    CHECK_LL = "🖇 צפייה בלוג הקישורים"
    MEDIAINFO_LINK = "📃 מידע על המדיה"
    SCREENSHOTS = "🖼 צילומי מסך"

    STATUS_NAME = "<blockquote>╭ <b>שם:</b> <code>{Name}</code>"
    PROCESSED = "\n┊ <b>הושלם:</b> {Processed}"
    ETA = " | <b>נותר:</b> {Eta}"
    SPEED = "\n┊ <b>מהירות:</b> {Speed}"
    ELAPSED = " | <b>עבר:</b> {Elapsed}"
    ENGINE = "\n┊ <b>מנוע:</b> {Engine}"
    STA_MODE = "\n┊ <b>מצב:</b> {Mode}"
    STATUS_SIZE = "\n┊ <b>גודל: </b>{Size}"
    NON_ENGINE = "\n┊ <b>מנוע:</b> {Engine}"
    USER = "\n┊ <b>משתמש:</b> <code>{User}</code> | "
    BTSEL = "\n┊ <b>בחירה:</b> {Btsel}"
    TASKS = "┊ <b>משימות:</b> {Tasks}\n"
    BOT_TASKS = "<blockquote>➲ <b>משימות:</b> {Tasks}/{Ttask} | <b>פנוי:</b> {Free}</blockquote>\n"
    Cpu = "<blockquote>╭ <b>מעבד:</b> {cpu}% | "
    FREE = "<b>פנוי:</b> {free} [{free_p}%]"
    uptime = "<b>זמן פעילות:</b> {uptime}"
    DL = "\n╰ <b>הורדה:</b> {DL}/s | "
    UL = "<b>העלאה:</b> {UL}/s</blockquote>"

    STOP_DUPLICATE = "הקובץ או התיקייה כבר קיימים בדרייב.\nהנה תוצאות ({content}):"
    COUNT_MSG = "<b>סופר:</b> <code>{LINK}</code>"
    LIST_SEARCHING = "<b>מחפש את <i>{NAME}</i></b>"
    LIST_FOUND = "<b>נמצאו {NO} תוצאות עבור <i>{NAME}</i></b>"
    LIST_NOT_FOUND = "לא נמצאו תוצאות עבור <i>{NAME}</i>"
    NO_ACTIVE_DL = """<i>אין הורדות פעילות כרגע.</i>

⌬ <b><i>מצב הבוט</i></b>
<blockquote>╭ <b>מעבד:</b> {cpu}% | <b>פנוי:</b> {free} [{free_p}%]
╰ <b>זיכרון:</b> {ram} | <b>זמן פעילות:</b> {uptime}</blockquote>
    """
