import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import mailer
import socket

class notifications:
        def __init__(self, notifier = '', notification_type = '', method = ''):
                if notification_type != '' and method != '':
                        self.notifyMe = True
                        self.notifier = notifier
                        self.notification_type = notification_type
                        self.method = method
                else:
                        self.notifyMe = False
                        self.notifier = ''
                        self.notification_type = ''
                        self.method = ''
        
        def notify(self, url, actual_output):
                if self.notifyMe:
                        if self.notification_type == 'email':
                                self.sendMail(url, actual_output)
                        elif self.notification_type == 'slack':
                                self.sendSlackNotification()
                        else:
                                print("error while trying to notify using: " + self.notification_type + " with: " + self.method) 

        def sendSlackNotification(self):
                # prototype function for sending slack notifications
                return

        def sendMail(self, url, status):
                # early return in case the mailer is not setup
                if not self.notifier.is_set():
                        return
                
                # Email details
                sender_email = self.notifier.address
                receiver_email = self.method

                # Create the email
                subject = "Subject: Your service is down!"
                body = "The Service under: " + url + " is currently unavailable!\n\nthe returned http-status-code is: " +  str(status) + ")"

                # Create MIME object
                message = MIMEMultipart()
                message["From"] = sender_email
                message["To"] = receiver_email
                message["Subject"] = subject

                # Attach the email body
                message.attach(MIMEText(body, "plain"))

                try:
                        # Connect to the mail server
                        with smtplib.SMTP(self.notifier.server, self.notifier.port, timeout=30) as server:
                                server.starttls()  # Secure the connection
                                server.login(self.notifier.user, self.notifier.password)  # Login to your email
                                server.sendmail(sender_email, receiver_email, message.as_string())
                except (smtplib.SMTPException, socket.timeout) as e:
                        print(f"Failed to send email: {e}")

