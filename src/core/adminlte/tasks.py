from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth import get_user_model
from django.conf import settings
from src.cms.models import Mailing
import os

User = get_user_model()


@shared_task
def send_mass_mail_task(mailing_id, user_ids=None):
    try:
        mailing = Mailing.objects.get(pk=mailing_id)

        if user_ids:
            users = User.objects.filter(id__in=user_ids)
        else:
            users = User.objects.exclude(email='').exclude(email__isnull=True)

        emails = list(users.values_list('email', flat=True))

        if not emails:
            return "No recipients found"

        file_path = os.path.join(settings.MEDIA_ROOT, mailing.template_file.name)
        with open(file_path, 'r', encoding='utf-8') as f:
            html_content = f.read()


        msg = EmailMultiAlternatives(
            subject=mailing.subject,
            body="",
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[],
            bcc=emails
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send()

        return f"Sent emails to {len(emails)} users"

    except Mailing.DoesNotExist:
        return "Mailing template not found"