import smtplib
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class Email:
    def __init__(self, smtp_server, smtp_port, smtp_user, smtp_password):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.smtp_user = smtp_user
        self.smtp_password = smtp_password

    def create_header(self, sender, sender_name, to, subject) -> None:
        self.sender = sender
        self.sender_name = sender_name
        self.to = to
        self.subject = subject
        self.body = ""

        self.msg = MIMEMultipart()
        self.msg['From'] = f'{self.sender_name} <{self.sender}>'
        self.msg['To'] = self.to
        self.msg['Subject'] = self.subject

    def append_line(self, message):
        self.body += message + '\n'

    def add_attachment(self, file_path, subtype='octet-stream'):
        file_name = file_path[file_path.rindex('/')+1:]
        with open(file_path, 'rb') as file:
            attachment = MIMEApplication(_data=file.read(), _subtype=subtype)
            attachment.add_header(
                'content-disposition',
                'attachment',
                filename=file_name)
            self.msg.attach(attachment)

    def send(self):
        self.msg.attach(MIMEText(self.body, 'plain'))
        server = smtplib.SMTP(self.smtp_server, self.smtp_port)
        server.starttls()
        server.login(self.smtp_user, self.smtp_password)
        server.sendmail(self.sender, self.to, self.msg.as_string())
        server.quit()
