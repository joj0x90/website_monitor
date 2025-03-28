import smtplib
import requests
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import socket
from dotenv import load_dotenv
import os

import notifier
import config

class notifications:
        def __init__(self, notifier = '', notification_type = '', method = ''):
                # Load the .env file
                load_dotenv()

                if notification_type != '':
                        self.notifyMe = True
                        self.notifier = notifier
                        self.notification_type = notification_type
                        self.method = method
                else:
                        self.notifyMe = False
                        self.notifier = ''
                        self.notification_type = ''
                        self.method = ''

        def print(self):
                if config.GLOBAL_VERBOSE:
                        print("+" * 30)
                        print(f"notifyMe: {self.notifyMe}")
                        print(f"Notifier: {self.notifier}")
                        print(f"notification_type: {self.notification_type}")
                        print(f"method: {self.method}")
                        print("+" * 30)
        
        def notify(self, url, actual_output):
                if self.notifyMe:
                        if self.notification_type == 'email':
                                self.sendMail(url, actual_output)
                        elif self.notification_type == 'slack':
                                self.sendSlackNotification(url, actual_output)
                        else:
                                if config.GLOBAL_VERBOSE:
                                        print("error while trying to notify using: " + self.notification_type + " with: " + self.method) 

        def sendSlackNotification(self, url, status):
                App_name = os.getenv("APP_NAME", "Website-monitor")
                App_version = os.getenv("APP_VERSION", "0.1")
                slack_webhook = os.getenv("SLACK_WEBHOOK", "")

                slack_data = {
                        "text": "[" + App_name + " v" + App_version + "] The Service at " + url + " has an unexpected http-status: " + str(status)
                }

                # Send the POST request
                response = requests.post(
                        slack_webhook, json=slack_data,
                        headers={'Content-Type': 'application/json'}
                )

                # Check the response
                if config.GLOBAL_VERBOSE:
                        if response.status_code == 200:
                                print("Slack Notification sent successfully!")
                        else:
                                print(f"Failed to send notification: {response.status_code}, {response.text}")
        
        def is_ssl_port(self, smtp_server, port):
                try:
                        # Attempt to establish an SSL connection
                        with smtplib.SMTP_SSL(smtp_server, port, timeout=10) as server:
                                server.noop()  # Send a NOOP command to test the connection
                        return True  # Connection successful
                except (smtplib.SMTPException, ConnectionRefusedError, TimeoutError):
                        return False  # Connection failed
                except Exception as e:
                        return False    # general error


        def sendMail(self, url, status):
                # early return in case the mailer is not setup
                if not self.notifier.is_set():
                        return
                
                # Email details
                sender_email = self.notifier.address
                receiver_email = self.method

                # Create the email
                App_name = os.getenv("APP_NAME", "Website-monitor")
                App_version = os.getenv("APP_VERSION", "0.1")

                subject = "[" + App_name + "]: Your service is down!"
                body = "The Service under: " + url + " is currently unavailable!\nthe returned http-status-code is: " +  str(status) + "\n\n"
                body += "This Service was provided by {App_name} v{App_version}"

                # Create MIME object
                message = MIMEMultipart()
                message["From"] = sender_email
                message["To"] = receiver_email
                message["Subject"] = subject

                # Attach the email body
                message.attach(MIMEText(body, "plain"))

                try:
                        smtp_server = self.notifier.server
                        smtp_port = self.notifier.port
                        if self.is_ssl_port(smtp_server, smtp_port):
                                # Connect to the mail server via ssl
                                with smtplib.SMTP_SSL(smtp_server, smtp_port, timeout=30) as server:
                                        server.login(self.notifier.user, self.notifier.password)
                                        server.sendmail(sender_email, receiver_email, message.as_string())
                                        if config.GLOBAL_VERBOSE:
                                                print("ssl encrypted email notification send to: " + receiver_email)
                        else:
                                with smtplib.SMTP(smtp_server, smtp_port) as server:
                                        server.starttls()
                                        server.login(self.notifier.user, self.notifier.password)
                                        server.sendmail(sender_email, receiver_email, message.as_string())
                                        if config.GLOBAL_VERBOSE:
                                                print("email notification send to: " + receiver_email)
                except (smtplib.SMTPException, socket.timeout) as e:
                        if config.GLOBAL_VERBOSE:
                                print(f"Failed to send email: {e}")

