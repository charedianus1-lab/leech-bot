#!/usr/bin/env python3
# Hebrew help pages. Commands stay in English. Yemot-management build.
from bot.helper.telegram_helper.bot_commands import BotCommands as B

_G_YM = f'''⌬ <b><i>ימות המשיח - סטטוס ושיחות</i></b>

<blockquote>╭ /{B.YemotCommand[0]} או /{B.YemotCommand[1]}: תפריט ניהול הראשי עם כפתורים.
┊ /{B.YmStatCommand}: סטטוס הקו - האם השרת פעיל וכמה שיחות פעילות עכשיו.
╰ /{B.YmCallsCommand}: רשימת השיחות הפעילות כרגע בקו.</blockquote>'''

_G_FILES = f'''⌬ <b><i>ימות המשיח - קבצים</i></b>

<blockquote>נתיבים נכתבים בלי קידומת (למשל <code>/AI/in</code>) או עם <code>ivr2:</code> - שניהם עובדים.
╭ /{B.YmFilesCommand} [נתיב]: רשימת הקבצים והתיקיות בנתיב (ברירת מחדל: השורש).
┊ /{B.YmTxtCommand} &lt;נתיב&gt;: הצגת תוכן של קובץ טקסט או הגדרות מהקו.
┊ /{B.YmDlCommand} &lt;נתיב&gt;: הורדת קובץ מהקו לטלגרם (עד 45MB).
┊ /{B.YmUpCommand} &lt;נתיב יעד&gt;: בתגובה לקובץ בטלגרם - מעלה אותו לקו (עד 19MB). אם הקובץ קיים תתבקש לאשר דריסה.
┊ /{B.YmWriteCommand} &lt;נתיב&gt; &lt;טקסט&gt;: כתיבת קובץ טקסט חדש בקו. אם קיים - דריסה באישור בלבד.
╰ /{B.YmDelCommand} &lt;נתיב&gt;: מחיקת קובץ מהקו. דורש אישור, בלתי הפיך.</blockquote>'''

_G_EXT = f'''⌬ <b><i>ימות המשיח - שלוחות</i></b>

<blockquote>╭ /{B.YmExtCommand}: הצגת הגדרות כל שלוחות המערכת.
╰ /{B.YmSetCommand} &lt;נתיב שלוחה&gt; מפתח=ערך ...: שינוי הגדרות שלוחה. דורש אישור.
דוגמה: <code>/{B.YmSetCommand} /5 type=playfile playfile=/000.wav</code></blockquote>'''

_G_MSG = f'''⌬ <b><i>ימות המשיח - הודעות וקמפיינים</i></b>

<blockquote>╭ /{B.YmSmsCommand} &lt;טלפון&gt; &lt;הודעה&gt;: שליחת SMS מהקו. דורש אישור.
┊ /{B.YmTzCommand} &lt;טלפון&gt;: שליחת צינתוק (שיחה מתנתקת). דורש אישור.
╰ /{B.YmCampCommand}: תבניות הקמפיין במערכת. הפעלת קמפיין תתווסף בעתיד.</blockquote>'''

_G_ADMIN = f'''⌬ <b><i>ניהול הבוט (בעלים וסודו)</i></b>

<blockquote>╭ /{B.RestartCommand[0]} או /{B.RestartCommand[1]}: הפעלה מחדש של הבוט.
┊ /{B.LogCommand}: קובץ הלוג של הבוט.
┊ /{B.PingCommand[0]}: בדיקת זמן תגובה.
┊ /{B.UserSetCommand[0]} או /{B.UserSetCommand[1]}: הגדרות אישיות.
╰ /{B.ShellCommand}: הרצת פקודת מעטפת בשרת (בעלים בלבד).</blockquote>'''

GUIDE = [
    ("ym", "סטטוס ושיחות", _G_YM),
    ("files", "קבצים", _G_FILES),
    ("ext", "שלוחות", _G_EXT),
    ("msg", "הודעות", _G_MSG),
    ("admin", "ניהול", _G_ADMIN),
]
GUIDE_HOME = "㊂ <b><i>ניהול ימות המשיח</i></b>\n\nבחר קטגוריה כדי לראות את הפקודות. מחיקות ושינויים מבקשים אישור לפני ביצוע."
