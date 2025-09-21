from django.core.management.base import BaseCommand
from apps.news.models import NewsCategory, NewsTag, NewsPost


class Command(BaseCommand):
    help = '修正所有新聞相關模型的 slug，將中文轉換為英文'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='僅顯示將要進行的更改，不實際執行',
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        
        if dry_run:
            self.stdout.write(self.style.WARNING('這是預覽模式，不會實際更改數據庫'))
        
        # 修正新聞分類 slug
        self.stdout.write(self.style.SUCCESS('\n=== 修正新聞分類 slug ==='))
        categories = NewsCategory.objects.all()
        
        for category in categories:
            old_slug = category.slug
            # 重新生成 slug
            new_slug = category.generate_slug_from_chinese(category.name)
            
            if old_slug != new_slug:
                self.stdout.write(f'分類: {category.name}')
                self.stdout.write(f'  舊 slug: {old_slug}')
                self.stdout.write(f'  新 slug: {new_slug}')
                
                if not dry_run:
                    category.slug = new_slug
                    category.save()
                    self.stdout.write(self.style.SUCCESS('  ✓ 已更新'))
                else:
                    self.stdout.write(self.style.WARNING('  (預覽模式)'))
            else:
                self.stdout.write(f'分類: {category.name} - slug 正確: {old_slug}')
        
        # 修正新聞標籤 slug
        self.stdout.write(self.style.SUCCESS('\n=== 修正新聞標籤 slug ==='))
        tags = NewsTag.objects.all()
        
        for tag in tags:
            old_slug = tag.slug
            # 重新生成 slug
            new_slug = tag.generate_slug_from_chinese(tag.name)
            
            if old_slug != new_slug:
                self.stdout.write(f'標籤: {tag.name}')
                self.stdout.write(f'  舊 slug: {old_slug}')
                self.stdout.write(f'  新 slug: {new_slug}')
                
                if not dry_run:
                    tag.slug = new_slug
                    tag.save()
                    self.stdout.write(self.style.SUCCESS('  ✓ 已更新'))
                else:
                    self.stdout.write(self.style.WARNING('  (預覽模式)'))
            else:
                self.stdout.write(f'標籤: {tag.name} - slug 正確: {old_slug}')
        
        # 修正新聞文章 slug
        self.stdout.write(self.style.SUCCESS('\n=== 修正新聞文章 slug ==='))
        posts = NewsPost.objects.all()
        
        for post in posts:
            old_slug = post.slug
            # 重新生成 slug
            new_slug = post.generate_slug_from_chinese(post.title)
            
            if old_slug != new_slug:
                self.stdout.write(f'文章: {post.title}')
                self.stdout.write(f'  舊 slug: {old_slug}')
                self.stdout.write(f'  新 slug: {new_slug}')
                
                if not dry_run:
                    post.slug = new_slug
                    post.save()
                    self.stdout.write(self.style.SUCCESS('  ✓ 已更新'))
                else:
                    self.stdout.write(self.style.WARNING('  (預覽模式)'))
            else:
                self.stdout.write(f'文章: {post.title} - slug 正確: {old_slug}')
        
        if dry_run:
            self.stdout.write(self.style.WARNING('\n這是預覽模式。要實際執行更改，請運行:'))
            self.stdout.write(self.style.WARNING('python manage.py fix_slugs'))
        else:
            self.stdout.write(self.style.SUCCESS('\n所有 slug 修正完成！'))
