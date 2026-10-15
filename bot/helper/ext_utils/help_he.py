#!/usr/bin/env python3
# Hebrew help pages. Commands stay in English.
from bot.helper.telegram_helper.bot_commands import BotCommands as B

help_string = [f'''⌬ <b><i>פקודות בסיסיות</i></b>

<blockquote><b>הורדה והעלאה לענן (Mirror):</b>
╭ /{B.MirrorCommand[0]} או /{B.MirrorCommand[1]}: הורדת קישור/קובץ והעלאה לענן.
╰ /{B.CategorySelect}: בחירת קטגוריה להעלאה לענן.

<b>יוטיוב ואתרים נתמכים (yt-dlp):</b>
╰ /{B.YtdlCommand[0]} או /{B.YtdlCommand[1]}: הורדת קישור שנתמך ב-yt-dlp והעלאה לענן.

<b>הורדה לטלגרם (Leech):</b>
╭ /{B.LeechCommand[0]} או /{B.LeechCommand[1]}: הורדת קישור/קובץ והעלאה לטלגרם.
╰ /{B.YtdlLeechCommand[0]} או /{B.YtdlLeechCommand[1]}: הורדה עם yt-dlp (קישור נתמך) והעלאה לטלגרם.

<b>גוגל דרייב:</b>
╭ /{B.CloneCommand[0]}: העתקת קובץ/תיקייה לדרייב.
┊ /{B.CountCommand} [קישור_דרייב]: ספירת קבצים ותיקיות בדרייב.
╰ /{B.DeleteCommand} [קישור_דרייב]: מחיקת קובץ/תיקייה מהדרייב (בעלים וסודו בלבד).

<b>ביטול משימות:</b>
╰ /{B.CancelMirror}: ביטול משימה לפי מזהה (gid) או בתגובה להודעה.</blockquote>''',

f'''⌬ <b><i>פקודות משתמש</i></b>

<blockquote><b>הגדרות:</b>
┊ /{B.UserSetCommand[0]} או /{B.UserSetCommand[1]} [חיפוש]: פתיחת ההגדרות האישיות (גם בפרטי).
╰ /{B.CoverCommand}: בתגובה לסרטון, קובע תמונה ממוזערת / פוסטר כשער שלו.

<b>הזדהות:</b>
╰ /login: התחברות לבוט בלי סיסמה זמנית (בפרטי).

<b>מצב הבוט:</b>
╭ /{B.StatusCommand[0]} או /{B.StatusCommand[1]}: מציג את כל המשימות הפעילות. אפשר להוסיף <code>me</code> או מזהה משתמש כדי לראות רק את שלו.
┊ /{B.StatsCommand[0]} או /{B.StatsCommand[1]}: נתוני השרת בפירוט.
╰ /{B.PingCommand[0]} או /{B.PingCommand[1]}: בדיקת זמן תגובה של הבוט.

<b>RSS:</b>
╰ /{B.RssCommand}: תפריט RSS (הרשמה/ביטול/הפעלה/השהיה)</blockquote>''',

f'''⌬ <b><i>פקודות בעלים וסודו</i></b>

<blockquote><b>הגדרות הבוט:</b>
╭ /{B.BotSetCommand[0]} או /{B.BotSetCommand[1]} [חיפוש]: פתיחת הגדרות הבוט (בעלים וסודו בלבד).
╰ /{B.UsersCommand}: נתוני משתמשים (בעלים וסודו בלבד).

<b>הרשאות:</b>
╭ /{B.AuthorizeCommand[0]} או /{B.AuthorizeCommand[1]}: מתן הרשאה לצ'אט או משתמש להשתמש בבוט (בעלים וסודו בלבד).
┊ /{B.UnAuthorizeCommand[0]} או /{B.UnAuthorizeCommand[1]}: ביטול הרשאה לצ'אט או משתמש (בעלים וסודו בלבד).
┊ /{B.AddSudoCommand}: הוספת משתמש סודו (בעלים בלבד).
┊ /{B.RmSudoCommand}: הסרת משתמש סודו (בעלים בלבד).
┊ /{B.AddBlackListCommand[0]} או /{B.AddBlackListCommand[1]}: הוספת משתמש לרשימה השחורה, הוא לא יוכל להשתמש בבוט.
╰ /{B.RmBlackListCommand[0]} או /{B.RmBlackListCommand[1]}: הסרת משתמש מהרשימה השחורה.

<b>הודעות לכולם:</b>
╰ /{B.BroadcastCommand[0]} או /{B.BroadcastCommand[1]} [תגובה להודעה]: שליחת הודעה לכל מי שהפעיל את הבוט בפרטי.

<b>גוגל דרייב:</b>
╰ /{B.GDCleanCommand[0]} או /{B.GDCleanCommand[1]} [מזהה_תיקייה]: מחיקת כל הקבצים מתיקייה בדרייב.

<b>ביטול משימות:</b>
╰ /{B.CancelAllCommand[0]}: ביטול כל המשימות, ו-/{B.CancelAllCommand[1]} לכמה בוטים.

<b>תחזוקה:</b>
╭ /{B.RestartCommand[0]} או /{B.RestartCommand[1]}: הפעלה מחדש ועדכון הבוט (בעלים וסודו בלבד).
┊ /{B.RestartCommand[2]}: הפעלה מחדש ועדכון של כל הבוטים (בעלים וסודו בלבד).
╰ /{B.LogCommand}: קובץ הלוג של הבוט, שימושי לבדיקת קריסות (בעלים וסודו בלבד).

<b>הרצת קוד:</b>
╭ /{B.ShellCommand}: הרצת פקודות מעטפת (בעלים בלבד).
┊ /{B.EvalCommand}: הרצת קוד פייתון (בעלים בלבד).
┊ /{B.ExecCommand}: הרצת פקודות ב-Exec (בעלים בלבד).
┊ /{B.ClearLocalsCommand}: ניקוי משתני {B.EvalCommand} או {B.ExecCommand} (בעלים בלבד).
╰ /exportsession: יצירת StringSession של המשתמש (בעלים בלבד).

<b>RSS:</b>
╰ /{B.RssCommand}: תפריט RSS (הרשמה/ביטול/הפעלה/השהיה)

<b>נוספים:</b>
╭ /{B.AddImageCommand} [קישור/תמונה]: הוספת תמונות לבוט.
╰ /{B.ImagesCommand}: רשת של התמונות השמורות.</blockquote>''',

f'''⌬ <b><i>פקודות שונות</i></b>

<blockquote><b>נוספים:</b>
╭ /{B.SpeedCommand[0]} או /{B.SpeedCommand[1]}: בדיקת מהירות השרת.
╰ /{B.MediaInfoCommand[0]} או /{B.MediaInfoCommand[1]} [קישור/מדיה]: פרטי מדיה של קובץ או קישור הורדה.

<b>חיפוש בדרייב:</b>
╰ /{B.ListCommand} [חיפוש]: חיפוש בגוגל דרייב.

<b>חיפוש סרטים וסדרות:</b>
╭ /{B.IMDBCommand}: חיפוש ב-IMDB.
┊ /{B.AniListCommand}: חיפוש אנימה ב-AniList.
┊ /{B.AnimeHelpCommand}: מדריך אנימה.
╰ /{B.MyDramaListCommand}: חיפוש ב-MyDramaList.</blockquote>
''']

