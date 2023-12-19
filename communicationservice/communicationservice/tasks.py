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
        )
        
    except Exception as e:
        print("Exception occurred in sending mail:- "+str(e))
        
        

def SendOrderConfirmationMail(payload):
    print("+++++++++++++++++++Sending mail to user++++++++++++++++++++++++")
    try:
        send_mail(
                "Order Confirmation Karthik E-commerce",
                f"Your order of {payload['product']['name']} has been confirmed and will be delivered in 3-4 business days",
                settings.EMAIL_HOST_USER,
                [payload["email"],],
        )
    except Exception as e:
        print("Exception occurred in sending mail:- "+str(e))