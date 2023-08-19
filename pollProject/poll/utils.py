from django.core.mail import EmailMessage
from django.core.mail import EmailMultiAlternatives
from django.conf import settings

class Utils:
    @staticmethod
    def send_message(details):
        subject = details['subject']
        from_email = settings.EMAIL_HOST_USER
        to = details['to_email']
        reply_to = settings.EMAIL_HOST_USER
        text_content = details['text_content']
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to], [reply_to])
        msg.send()
