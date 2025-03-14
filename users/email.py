from django.core.mail import send_mail

from ytasks import settings


class Email:
    def __init__(self, email, title, description):
        self.email = email
        self.title = title
        self.description = description

    def send(self):
        send_mail(
            self.title,
            self.description,
            settings.EMAIL_HOST_USER,
            [self.email],
            fail_silently=False,
        )

    class Builder:
        email = ""
        title = ""
        description = ""

        def setEmail(self, email):
            self.email = email
            return self

        def setTitle(self, title):
            self.title = title
            return self

        def addDescriptionLine(self, line):
            self.description += line + "\n"
            return self

        def build(self):
            return Email(self.email, self.title, self.description)
