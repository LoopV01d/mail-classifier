class MailMessage:
    def __init__(self, name, topic, sender, message):
        self.name = name
        self.topic = topic
        self.sender = sender
        self.message = message

    def get_full_mail_text(self):
         return f"{self.topic} {self.message}".lower()