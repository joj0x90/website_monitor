class notifier:
        def __init__(self, address, user, password, server, port, webhook):
                self.address = address
                self.user = user
                self.password = password
                self.server = server
                self.port = port
                self.webhook = webhook

        # there must either be a config for emailing or for sending slack notifications
        def is_set(self):
                return (self.address != '' and self.user != '' and self.password != '' and self.server != '' and self.port != '') or self.webhook != ''