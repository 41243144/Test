from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from django.contrib.auth.models import Group
from .models import Vendor

@receiver(post_save, sender=Vendor)
def add_user_to_groups(sender, instance, created, **kwargs):
    if created:
        groups = Group.objects.filter(name__in=['Editors', 'Moderators'])
        instance.user.groups.add(*groups)

@receiver(pre_delete, sender=Vendor)
def remove_user_from_groups(sender, instance, **kwargs):
    groups = Group.objects.filter(name__in=['Editors', 'Moderators'])
    instance.user.groups.remove(*groups)
