# Light Hebrew layer: exact-phrase replacement on outgoing bot text.
_MAP = [
    (">Download<", ">מוריד<"), (">Upload<", ">מעלה<"), (">Clone<", ">משכפל<"),
    (">QueueDL<", ">בתור להורדה<"), (">QueueUp<", ">בתור להעלאה<"), (">Pause<", ">מושהה<"),
    (">Archive<", ">דוחס<"), (">Extract<", ">מחלץ<"), (">Split<", ">מפצל<"),
    (">CheckUp<", ">בודק<"), (">Seed<", ">זורע<"), (">Metadata<", ">מטא-דאטה<"),
    ("No Active Downloads!", "אין הורדות פעילות!"),
    ("Cancelled by user!", "בוטל על ידי המשתמש!"),
    ("Download Cancelled by User!", "ההורדה בוטלה על ידי המשתמש!"),
    ("Task has been cancelled.", "המשימה בוטלה."),
    ("Timed Out. Task has been cancelled!", "הזמן נגמר. המשימה בוטלה!"),
    ("Cancelling...", "מבטל..."),
    ("Checking Size Limit of link/file/folder/tasks...", "בודק מגבלת גודל..."),
    ("Bot Max Tasks limit exceeded.", "הבוט הגיע למגבלת המשימות."),
    ("Please wait for the completion of other tasks.", "המתן לסיום משימות אחרות."),
    ("Internal Error occurred", "אירעה שגיאה פנימית"),
    ("You Are not authorized user!", "אין לך הרשאה להשתמש בבוט."),
    ("You have exhausted all your Daily Leech Limit.", "ניצלת את מכסת ההורדות היומית."),
    ("You have exhausted all your Daily Mirror Limit.", "ניצלת את המכסה היומית."),
    ("You have exhausted all your Daily Task Limits.", "ניצלת את מכסת המשימות היומית."),
    ("Daily Leech Limit is", "המכסה היומית היא"),
    ("Leech limit is", "מגבלת הורדה:"),
    ("Direct limit is", "מגבלת הורדה ישירה:"),
    ("Google drive limit is", "מגבלת דרייב:"),
    ("Clone limit is", "מגבלת שכפול:"),
    ("Mega limit is", "מגבלת Mega:"),
    ("ERROR: Invalid URL", "שגיאה: קישור לא תקין"),
    ("ERROR: File not found!", "שגיאה: הקובץ לא נמצא"),
    ("ERROR: Something went wrong!", "שגיאה: משהו השתבש"),
    ("ERROR: Something went wrong", "שגיאה: משהו השתבש"),
    ("ERROR: Use ytdl cmds for Youtube links", "שגיאה: לקישורי יוטיוב השתמש בפקודת /ytdl"),
    ("ERROR: Direct Link not found", "שגיאה: לא נמצא קישור הורדה ישיר"),
    ("ERROR: Direct link not found", "שגיאה: לא נמצא קישור הורדה ישיר"),
    ("ERROR: Download link not found", "שגיאה: לא נמצא קישור הורדה"),
    ("ERROR: Can't extract the link", "שגיאה: אי אפשר לחלץ את הקישור"),
    ("ERROR: this host is not supported in this build", "שגיאה: האתר הזה לא נתמך בבוט הזה"),
    ("ERROR: Torrent is not supported in this build", "שגיאה: טורנטים לא נתמכים בבוט הזה"),
    ("ERROR:", "שגיאה:"),
    ("Aria2c Download Error:", "שגיאת הורדה (aria2):"),
    ("GDRIVE_ID not Provided!", "לא הוגדר GDRIVE_ID"),
    ("Google Drive ID validation failed!!", "אימות מזהה הדרייב נכשל"),
    ("No RClone Destination!", "לא הוגדר יעד RClone"),
    ("Wrong Rclone Upload Destination!", "יעד העלאת RClone שגוי"),
    ("FFmpeg Cmds are disabled by the Owner!", "פקודות FFmpeg מבוטלות על ידי הבעלים"),
    ("Cancel this task?", "לבטל את המשימה?"),
    ("Choose which of", "בחר איזו מהמשימות לבטל:"),
    (" Not Found.", " לא נמצא."),
    ("File not found or no longer available!", "הקובץ לא נמצא או שכבר לא זמין!"),
]


def he(text):
    if not isinstance(text, str):
        return text
    for a, b in _MAP:
        if a in text:
            text = text.replace(a, b)
    return text
