import json, os
from dotenv import load_dotenv

import target
import mailer
import notification

def parse(file_path):
        mailer = parse_mail_sender(file_path)

        with open(file_path, 'r') as file:
                data = json.load(file)

                targets = []
                # iterate over json structure 
                for entry in data['targets']:
                        # Create the host object
                        url = entry['url']
                        expected = entry.get('status', 200)

                        host_obj = target.host(url, expected)

                        # Create notifications object
                        notification_type = entry.get('notification-type', '')
                        method = entry.get('method', '')

                        notification_obj = notification.notifications(mailer, notification_type, method)

                        # Create the target object
                        target_obj = target.target(host_obj, notification_obj)

                        # Add the target object to the list
                        targets.append(target_obj)

                return targets

def parse_mail_sender(json_file):
        # Load the .env file
        load_dotenv()

        mail_sender_obj = mailer.mailer(
                address=os.getenv("MAIL_ADDRESS", ""),
                user=os.getenv("MAIL_USER", ""),
                password=os.getenv("MAIL_PASSWORD", ""),
                server=os.getenv("MAIL_SERVER", ""),
                port=os.getenv("SMTP_PORT", 0),
        )

        return mail_sender_obj