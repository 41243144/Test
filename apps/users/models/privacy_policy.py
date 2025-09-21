from django.db import models
from wagtail.contrib.settings.models import BaseGenericSetting, register_setting
from wagtail.fields import StreamField
from wagtail.admin.panels import FieldPanel
from apps.users.blocks.privacy_policy import (
    IntroductionBlock, 
    CollectedDataBlock,
    DataUsageBlock,
    DataShareBlock,
    DataSecurityBlock,
    RightsBlock,
    CookiePolicyBlock,
    ContactBlock
)

@register_setting
class SitePolicySetting(BaseGenericSetting):
    content = StreamField(
        [
            ("introduction", IntroductionBlock()),
            ("collected_data", CollectedDataBlock()),
            ("data_usage", DataUsageBlock()),
            ("data_share", DataShareBlock()),
            ("data_security", DataSecurityBlock()),
            ("rights", RightsBlock()),
            ("cookie_policy", CookiePolicyBlock()),
            ("contact", ContactBlock()),
        ],
        blank=True,
        use_json_field=True,

        block_counts={
            "introduction": {"max_num": 1},
        },
    )
    
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="最後更新時間",
        help_text="內容最後更新的時間"
    )

    panels = [
        FieldPanel("content"),
    ]

    class Meta:
        verbose_name = "隱私權政策"
        verbose_name_plural = "隱私權政策"
