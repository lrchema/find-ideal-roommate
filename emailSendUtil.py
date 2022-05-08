import yagmail
from . import dbconn

def sendEmail(emailBody, toUserid):
    conn = dbconn()
    conn.reconnect()
    cur = conn.cursor()
    cur.execute("select email from user_info where userid=%s", (toUserid,))
    to_address = cur.fetchone()

    user = 'idealroommate045@gmail.com'
    app_password ='ooeykmposzgmryxp'

    subject = 'A potential roommate!'
    content = [emailBody]

    with yagmail.SMTP(user, app_password) as yag:
        yag.send(to_address, subject, content)
    print('Sent email successfully')