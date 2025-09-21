# blocks/privacy_policy.py
from wagtail import blocks



############# 警告區塊 #############
# apps/users/blocks/privacy_policy.py

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
        default="警告",
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
        template = "blocks/privacy_policy/alert_block.html"
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
        template = "blocks/privacy_policy/introduction.html"
        label = "前言區塊"


################# 收集的資料 #############

class SectionBlock(blocks.StructBlock):
    """一個可重複的「分類＋項目清單」區塊"""
    section_title = blocks.CharBlock(
        required=True,
        label="標題",
        help_text="例如： 個人識別資料"
    )
    items = blocks.ListBlock(
        blocks.CharBlock(max_length=255, label="項目"),
        label="項目清單",
        help_text="列出該分類下的所有項目"
    )

    class Meta:
        icon = "list-ul"
        label = "資料分類區塊"

class CollectedDataBlock(blocks.StructBlock):
    title = blocks.CharBlock(
        required=False,
        default="我們收集的資料",
        label="區塊標題",
    )

    sections = blocks.ListBlock(
        SectionBlock(),
        label="資料分類",
        help_text="點 + 新增一個分類，再為它填標題＆項目"
    )

    extra = blocks.StreamBlock(
        [
            ("alert", AlertBlock()),
        ],
        label="新增警告",
        required=False,
    )

    class Meta:
        template = "blocks/privacy_policy/collected_data_block.html"
        label = "收集的資料區塊"

############# 資料使用目的 #############
class DataUsageBlock(blocks.StructBlock):
    title = blocks.CharBlock(
        required=False,
        default="資料使用目的",
        label="區塊標題",
    )
    subtitle = blocks.CharBlock(
        required=False,
        default="我們使用您的個人資料於以下目的：",
        label="前言文字",
    )

    usage_items = blocks.ListBlock(
        blocks.StructBlock([
            ("name", blocks.CharBlock(label="用途標題")),
            ("description", blocks.CharBlock(label="用途說明")),
        ]),
        label="用途清單",
        help_text="每一筆填一個用途，包括標題與說明",
    )

    extra = blocks.StreamBlock(
        [
            ("alert", AlertBlock()),
        ],
        label="新增警告",
        required=False,
    )

    class Meta:
        template = "blocks/privacy_policy/data_usage_block.html"
        label = "資料使用目的區塊"

############## 資料分享區塊 #############
class DataShareBlock(blocks.StructBlock):
    title = blocks.CharBlock(
        required=False,
        default="資料分享與揭露",
        label="區塊標題",
    )

    subtitle = blocks.CharBlock(
        required=False,
        default="我們可能在以下情況分享您的資料：",
        label="副標題",
    )
    # 動態清單：分享情況
    share_conditions = blocks.ListBlock(
        blocks.StructBlock([
            ("condition", blocks.CharBlock(label="分享情況")),
            ("description", blocks.CharBlock(label="說明")),
        ]),
        label="分享情況列表",
        help_text="點 + 新增一筆，填入分享情況與對應說明",
    )

    extra = blocks.StreamBlock(
        [
            ("alert", AlertBlock()),
        ],
        label="新增警告",
        required=False,
    )

    class Meta:
        template = "blocks/privacy_policy/data_share_block.html"
        label = "資料分享區塊"

############## 資料安全區塊 #############
class DataSecurityBlock(blocks.StructBlock):
    title = blocks.CharBlock(
        required=False,
        default="資料安全措施",
        label="區塊標題",
    )
    subtitle = blocks.CharBlock(
        required=False,
        default="我們採用多重安全措施保護您的資料：",
        label="副標題",
    )
    measures_left = blocks.ListBlock(
        blocks.CharBlock(label="左側項目"),
        label="顯示在左側的項目",
        help_text="例如 SSL 加密傳輸技術、資料庫加密儲存、存取權限控制…",
    )
    measures_right = blocks.ListBlock(
        blocks.CharBlock(label="右側項目"),
        label="顯示在右側的項目",
        help_text="例如 定期安全性檢測與更新、員工資安教育訓練、第三方安全認證…",
    )

    extra = blocks.StreamBlock(
        [
            ("alert", AlertBlock()),
        ],
        label="新增警告",
        required=False,
    )

    class Meta:
        template = "blocks/privacy_policy/data_security_block.html"
        label = "資料安全區塊"

