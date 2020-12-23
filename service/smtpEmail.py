import smtplib
import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
fromaddr = "ĐỊA CHỈ EMAIL CỦA BAN"
toaddr = "ĐỊA CHỈ NHẬN MAIL"
msg = MIMEMultipart()    
msg['From'] = fromaddr
msg['To'] = toaddr
msg['Subject'] = "TIÊU ĐỀ CỦA MAIL (SUBJECT)"
body = "NỘI DUNG MAIL"
try:
    msg.attach(MIMEText(body, 'plain'))
    filename = "ĐƯỜNG DẪN ĐẾN FILE ĐÍNH KÈM"
    attachment = open(filename, "rb")
    part = MIMEBase('application', 'octet-stream')
    part.set_payload((attachment).read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', "attachment; filename= %s" % filename)
    msg.attach(part)
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(fromaddr, "MẬT KHẨU ")
    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text)
    server.quit()
except Exception as e:
    print(str(e))