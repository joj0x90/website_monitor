class mailer:
        def __init__(self, address, user, password, server, port):
                self.address = address
                self.user = user
                self.password = password
                self.server = server
                self.port = port

        def is_set(self):
                return self.address != '' and self.user != '' and self.password != '' and self.server != '' and self.port != ''