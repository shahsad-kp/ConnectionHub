# Generated by Django 4.1.13 on 2024-10-24 02:33

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='OtpVerification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=50)),
                ('email', models.EmailField(blank=True, max_length=254)),
                ('phone_number', models.CharField(blank=True, max_length=15)),
                ('otp', models.CharField(blank=True, max_length=6)),
                ('type', models.CharField(choices=[('email', 'Email'), ('phone', 'Phone')], max_length=10)),
                ('verified', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
