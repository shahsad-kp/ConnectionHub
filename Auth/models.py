from datetime import timedelta

from django.core.mail import EmailMessage
from django.db import models
from django.template.loader import render_to_string
from django.utils import timezone
from pyotp import TOTP
from twilio.rest import Client

from ConnectionHub.settings import env


class OtpVerification(models.Model):
    username = models.CharField(max_length=50)
    email = models.EmailField(blank=True)
    phone_number = models.CharField(max_length=15, blank=True)
    otp = models.CharField(max_length=6, blank=True)
    type = models.CharField(max_length=10, choices=(('email', 'Email'), ('phone', 'Phone')))
    verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"OTP of {self.username}"

    def generate_otp(self):
        self.otp = TOTP(env('OTP_SECRET_KEY')).now()
        self.save()

    def send_otp(self):
        if not self.otp:
            self.generate_otp()
        subject = 'OTP Validation of ConnectionHub'
        html_message = render_to_string(
            'otp-email.html',
            {
                'otp': self.otp,
                'name': self.username
            }
        )
        if self.type == 'email':
            message = EmailMessage(
                subject=subject,
                body=html_message,
                to=[self.email],
            )
            message.content_subtype = 'html'
            message.send()
        else:
            TWILIO_ACCOUNT_SID = env('TWILIO_ACCOUNT_SID')
            TWILIO_AUTH_TOKEN = env('TWILIO_AUTH_TOKEN')
            client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
            verification = client.verify.v2.services(TWILIO_ACCOUNT_SID) \
                .verifications \
                .create(to=self.phone_number, channel="sms")

    def verify_otp(self):
        current_date = timezone.now()
        if (self.created_at + timedelta(minutes=5)) > current_date:
            self.verified = True
            self.save()
            return True
        return False
