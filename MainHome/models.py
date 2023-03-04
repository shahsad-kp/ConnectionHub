from django.core.mail import EmailMessage

from django.db import models
from datetime import datetime, timedelta

from django.utils import timezone
from pyotp import TOTP
from twilio.rest import Client

from ConnectionHub.settings import env
from MainUsers.models import User


class OtpVerification(models.Model):
    username = models.CharField(max_length=50)
    email = models.EmailField(blank=True)
    phone_number = models.CharField(max_length=15, blank=True)
    otp = models.CharField(max_length=6, blank=True)
    type = models.CharField(max_length=10, choices=(('email', 'Email'), ('phone', 'Phone')))
    verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(default=timezone.now() + timedelta(minutes=5))

    def __str__(self):
        return f"OTP of {self.username}"

    def is_valid(self):
        return self.expires_at > datetime.now()

    def generate_otp(self):
        self.otp = TOTP(env('OTP_SECRET_KEY')).now()
        self.save()

    def send_otp(self):
        if not self.otp:
            self.generate_otp()
        subject = 'OTP Validation of ConnectionHub'
        body = f'Dear User, use this One Time Password ({self.otp}) to verify your {self.type}' \
               ' This OTP will be valid for the next 5 mins.'
        if self.type == 'email':
            message = EmailMessage(
                subject=subject,
                body=body,
                to=[self.email],
            )
            message.send()
        else:
            TWILIO_ACCOUNT_SID = env('TWILIO_ACCOUNT_SID')
            TWILIO_AUTH_TOKEN = env('TWILIO_AUTH_TOKEN')
            client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
            verification = client.verify.v2.services(TWILIO_ACCOUNT_SID) \
                .verifications \
                .create(to=self.phone_number, channel="sms")

    def verify_otp(self, otp):
        current_date = timezone.now()
        if self.expires_at > current_date:
            self.verified = True
            self.save()
            return True
        return False
