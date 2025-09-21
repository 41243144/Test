from django.apps import AppConfig
from django.db.models.signals import post_migrate


class ProductConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api.v1.product'

    def ready(self):
        import api.v1.product.signals
        # 在 migration 完成後呼叫 assign_group_permissions
        post_migrate.connect(assign_group_permissions)

def assign_group_permissions(sender, **kwargs):
    from django.contrib.auth.models import Group, Permission
    from django.contrib.contenttypes.models import ContentType
    from .models import Product

    # 取得 Product 這個 model 對應的 ContentType
    ct = ContentType.objects.get_for_model(Product)

    # 撈出 add/change/delete 這三種 permission
    perms = Permission.objects.filter(
        content_type=ct,
        codename__in=[
            'add_product',
            'change_product',
            'delete_product',
            'view_product'
        ]
    )

    # 要指派的群組清單
    group_names = ['Editors', 'Moderators']

    for name in group_names:
        group, created = Group.objects.get_or_create(name=name)
        # 把這些 permission 全部指派給群組
        group.permissions.add(*perms)
        group.save()