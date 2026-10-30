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


_G_HEB = f'''⌬ <b><i>לוח עברי ולימוד</i></b>

<blockquote>╭ /{B.HebDateCommand} [תאריך]: התאריך העברי של היום, או המרה של תאריך לועזי (למשל /{B.HebDateCommand} 30/10/2026).
┊ /{B.ShabbatCommand} [עיר]: פרשת השבוע, הדלקת נרות והבדלה לפי עיר. שליחה עם שם עיר שומרת אותה כברירת מחדל.
╰ /{B.SefariaCommand} &lt;מראה מקום&gt;: פתיחת מקור בספריא, למשל <code>/{B.SefariaCommand} תהילים כג</code>.</blockquote>'''

_G_TOOLS = f'''⌬ <b><i>כלים קטנים</i></b>

<blockquote>╭ /{B.CalcCommand} &lt;ביטוי&gt;: מחשבון, למשל <code>/{B.CalcCommand} 2+3*4</code>.
┊ /{B.WeatherCommand} [עיר]: מזג אוויר עכשיו ותחזית להיום.
╰ /{B.QrCommand} &lt;טקסט&gt;: יצירת קוד QR.</blockquote>'''

_G_REM = f'''⌬ <b><i>תזכורות, משימות ופתקים</i></b>

<blockquote>╭ /{B.RemindCommand} בעוד 30 דקות לקנות חלב - דוגמאות זמן: "בעוד 2 שעות", "18:30", "מחר 08:00", "15/11 09:00".
┊ /{B.RemindersCommand}: תזכורות פעילות. ביטול: /{B.RemindDelCommand} &lt;מספר&gt;.
┊ /{B.TaskCommand} &lt;משימה&gt;: הוספה. /{B.TasksCommand}: רשימה. /{B.DoneCommand} &lt;מספר&gt;: סימון שבוצע. /{B.TaskDelCommand} &lt;מספר&gt;: מחיקה באישור.
┊ /{B.NoteCommand} &lt;פתק&gt;: שמירה. /{B.NotesCommand}: רשימה. /{B.NoteDelCommand} &lt;מספר&gt;: מחיקה באישור.
╰ התזכורות נשמרות ב-Drive של הבוט ונשלחות כשהשרת פעיל; אחרי אתחול תקבל אותן מיד עם החזרה לאוויר.</blockquote>'''

_G_RSS = f'''⌬ <b><i>חדשות ועדכוני RSS</i></b>

<blockquote>╭ /{B.RssCommand} add &lt;קישור לפיד&gt; [שם]: הרשמה לעדכונים מאתר.
┊ /{B.RssCommand}: רשימת הפידים הרשומים.
┊ /{B.RssCommand} now &lt;מספר&gt;: 5 הפריטים האחרונים מהפיד.
╰ /{B.RssCommand} del &lt;מספר&gt;: הסרת פיד (באישור). בדיקה פעם בשעה; פריטים חדשים נשלחים לפרטי.</blockquote>'''

_G_STATE = f'''⌬ <b><i>מצב ושמירה</i></b>

<blockquote>╭ /{B.MyStateCommand}: איפה נשמרים הנתונים (חשבון ה-Drive), ספירת פתקים/משימות/תזכורות/פידים, ומצב המתזמן.
╰ הנתונים האישיים נשמרים בקובץ JSON בדרייב שאליו הבוט כבר מעלה, לא בשרת הזמני.</blockquote>'''

GUIDE = [
    ("heb", "לוח עברי", _G_HEB),
    ("rem", "תזכורות", _G_REM),
    ("rss", "חדשות RSS", _G_RSS),
    ("tools", "כלים", _G_TOOLS),
    ("state", "מצב ושמירה", _G_STATE),
    ("ym", "ימות: סטטוס", _G_YM),
    ("files", "קבצים", _G_FILES),
    ("ext", "שלוחות", _G_EXT),
    ("msg", "הודעות", _G_MSG),
    ("admin", "ניהול", _G_ADMIN),
]
GUIDE_HOME = "㊂ <b><i>ימות המשיח וכלים אישיים</i></b>\n\nבחר קטגוריה כדי לראות את הפקודות. מחיקות ושינויים מבקשים אישור לפני ביצוע."
