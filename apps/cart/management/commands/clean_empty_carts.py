from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from apps.cart.models import Cart


class Command(BaseCommand):
    help = '清理超過指定天數的空購物車'

    def add_arguments(self, parser):
        parser.add_argument(
            '--days',
            type=int,
            default=30,
            help='清理超過多少天的空購物車（默認 30 天）'
        )

    def handle(self, *args, **options):
        days = options['days']
        cutoff_date = timezone.now() - timedelta(days=days)
        
        # 查找空的且超過指定天數的購物車
        empty_carts = Cart.objects.filter(
            updated_at__lt=cutoff_date,
            items__isnull=True
        ).distinct()
        
        count = empty_carts.count()
        
        if count > 0:
            empty_carts.delete()
            self.stdout.write(
                self.style.SUCCESS(f'成功清理了 {count} 個空購物車')
            )
        else:
            self.stdout.write(
                self.style.WARNING('沒有找到需要清理的空購物車')
            )
