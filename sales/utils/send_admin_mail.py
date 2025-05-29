from django.core.mail import send_mail
from django.conf import settings

def send_alert_email(customer, product, user):
    try:
        subject = 'Stock Placed  Alert'
        message = f'Be notified that {user} placed order for product {product} to customer {customer} '
        from_email = settings.EMAIL_HOST_USER
        recipient_list = ['agikedwin73@gmail.com']

        send_mail(subject, message, from_email, recipient_list)
    except Exception as e:
        print(f'Some email sending exceptions {e}')