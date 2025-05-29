import africastalking
from django.conf import settings

africastalking.initialize(
    username=settings.AFRICASTALKING_USERNAME,
    api_key=settings.AFRICASTALKING_API_KEY
)

sms = africastalking.SMS


def send_sms(to_number, message):
    try:
        print('Reached sending fnc')
        res = sms.send(message, [to_number])
        print(res)
        return res
    except Exception as e:
        print(f"Failed to send the sms {e}")

        return None