############## 您的權利區塊 #############
class RightsBlock(blocks.StructBlock):
    title = blocks.CharBlock(
        required=False,
        default="您的權利",
        label="區塊標題",
    )
    subtitle = blocks.CharBlock(
        required=False,
        default="根據個人資料保護法，您享有以下權利：",
        label="副標題",
    )
    left_items = blocks.ListBlock(
        blocks.StructBlock([
            ("name", blocks.CharBlock(label="項目")),
            ("description", blocks.CharBlock(label="說明")),
        ]),
        label="左側權利清單",
        help_text="例如 查詢權、更正權、刪除權",
    )
    right_items = blocks.ListBlock(
        blocks.StructBlock([
            ("name", blocks.CharBlock(label="項目")),
            ("description", blocks.CharBlock(label="說明")),
        ]),
        label="右側權利清單",
        help_text="例如 停止處理權、資料可攜權、反對權",
    )
    contact_text = blocks.CharBlock(
        required=False,
        default="如需行使上述權利，請透過以下聯絡方式與我們聯繫。",
        label="聯絡說明",
    )

    extra = blocks.StreamBlock(
        [
            ("alert", AlertBlock()),
        ],
        label="新增警告",
        required=False,
    )

    class Meta:
        template = "blocks/privacy_policy/rights_block.html"
        label = "您的權利區塊"

############## Cookie區塊 #############
class CookiePolicyBlock(blocks.StructBlock):
    title = blocks.CharBlock(
        required=False,
        default="Cookie 使用政策",
        label="區塊標題",
    )
    subtitle = blocks.CharBlock(
        required=False,
        default="我們使用 Cookie 來：",
        label="副標題",
    )
    items = blocks.ListBlock(
        blocks.CharBlock(label="用途"),
        label="使用項目清單",
        help_text="在此列表中新增每一項 Cookie 使用用途",
    )
    footnote = blocks.CharBlock(
        required=False,
        default="您可以透過瀏覽器設定管理或停用 Cookie，但這可能影響部分網站功能。",
        label="附註文字",
    )

    class Meta:
        template = "blocks/privacy_policy/cookie_policy_block.html"
        label = "Cookie 政策區塊"

############## 聯絡我們區塊 ##############
class ContactBlock(blocks.StructBlock):
    title = blocks.CharBlock(
        required=False,
        default="聯絡我們",
        label="區塊標題",
    )
    intro = blocks.RichTextBlock(
        required=False,
        default="如您對本隱私權政策有任何疑問或建議，請透過以下方式聯絡我們：",
        label="前言文字",
        help_text="顯示在聯絡方式列表上方",
    )
    left_contacts = blocks.ListBlock(
        blocks.StructBlock([
            ("icon", blocks.ChoiceBlock(
                choices=[
                    ("envelope", "電子郵件"),
                    ("phone", "客服電話"),
                ],
                default="envelope",
                label="左側圖示",
                help_text="選擇 FontAwesome 圖示名稱（無 fa- 前綴）"
            )),
            ("label", blocks.CharBlock(label="欄位標題")),
            ("value", blocks.CharBlock(label="欄位內容")),
        ]),
        label="左側聯絡方式",
        help_text="例如 電子郵件、客服電話",
    )
    right_contacts = blocks.ListBlock(
        blocks.StructBlock([
            ("icon", blocks.ChoiceBlock(
                choices=[
                    ("clock", "服務時間"),
                    ("map-marker-alt", "通訊地址"),
                ],
                default="clock",
                label="右側圖示",
                help_text="選擇 FontAwesome 圖示名稱（無 fa- 前缀）"
            )),
            ("label", blocks.CharBlock(label="欄位標題")),
            ("value", blocks.CharBlock(label="欄位內容")),
        ]),
        label="右側聯絡方式",
        help_text="例如 服務時間、通訊地址",
    )

    class Meta:
        template = "blocks/privacy_policy/contact_block.html"
        label = "聯絡我們區塊"