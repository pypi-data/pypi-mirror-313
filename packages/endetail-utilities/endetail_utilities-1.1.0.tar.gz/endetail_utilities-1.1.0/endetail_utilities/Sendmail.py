import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os


class SendMail:
    def __init__(self, smtp_server, port, username, password):
        self.smtp_server = smtp_server
        self.port = port
        self.username = username
        self.password = password
        self.use_ssl = False
        self.use_tls = False

        if port == 465:
            self.use_ssl = True
            self.use_tls = False
        elif port == 587:
            self.use_ssl = False
            self.use_tls = True
        elif port == 25:
            self.use_ssl = False
            self.use_tls = False
        else:
            raise ValueError("Unsupported port. Use 465 for SSL, 587 for TLS, or 25 for no security.")


    def send(self, to_email, subject, body, attachment_path=None, reply_to=None, from_email=None):
        # Vytvoření zprávy
        msg = MIMEMultipart()
        msg['From'] = from_email if from_email else self.username
        msg['To'] = to_email
        msg['Subject'] = subject

        if reply_to:
            msg.add_header('Reply-To', reply_to)

        msg.attach(MIMEText(body, 'plain'))

        # Přidání přílohy, pokud je poskytnuta
        if attachment_path and os.path.isfile(attachment_path):
            with open(attachment_path, 'rb') as attachment:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(attachment.read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', f'attachment; filename={os.path.basename(attachment_path)}')
                msg.attach(part)

        if self.use_ssl:
            with smtplib.SMTP_SSL(self.smtp_server, self.port) as server:
                server.login(self.username, self.password)
                server.sendmail(from_email if from_email else self.username, to_email, msg.as_string())
        else:
            with smtplib.SMTP(self.smtp_server, self.port) as server:
                if self.use_tls:
                    server.starttls()  # Přepnutí na TLS
                server.login(self.username, self.password)
                server.sendmail(from_email if from_email else self.username, to_email, msg.as_string())


        # Připojení k SMTP serveru
        if self.use_ssl:
            with smtplib.SMTP_SSL(self.smtp_server, self.port) as server:
                server.login(self.username, self.password)
                server.sendmail(from_email if from_email else self.username, to_email, msg.as_string())
        else:
            with smtplib.SMTP(self.smtp_server, self.port) as server:
                server.starttls()  # Přepnutí na TLS
                server.login(self.username, self.password)
                server.sendmail(from_email if from_email else self.username, to_email, msg.as_string())