PASSWORD_ERROR_MESSAGE = """
<blockquote><b>הקישור הזה דורש סיסמה!</b>
- הוסף <b>::</b> אחרי הקישור וכתוב את הסיסמה אחרי הסימן.
<b>לדוגמה:</b> {}::הסיסמה
שים לב: בלי רווחים לפני ואחרי <b>::</b>
בסיסמה עצמה מותר רווח.</blockquote>
"""

_ARGS = {
    "name": ("שם חדש", """㊂ <b>שם חדש</b> » <code>-n</code>

<blockquote>שינוי שם הקובץ או התיקייה לפני ההעלאה.
➲ <code>/cmd link -n My Movie 2024.mkv</code></blockquote>
<i>לא מתאים לקבצים רבים. התחילית/סיומת/הסרת טקסט מ-/us ממשיכות לחול.</i>"""),
    "yt_name": ("שם חדש", """㊂ <b>שם חדש</b> » <code>-n</code>

<blockquote>שינוי שם הקובץ שהורד.
➲ <code>/cmd link -n My Video</code></blockquote>
<i>בלי סיומת, yt-dlp מוסיף אותה לבד.</i>"""),
    "zip": ("חילוץ / דחיסה", """㊂ <b>חילוץ / דחיסה</b> » <code>-e</code> <code>-z</code>

<blockquote>➲ <code>/cmd link -e</code> חילוץ ארכיון
➲ <code>/cmd link -e pass123</code> חילוץ עם סיסמה
➲ <code>/cmd link -z</code> דחיסה ל-zip
➲ <code>/cmd link -z pass123</code> דחיסה עם סיסמה
➲ <code>/cmd link -e -z</code> חילוץ ואז דחיסה מחדש</blockquote>
<i>כששניהם מופיעים, קודם מחלצים.</i>"""),
    "yt_zip": ("דחיסה", """㊂ <b>דחיסה</b> » <code>-z</code>

<blockquote>➲ <code>/cmd link -z</code> דחיסה ל-zip
➲ <code>/cmd link -z pass123</code> דחיסה עם סיסמה</blockquote>
<i>שימושי לפלייליסטים, מקבלים ארכיון אחד.</i>"""),
    "upload": ("העלאה אל", """㊂ <b>העלאה אל</b> » <code>-up</code>

<blockquote>בחירת יעד הקבצים. בלי זה הבוט משתמש ביעד ברירת המחדל.
➲ <code>/cmd link -up gd</code> גוגל דרייב
➲ <code>/cmd link -up rc</code> נתיב RClone שלך
➲ <code>/cmd link -up ddl</code> שרתי DDL שלך (GoFile, PixelDrain...)
➲ <code>/cmd link -up rcl</code> בחירת שרת ותיקייה בכפתורים
➲ <code>/cmd link -up remote:folder</code> נתיב rclone ישיר
➲ <code>/cmd link -up mrcc:remote:folder</code> עם rclone.conf שלך
➲ <code>/cmd link -up movies</code> נתיב העלאה ששמרת ב-/us</blockquote>
<i>שרתי DDL, RClone ונתיבי העלאה מגדירים ב-/us ← Mirror.</i>"""),
    "dump": ("צ'אט יעד", """㊂ <b>צ'אט יעד</b> » <code>-ud</code>

<blockquote>שליחת הקבצים לצ'אט או לערוץ במקום לכאן.
➲ <code>/cmd link -ud MyChannel</code> יעד שמור ב-/us
➲ <code>/cmd link -ud -100123456789</code> מזהה צ'אט
➲ <code>/cmd link -ud @mychannel</code> שם משתמש
➲ <code>/cmd link -ud all</code> כל היעדים השמורים שלך</blockquote>
<i>הבוט חייב להיות מנהל שם. עם יותר מיעד אחד ובלי <code>-ud</code> מקבלים כפתורים.</i>"""),
    "multi": ("כמה קישורים", """㊂ <b>כמה קישורים</b> » <code>-i</code>

<blockquote>הרצת כמה קישורים/קבצים ברצף. עונים על ה<b>ראשון</b>:
➲ <code>/cmd -i 5</code> ההודעה הזו וארבע אחריה</blockquote>
<i>כל אחד רץ כמשימה נפרדת.</i>"""),
    "samedir": ("אותה תיקייה", """㊂ <b>אותה תיקייה</b> » <code>-m</code>

<blockquote>שמירת הקבצים של כמה קישורים בתיקייה אחת.
➲ <code>/cmd -i 5 -m Season 1</code>
➲ <code>/cmd -b -m Season 1</code></blockquote>
<i>מתאים עם <code>-z</code> כדי לקבל ארכיון אחד של הכול.</i>"""),
    "bulk": ("רשימת קישורים", """㊂ <b>רשימת קישורים</b> » <code>-b</code>

<blockquote>עונים על הודעה או קובץ txt עם קישור בכל שורה:
<code>link1 -n first name</code>
<code>link2 -z</code>
<code>link3 -e</code>
ואז עונים עליה עם <code>/cmd -b</code>
➲ <code>/cmd -b 3:8</code> רק קישורים 3 עד 8
➲ <code>/cmd -b :10</code> 10 הקישורים הראשונים</blockquote>
<i>הארגומנטים של כל קישור כתובים באותה שורה שלו.</i>"""),
    "join": ("חיבור חלקים", """㊂ <b>חיבור חלקים</b> » <code>-j</code>

<blockquote>חיבור קבצים מפוצלים (.001 .002 ...) לקובץ אחד.
➲ <code>/cmd link -j</code> קישור לקבצים מפוצלים
➲ <code>/cmd -i 3 -j -m folder</code> חלקים שנשלחו ב-3 הודעות</blockquote>
<i>רץ לפני חילוץ ודחיסה.</i>"""),
    "select": ("בחירת קבצים", """㊂ <b>בחירת קבצים</b> » <code>-s</code>

<blockquote>בחירה אילו קבצים להוריד.
➲ <code>/cmd link -s</code></blockquote>
<i>מקבלים כפתור לפתיחת רשימת הקבצים.</i>"""),
    "yt_select": ("איכות", """㊂ <b>איכות</b> » <code>-s</code>

<blockquote>תמיד להציג כפתורי איכות, גם אם הוגדר פורמט ברירת מחדל באפשרויות YT-DLP.
➲ <code>/cmd link -s</code></blockquote>"""),
    "seed": ("זריעה", """㊂ <b>זריעה</b> » <code>-d</code>

<blockquote>המשך זריעה אחרי ההעלאה (טורנטים לא נתמכים בבוט הזה).</blockquote>"""),
    "auth": ("התחברות", """㊂ <b>התחברות</b> » <code>-u</code> <code>-p</code>

<blockquote>לקישורים ישירים או אתרים שדורשים שם משתמש וסיסמה.
➲ <code>/cmd link -u user -p pass</code></blockquote>"""),
    "headers": ("כותרות", """㊂ <b>כותרות</b> » <code>-h</code>

<blockquote>הוספת כותרות מותאמות לקישור ישיר.
➲ <code>/cmd link -h Referer: https://site.com Cookie: a=b</code></blockquote>"""),
    "rcf": ("דגלי RClone", """㊂ <b>דגלי RClone</b> » <code>-rcf</code>

<blockquote>דגלים נוספים של rclone למשימה הזו, מופרדים ב-<code>|</code>
➲ <code>/cmd link -up rc -rcf --buffer-size:8M|--drive-starred-only</code></blockquote>
<i>מחליף את דגלי RClone מ-/us. כל הדגלים: <a href='https://rclone.org/flags/'>rclone.org/flags</a></i>"""),
    "drive": ("תיקיית דרייב", """㊂ <b>תיקיית דרייב</b> » <code>-id</code> <code>-index</code>

<blockquote>העלאה לתיקייה מסוימת בגוגל דרייב.
➲ <code>/cmd link -id folder_link</code>
➲ <code>/cmd link -id folder_id -index https://index.site/0:</code></blockquote>"""),
    "category": ("קטגוריה", """㊂ <b>קטגוריה</b> » <code>-c</code>

<blockquote>העלאה לקטגוריית דרייב לפי שם.
➲ <code>/cmd link -c Movies</code></blockquote>
<i>בלי זה, כשיש כמה קטגוריות מקבלים כפתורים.</i>"""),
    "screenshots": ("צילומי מסך", """㊂ <b>צילומי מסך</b> » <code>-ss</code>

<blockquote>שליחת צילומי מסך של כל סרטון יחד עם ההעלאה.
➲ <code>/cmd link -ss 6</code></blockquote>
<i>כדי לקבל תמיד, מגדירים ב-/us ← Leech.</i>"""),
    "thumb": ("תמונה ממוזערת", """㊂ <b>תמונה ממוזערת</b> » <code>-t</code>

<blockquote>תמונה ממוזערת אחרת רק למשימה הזו.
➲ <code>/cmd link -t https://site.com/image.jpg</code>
➲ <code>/cmd link -t https://t.me/channel/123</code> תמונה מטלגרם</blockquote>
<i>בלי זה משתמשים בתמונה מ-/us ובתמונה אוטומטית.</i>"""),
    "convert": ("המרת מדיה", """㊂ <b>המרת מדיה</b> » <code>-ca</code> <code>-cv</code>

<blockquote>➲ <code>/cmd link -cv mp4</code> כל הסרטונים ל-mp4
➲ <code>/cmd link -ca mp3</code> כל השמע ל-mp3
➲ <code>/cmd link -ca mp3 -cv mp4</code> שניהם
➲ <code>/cmd link -ca mp3 + flac ogg</code> רק flac ו-ogg ל-mp3
➲ <code>/cmd link -cv mkv - webm flv</code> כל הסרטונים ל-mkv חוץ מ-webm ו-flv</blockquote>
<i>סרטונים מומרים בלי קידוד מחדש כשאפשר, אז זה מהיר. הקבצים המקוריים מוחלפים.</i>"""),
    "extract_audio": ("חילוץ שמע", """㊂ <b>חילוץ שמע</b> » <code>-ea</code>

<blockquote>הוצאת השמע מכל סרטון והעלאת השמע בלבד.
➲ <code>/cmd link -ea</code> כ-mp3
➲ <code>/cmd link -ea m4a</code> כ-m4a (הכי מהיר, בדרך כלל בלי קידוד מחדש)
➲ <code>/cmd link -ea flac</code> גם <code>opus</code> <code>ogg</code> <code>wav</code></blockquote>
<i>סרטונים בלי שמע נשארים כמו שהם.</i>"""),
    "ffmpeg": ("פקודות FFmpeg", """㊂ <b>פקודות FFmpeg</b> » <code>-ff</code>

<blockquote>הרצת פקודת FFmpeg ששמרת ב-/us ← Universal ← FFmpeg Cmds.
➲ <code>/cmd link -ff tomp3</code>
בפקודה השמורה כותבים <code>mltb</code> כשם הקלט והפלט.
הקלט קובע על אילו קבצים היא רצה:
<code>mltb</code> כל הקבצים · <code>mltb.video</code> כל הסרטונים · <code>mltb.audio</code> כל השמע · <code>mltb.mkv</code> רק mkv
<code>tomp3: -i mltb.audio -c:a libmp3lame mltb.mp3</code>
➲ <code>/cmd link -ff tomp3 subs</code> הרצת יותר מאחת</blockquote>"""),
    "rclone_dl": ("מ-RClone", """㊂ <b>מ-RClone</b>

<blockquote>הורדה מהענן שלך כמו מקישור.
➲ <code>/cmd rcl</code> בחירת קובץ בכפתורים
➲ <code>/cmd remote:folder/file.mkv</code>
➲ <code>/cmd mrcc:remote:folder</code> עם rclone.conf שלך</blockquote>"""),
    "tg": ("קישורי טלגרם", """㊂ <b>קישורי טלגרם</b>

<blockquote>עונים על קובץ, או שולחים קישור להודעה:
➲ <code>/cmd https://t.me/channel/123</code> ציבורי
➲ <code>/cmd https://t.me/c/123456/78</code> פרטי
➲ <code>/cmd -i 5</code> עונים על הקובץ הראשון כדי לקחת 5 ברצף</blockquote>
<i>צ'אטים פרטיים דורשים את הסשן שלך (/us) או של הבוט.</i>"""),
    "yt_opt": ("אפשרויות YT-DLP", """㊂ <b>אפשרויות YT-DLP</b> » <code>-opt</code>

<blockquote>אפשרויות yt-dlp נוספות למשימה הזו, מופרדות ב-<code>|</code>
➲ <code>/cmd link -opt playliststart:^5|playlistend:^10</code>
➲ <code>/cmd link -opt writesubtitles:true|format:bv*+ba</code>
לפני מספרים מוסיפים <code>^</code>.</blockquote>
<i>אפשרויות קבועות שומרים ב-/us ← Universal. גם קוקיז.</i>"""),
    "clone_links": ("נתמכים", """㊂ <b>נתמכים</b>

<blockquote>➲ <code>/cmd gdrive_link</code>
➲ קישורי GDTot · Filepress · Filebee · Appdrive · GDFlix
➲ <code>/cmd remote:folder -up remote2:folder</code> מ-rclone ל-rclone</blockquote>"""),
    "clone_up": ("העלאה אל", """㊂ <b>העלאה אל</b> » <code>-up</code>

<blockquote>לנתיבי rclone, בחירת יעד ההעתקה.
➲ <code>/cmd remote:folder -up rcl</code> בחירה בכפתורים
➲ <code>/cmd remote:folder -up remote2:folder</code></blockquote>
<i>בלי זה משתמשים בנתיב RClone שלך.</i>"""),
}

