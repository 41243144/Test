import os
from django.conf import settings
from django.apps import apps
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver
from django.db.models.signals import post_migrate
from .models import User, Profile
from django.contrib.auth.models import Permission, Group
from django.db.models.signals import m2m_changed
from allauth.account.utils import send_email_confirmation


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_profile_for_new_user(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(pre_save, sender=Profile)
def delete_old_portrait_on_change(sender, instance, **kwargs):
    if not instance.pk:
        return

    try:
        old = sender.objects.get(pk=instance.pk)
    except sender.DoesNotExist:
        return

    old_file = old.portrait
    new_file = instance.portrait

    if old_file and old_file.name and old_file != new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)

@receiver(post_delete, sender=Profile)
def delete_portrait_on_profile_delete(sender, instance, **kwargs):
    portrait = instance.portrait
    if portrait and portrait.name:
        if os.path.isfile(portrait.path):
            os.remove(portrait.path)