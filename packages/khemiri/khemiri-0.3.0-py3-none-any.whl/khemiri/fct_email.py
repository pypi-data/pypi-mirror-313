import os, logging, traceback, smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import formatdate
from email import encoders

# __all__ = [
#     name for name, obj in globals().items()
#     if callable(obj) or isinstance(obj, type)  # Include functions and classes
# ]

class EmailSender:
    def __init__(self, gmail_user, gmail_pass):
        self.gmail_user = gmail_user
        self.gmail_pass = gmail_pass

    def send_email(self, send_to=[], subject='', body='', file_name='', directory=''):
        for recipient in send_to:
            try:
                # Create a multipart message
                msg = MIMEMultipart()
                msg['Subject'] = subject
                msg['From'] = self.gmail_user
                msg['To'] = recipient
                msg['Date'] = formatdate(localtime=True)

                # Attach the email body
                msg.attach(MIMEText(body, 'plain'))

                # Attach the file
                if file_name:
                    file_path = os.path.join(directory, file_name)
                    if os.path.isfile(file_path):
                        with open(file_path, 'rb') as file:
                            part = MIMEBase('application', 'octet-stream')
                            part.set_payload(file.read())
                            encoders.encode_base64(part)
                            part.add_header(
                                'Content-Disposition',
                                f'attachment; filename={os.path.basename(file_path)}',
                            )
                            msg.attach(part)
                    else:
                        logging.error(f"File '{file_path}' not found.")
                        return

                # Send the email
                with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
                    smtp_server.ehlo()
                    smtp_server.login(self.gmail_user, self.gmail_pass)
                    smtp_server.sendmail(self.gmail_user, recipient, msg.as_string())

                logging.info(f'Email sent to {recipient}')

            except:
                logging.error(f'Failed to send email: {traceback.format_exc()}')

# Example usage:
# send_to = ["recipient@example.com"]
# email_sender = EmailSender(gmail_user='email@gmail.com', gmail_pass='your_password')
# email_sender.send_email(
#     send_to=send_to,
#     subject='Email subject text',
#     body='Email body text',
#     file_name=f'results.xlsx',
#     directory='.'
# )
