# blocks/terms_of_service.py
from wagtail import blocks

############# 警告區塊 #############
class AlertBlock(blocks.StructBlock):
    TYPES = [
        ("primary",   "主色（藍色）"),
        ("secondary", "次要（灰色）"),
        ("success",   "成功（綠色）"),
        ("danger",    "危險（紅色）"),
        ("warning",   "警告（黃色）"),
        ("info",      "資訊（淺藍）"),
        ("light",     "淺色（白色）"),
        ("dark",      "深色（黑色）"),
    ]

    ICON_MAP = {
        "primary":   "info-circle",
        "secondary": "clipboard-list",
        "success":   "check-circle",
        "danger":    "times-circle",
        "warning":   "exclamation-triangle",
        "info":      "info-circle",
        "light":     "sun",
        "dark":      "moon",
    }

    alert_label = blocks.CharBlock(
        required=True,
        default="重要提醒",
        label="警告標題",
        help_text="顯示在警告區塊的標題"
    )

    alert_type = blocks.ChoiceBlock(
        choices=TYPES,
        default="warning",
        label="警告樣式",
        help_text="選擇 Bootstrap 的 alert 顏色",
    )
    content = blocks.TextBlock(label="內容")

    class Meta:
        template = "blocks/terms_of_service/alert_block.html"
        label = "警告區塊"

    def get_context(self, value, parent_context=None):
        context = super().get_context(value, parent_context)
        at = value.get("alert_type")
        # 取得 icon
        context["icon_name"] = self.ICON_MAP.get(at, "info-circle")
        return context

############# 前言區塊 #############
class IntroductionBlock(blocks.StructBlock):
    site_name = blocks.CharBlock(
        required=True,
        default="尚虎雲產銷平台",
        label="網站名稱"
    )

    extra = blocks.StreamBlock(
        [
            ("alert", AlertBlock()),
        ],
        label="新增警告區塊",
        required=False,
    )
    
    class Meta:
        template = "blocks/terms_of_service/introduction.html"
        label = "前言區塊"

################# 服務說明 #############
class SectionBlock(blocks.StructBlock):
    """一個可重複的「分類＋項目清單」區塊"""
    section_title = blocks.CharBlock(
        required=True,
        label="標題",
        help_text="例如：平台服務"
    )
    items = blocks.ListBlock(
        blocks.CharBlock(max_length=255, label="項目"),
        label="項目清單",
        help_text="列出該分類下的所有項目"
    )

    class Meta:
        icon = "list-ul"
        label = "服務分類區塊"

class ServiceDescriptionBlock(blocks.StructBlock):
    title = blocks.CharBlock(
        required=True,
        default="服務說明",
        label="區塊標題"
    )
    sections = blocks.ListBlock(SectionBlock(), label="服務分類")

    class Meta:
        template = "blocks/terms_of_service/service_description.html"
        label = "服務說明區塊"

################# 用戶責任 #############
class UserResponsibilityBlock(blocks.StructBlock):
    title = blocks.CharBlock(
        required=True,
        default="用戶責任與義務",
        label="區塊標題"
    )
    content = blocks.RichTextBlock(
        label="責任說明",
        help_text="說明用戶需要承擔的責任"
    )
    responsibilities = blocks.ListBlock(
        blocks.StructBlock([
            ('title', blocks.CharBlock(label="責任項目")),
            ('description', blocks.TextBlock(label="詳細說明")),
        ]),
        label="責任清單"
    )
    
    extra = blocks.StreamBlock(
        [
            ("alert", AlertBlock()),
        ],
        label="新增警告區塊",
        required=False,
    )

    class Meta:
        template = "blocks/terms_of_service/user_responsibility.html"
        label = "用戶責任區塊"

