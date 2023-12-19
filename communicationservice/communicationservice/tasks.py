from django.core.mail import send_mail
from django.conf import settings


# simple mail sending logic
def SendSignUpMail(payload):
    print("+++++++++++++++++++Sending mail to user++++++++++++++++++++++++")
    try:
        
        send_mail(
                "SignUP Karthik E-commerce",
                "Welcome to the Karthik E-commerce here is your signup bonus of 1000 rupess coupon code: KARTHIK1000",
                settings.EMAIL_HOST_USER,
                [payload["email"],],
                fail_silently=False,
        )
        
    except Exception as e:
        print("Exception occurred in sending mail:- "+str(e))