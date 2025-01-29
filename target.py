import requests

import notification

class host:
        def __init__(self, url, expected_status):
                self.url = url
                self.expected_status = expected_status

class target:
        def __init__(self, host, notification):
                self.host = host
                self.notification = notification
                self.already_notified = False

        def check_status(self):
                try:
                        response = requests.get(self.host.url)
                        return [(response.status_code == self.host.expected_status), response.status_code]
                except requests.exceptions.RequestException:
                        return [False, None]

        def print_target(self):
                print("-" * 30)
                print(f"Host: {self.host.url}")
                print(f"Notification Type: {self.notification.notification_type}")
                print(f"Method: {self.notification.method}")
                print(f"Expected Status: {self.host.expected_status}")
                print("-" * 30)
