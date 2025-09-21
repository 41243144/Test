from django.core.management.base import BaseCommand
from apps.news.models import NewsCategory, NewsTag


class Command(BaseCommand):
    help = '測試新聞分類和標籤的自動 slug 產生功能'

    def handle(self, *args, **options):
        # 測試新聞分類
        self.stdout.write(self.style.SUCCESS('開始測試新聞分類自動 slug...'))
        
        categories = [
            {'name': '農業新聞', 'description': '關於農業的最新消息'},
            {'name': '技術創新', 'description': '農業技術創新資訊'},
            {'name': '市場行情', 'description': '農產品市場價格動態'},
            {'name': '政策法規', 'description': '農業相關政策法規'},
            {'name': 'Success Stories', 'description': '成功案例分享'},
        ]
        
        for cat_data in categories:
            category, created = NewsCategory.objects.get_or_create(
                name=cat_data['name'],
                defaults={
                    'description': cat_data['description'],
                    'color': '#007bff',
                    'is_active': True,
                }
            )
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'✓ 建立分類: {category.name} -> slug: {category.slug}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'- 分類已存在: {category.name} -> slug: {category.slug}')
                )
        
        # 測試新聞標籤
        self.stdout.write(self.style.SUCCESS('\n開始測試新聞標籤自動 slug...'))
        
        tags = [
            '有機農業',
            '智慧農業',
            '可持續發展',
            '農產品認證',
            '食品安全',
            'AI Technology',
            '區塊鏈應用',
        ]
        
        for tag_name in tags:
            tag, created = NewsTag.objects.get_or_create(
                name=tag_name,
                defaults={
                    'color': '#6c757d',
                    'is_active': True,
                }
            )
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'✓ 建立標籤: {tag.name} -> slug: {tag.slug}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'- 標籤已存在: {tag.name} -> slug: {tag.slug}')
                )
        
        self.stdout.write(self.style.SUCCESS('\n測試完成！'))
