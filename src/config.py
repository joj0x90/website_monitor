import json, os
from dotenv import load_dotenv

import target
import notifier
import notification

def parse(file_path):
        notifier = parse_notifier()

        with open(file_path, 'r') as file:
                data = json.load(file)

                wait_time = 300
                if 'refresh' in data:
                        wait_time = data['refresh']                       

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

                        notification_obj = notification.notifications(notifier, notification_type, method)

                        # Create target object
                        target_obj = target.target(host_obj, notification_obj)
                        targets.append(target_obj)

                return [wait_time, targets]

def parse_notifier():
        # Load the app config from the .env file
        load_dotenv()

        mail_sender_obj = notifier.notifier(
                address=os.getenv("MAIL_ADDRESS", ""),
                user=os.getenv("MAIL_USER", ""),
                password=os.getenv("MAIL_PASSWORD", ""),
                server=os.getenv("MAIL_SERVER", ""),
                port=os.getenv("SMTP_PORT", 0),
                webhook=os.getenv("SLACK_WEBHOOK", "")
        )

        return mail_sender_obj