import pyotp
from datetime import datetime, timedelta
from django.core.mail import send_mail
from django.conf import settings

def send_otp(request, email):
    totp = pyotp.TOTP(pyotp.random_base32(), interval=300)
    otp = totp.now()
    request.session['otp_secret_key'] = totp.secret
    valid_until = datetime.now() + timedelta(minutes=5)
    request.session['otp_valid_until'] = str(valid_until)

    print(f'Your one time password is {otp}')
    subject = 'Django App OTP Verification'
    message = f'Your OTP validation code is: {otp}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list)