
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
class SmtpEmail:
    def __init__(self,emailAddress,password):
        self.emailAddress=emailAddress
        self.password=password
    def sendEmail(self,toEmail,subject,message):
        try:
            msg = MIMEMultipart()
            msg['From'] = self.emailAddress
            msg['To'] = toEmail
            msg['Subject'] = subject
            msg.attach(MIMEText(message, 'plain'))
            server = smtplib.SMTP('smtp.gmail.com: 587')
            server.starttls()
            server.login(msg['From'], self.password)
            server.sendmail(msg['From'], msg['To'], msg.as_string())
            server.quit()
            print("successfully sent email to %s:" % (msg['To']))
            return True
        except:
            return False