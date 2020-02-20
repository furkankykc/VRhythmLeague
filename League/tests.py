from django.conf import settings
from django.core.mail import get_connection, send_mail, EmailMessage

#TODO: Insert clever settings mechanism
settings.configure()



send_mail('mail subject', 'body content',settings.EMAIL_HOST_USER,['furkanfbr@gmail.com'], fail_silently=False)