_TAP = "<i>לחץ על ארגומנט כדי לראות איך משתמשים בו:</i>"
_MAIN = {
    "leech": f"""㊂ <b>Leech</b>

<blockquote>הורדת כל דבר והעלאה לטלגרם.
➲ <code>/cmd link</code>
➲ תגובה לקישור או קובץ עם <code>/cmd</code></blockquote>
<blockquote>קישורים ישירים · קבצי טלגרם · GDrive · RClone ועוד.
ההגדרות שלך מ-/us חלות: תמונה ממוזערת, כיתוב, מצב העברה, יעדים...</blockquote>
{_TAP}""",
    "mirror": f"""㊂ <b>Mirror</b>

<blockquote>הורדת כל דבר והעלאה ל-GDrive, RClone או DDL.
➲ <code>/cmd link</code>
➲ תגובה לקישור או קובץ עם <code>/cmd</code></blockquote>
<blockquote>קישורים ישירים · קבצי טלגרם · GDrive · RClone ועוד.
הקישורים מגיעים בהודעה כשזה מסתיים.</blockquote>
{_TAP}""",
    "qbleech": f"""㊂ <b>qBittorrent Leech</b>

<blockquote>טורנטים לא נתמכים בבוט הזה.</blockquote>""",
    "qbmirror": f"""㊂ <b>qBittorrent Mirror</b>

<blockquote>טורנטים לא נתמכים בבוט הזה.</blockquote>""",
    "ytleech": f"""㊂ <b>YT-DLP Leech</b>

<blockquote>הורדה מיוטיוב ומאלף אתרים והעלאה לטלגרם.
➲ <code>/cmd link</code>
את האיכות בוחרים בכפתורים.</blockquote>
{_TAP}""",
    "ytmirror": f"""㊂ <b>YT-DLP Mirror</b>

<blockquote>הורדה מיוטיוב ומאלף אתרים והעלאה ל-GDrive, RClone או DDL.
➲ <code>/cmd link</code>
את האיכות בוחרים בכפתורים.</blockquote>
{_TAP}""",
    "clone": f"""㊂ <b>Clone</b>

<blockquote>העתקת קבצים בין ענני אחסון בלי להוריד אותם.
➲ <code>/cmd link</code>
➲ תגובה לקישור עם <code>/cmd</code></blockquote>
{_TAP}""",
}
