# models/terms_of_service.py
from django.db import models
from wagtail.contrib.settings.models import BaseGenericSetting, register_setting
from wagtail.fields import StreamField
from wagtail.admin.panels import FieldPanel
from apps.users.blocks.terms_of_service import (
    IntroductionBlock,
    ServiceDescriptionBlock,
    UserResponsibilityBlock,
    TransactionTermsBlock,
    IntellectualPropertyBlock,
    ServiceLimitationsBlock,
    DisclaimerBlock,
    TermsChangeBlock,
    ContactBlock
)

@register_setting
class SiteTermsSetting(BaseGenericSetting):
    content = StreamField(
        [
            ("introduction", IntroductionBlock()),
            ("service_description", ServiceDescriptionBlock()),
            ("user_responsibility", UserResponsibilityBlock()),
            ("transaction_terms", TransactionTermsBlock()),
            ("intellectual_property", IntellectualPropertyBlock()),
            ("service_limitations", ServiceLimitationsBlock()),
            ("disclaimer", DisclaimerBlock()),
            ("terms_change", TermsChangeBlock()),
            ("contact", ContactBlock()),
        ],
        blank=True,
        use_json_field=True,
        block_counts={
            "introduction": {"max_num": 1},
            "contact": {"max_num": 1},
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
        verbose_name = "服務條款"
        verbose_name_plural = "服務條款"
