# home/signals.py
from django.conf import settings
from django.db import transaction

def ensure_homepage(sender, **kwargs):
    """
    在 home app 的 migrations 跑完後觸發：
    - 若尚未有 HomePage：在 Root 下建立並發佈
    - 若 Root 下已有 slug='home'：若是 HomePage 直接沿用；若不是則改名讓出 slug
    - 建立或更新 Site 設定，把 root_page 指向 HomePage
    - 冪等性：重複觸發不會新增重複頁
    """
    # 用 runtime 模型（不要用 apps.get_model，避免樹狀 API 缺失）
    try:
        from wagtail.models import Page, Site
        from apps.home.models.home import HomePage
    except Exception:
        return  # 若模型尚不可用，直接略過

    with transaction.atomic():
        # 1) 找到 Wagtail 的 Root（depth=1；抓不到就用 id=1）
        root = Page.objects.filter(depth=1).first()
        if root is None:
            try:
                root = Page.objects.get(id=1)
            except Exception:
                return  # 沒有 Root（非常少見），先跳出

        # 2) 取得或建立 HomePage
        homepage = HomePage.objects.first()
        if not homepage:
            existing = root.get_children().filter(slug="home").first()
            if existing:
                specific = existing.specific
                if isinstance(specific, HomePage):
                    homepage = specific
                else:
                    # 讓出 'home' 的 slug
                    existing.slug = f"welcome-{existing.id}"
                    existing.save()
            if not homepage:
                homepage = HomePage(title="Home", slug="home")
                root.add_child(instance=homepage)
                # 發佈（不同 Wagtail 版本皆相容）
                try:
                    homepage.save_revision().publish()
                except Exception:
                    homepage.save()

        # 3) 取得或建立 Site，並把 root_page 指向 HomePage
        site = Site.objects.filter(is_default_site=True).first()
        if not site:
            hostname = getattr(
                settings, "WAGTAIL_SITE_HOSTNAME",
                (getattr(settings, "ALLOWED_HOSTS", []) or ["localhost"])[0],
            )
            port = getattr(settings, "WAGTAIL_SITE_PORT", 8000)
            site = Site.objects.create(
                hostname=hostname,
                port=port,
                site_name=getattr(settings, "WAGTAIL_SITE_NAME", "My Site"),
                is_default_site=True,
                root_page=homepage,
            )

        if site.root_page_id != homepage.id:
            site.root_page = homepage
            site.is_default_site = True
            site.save()
