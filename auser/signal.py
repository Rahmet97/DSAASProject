from django.contrib.sites.models import Site
from django.core.mail import EmailMessage
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from auser.models import RecommendUserEmail, InviteUserEmail


@receiver(post_save, sender=RecommendUserEmail)
def recommend_user_email_for_reg(sender, instance, created, **kwargs):
    if created and instance.is_active:
        mail_subject = 'Invite register'
        message = render_to_string('user/recommend_user_email.html', {
            'user': instance,
            'domain': Site.objects.get_current().domain,
            'uid': urlsafe_base64_encode(force_bytes(instance.pk)),
            # is invite by our admin (Digital saas)?
            'iiboa': urlsafe_base64_encode(force_bytes(instance.is_invite_by_our_admin)),
            'token': instance.token,
        })
        to_email = instance.email
        email = EmailMessage(mail_subject, message, to=[to_email])
        email.send()


@receiver(post_save, sender=InviteUserEmail)
def invite_user_email(sender, instance, created, **kwargs):
    if created and instance.is_active:
        mail_subject = 'Invite register for employee'
        message = render_to_string('user/recommend_user_email.html', {
            'user': instance,
            'domain': Site.objects.get_current().domain,
            'token': instance.token,
            'uid': urlsafe_base64_encode(force_bytes(instance.pk)),
            # is invite by our admin (Digital saas)?
            'iiboa': urlsafe_base64_encode(force_bytes(instance.is_invite_by_our_admin)),
        })
        to_email = instance.email
        email = EmailMessage(mail_subject, message, to=[to_email])
        email.send()