################# 交易條款 #############
class TransactionTermsBlock(blocks.StructBlock):
    title = blocks.CharBlock(
        required=True,
        default="交易條款",
        label="區塊標題"
    )
    transaction_rules = blocks.ListBlock(
        blocks.StructBlock([
            ('title', blocks.CharBlock(label="規則項目")),
            ('description', blocks.TextBlock(label="詳細說明")),
        ]),
        label="交易規則"
    )
    refund_policy = blocks.ListBlock(
        blocks.CharBlock(max_length=255, label="退款政策項目"),
        label="退款與退貨政策"
    )

    class Meta:
        template = "blocks/terms_of_service/transaction_terms.html"
        label = "交易條款區塊"

################# 知識產權 #############
class IntellectualPropertyBlock(blocks.StructBlock):
    title = blocks.CharBlock(
        required=True,
        default="知識產權",
        label="區塊標題"
    )
    platform_rights = blocks.ListBlock(
        blocks.CharBlock(max_length=255, label="平台權利"),
        label="平台知識產權"
    )
    user_rights = blocks.ListBlock(
        blocks.CharBlock(max_length=255, label="用戶權利"),
        label="用戶內容權利"
    )

    class Meta:
        template = "blocks/terms_of_service/intellectual_property.html"
        label = "知識產權區塊"

################# 服務限制與終止 #############
class ServiceLimitationsBlock(blocks.StructBlock):
    title = blocks.CharBlock(
        required=True,
        default="服務限制與終止",
        label="區塊標題"
    )
    platform_rights = blocks.ListBlock(
        blocks.StructBlock([
            ('title', blocks.CharBlock(label="權利項目")),
            ('description', blocks.TextBlock(label="詳細說明")),
        ]),
        label="平台保留權利"
    )
    notice_text = blocks.TextBlock(
        label="通知說明",
        required=False,
        help_text="終止服務的通知說明"
    )

    class Meta:
        template = "blocks/terms_of_service/service_limitations.html"
        label = "服務限制區塊"

################# 免責聲明 #############
class DisclaimerBlock(blocks.StructBlock):
    title = blocks.CharBlock(
        required=True,
        default="免責聲明",
        label="區塊標題"
    )
    disclaimer_items = blocks.ListBlock(
        blocks.CharBlock(max_length=255, label="免責項目"),
        label="免責情況"
    )
    
    extra = blocks.StreamBlock(
        [
            ("alert", AlertBlock()),
        ],
        label="新增提醒區塊",
        required=False,
    )

    class Meta:
        template = "blocks/terms_of_service/disclaimer.html"
        label = "免責聲明區塊"

################# 條款變更 #############
class TermsChangeBlock(blocks.StructBlock):
    title = blocks.CharBlock(
        required=True,
        default="條款變更",
        label="區塊標題"
    )
    change_procedures = blocks.ListBlock(
        blocks.CharBlock(max_length=255, label="變更程序"),
        label="條款修訂程序"
    )
    notice_text = blocks.TextBlock(
        label="變更說明",
        required=False,
        help_text="建議用戶定期查看的說明"
    )

    class Meta:
        template = "blocks/terms_of_service/terms_change.html"
        label = "條款變更區塊"

################# 聯絡資訊 #############
class ContactBlock(blocks.StructBlock):
    title = blocks.CharBlock(
        required=True,
        default="聯絡我們",
        label="區塊標題"
    )
    description = blocks.TextBlock(
        label="說明文字",
        default="如您對本服務條款有任何疑問或建議，請透過以下方式聯絡我們："
    )
    email = blocks.EmailBlock(
        label="電子郵件",
        default="legal@shanghuyun.com"
    )
    phone = blocks.CharBlock(
        label="客服電話",
        default="(02) 1234-5678"
    )
    service_hours = blocks.CharBlock(
        label="服務時間",
        default="週一至週五 09:00-18:00"
    )
    address = blocks.CharBlock(
        label="通訊地址",
        default="台北市信義區市府路1號"
    )

    class Meta:
        template = "blocks/terms_of_service/contact.html"
        label = "聯絡資訊區塊"
