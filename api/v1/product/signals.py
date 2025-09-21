import os
from django.conf import settings
from django.apps import apps
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver
from django.db.models.signals import post_migrate
from .models import Product
from django.contrib.auth.models import Permission, Group
from django.db.models.signals import m2m_changed
from allauth.account.utils import send_email_confirmation

@receiver(pre_save, sender=Product)
def delete_old_image_on_change(sender, instance, **kwargs):
    if not instance.pk:
        return

    try:
        old = sender.objects.get(pk=instance.pk)
    except sender.DoesNotExist:
        return

    old_file = old.image
    new_file = instance.image

    if old_file and old_file.name and old_file != new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)

@receiver(post_delete, sender=Product)
def delete_image_on_Product_delete(sender, instance, **kwargs):
    image = instance.image
    if image and image.name:
        if os.path.isfile(image.path):
            os.remove(image.path)