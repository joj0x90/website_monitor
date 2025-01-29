import json

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
    with open(json_file, 'r') as file:
        data = json.load(file)

    sender_data = data.get("sender_mail", {})
    mail_sender_obj = mailer.mailer(
        address=sender_data.get("mail_address", ""),
        user=sender_data.get("mail_user", ""),
        password=sender_data.get("mail_pass", ""),
        server=sender_data.get("mail_server", ""),
        port=sender_data.get("mail_port", 0),
    )

    return mail_sender_obj