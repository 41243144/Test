from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock
from wagtail.embeds.blocks import EmbedBlock
from wagtail.snippets.blocks import SnippetChooserBlock


class HeroBlock(blocks.StructBlock):
    """主視覺區塊"""
    title = blocks.CharBlock(required=True, max_length=255, label="主標題")
    subtitle = blocks.TextBlock(required=False, label="副標題")
    background_image = ImageChooserBlock(required=True, label="背景圖片")
    button_text_1 = blocks.CharBlock(required=False, max_length=50, label="按鈕1文字")
    button_url_1 = blocks.URLBlock(required=False, label="按鈕1連結")
    button_text_2 = blocks.CharBlock(required=False, max_length=50, label="按鈕2文字")
    button_url_2 = blocks.URLBlock(required=False, label="按鈕2連結")
    
    class Meta:
        template = 'home/blocks/hero_block.html'
        icon = 'image'
        label = '主視覺區塊'


class AboutBlock(blocks.StructBlock):
    """關於我們區塊"""
    title = blocks.CharBlock(required=True, max_length=255, label="標題")
    description = blocks.RichTextBlock(required=True, label="描述")
    image = ImageChooserBlock(required=True, label="圖片")
    features = blocks.ListBlock(
        blocks.StructBlock([
            ('feature_text', blocks.CharBlock(max_length=255, label="特色描述")),
        ]),
        label="特色列表",
        min_num=1,
        max_num=5
    )
    
    class Meta:
        template = 'home/blocks/about_block.html'
        icon = 'group'
        label = '關於我們'


class FeatureBlock(blocks.StructBlock):
    """功能特色區塊"""
    title = blocks.CharBlock(required=True, max_length=255, label="區塊標題")
    subtitle = blocks.CharBlock(required=False, max_length=255, label="副標題")
    features = blocks.ListBlock(
        blocks.StructBlock([
            ('number', blocks.CharBlock(max_length=10, label="編號")),
            ('title', blocks.CharBlock(max_length=255, label="功能標題")),
            ('description', blocks.TextBlock(label="功能描述")),
        ]),
        label="功能列表",
        min_num=1,
        max_num=6
    )
    
    class Meta:
        template = 'home/blocks/feature_block.html'
        icon = 'list-ul'
        label = '功能特色'


# class ProductShowcaseBlock(blocks.StructBlock):
#     """產品展示區塊"""
#     title = blocks.CharBlock(required=True, max_length=255, label="區塊標題")
#     subtitle = blocks.CharBlock(required=False, max_length=255, label="副標題")
#     products = blocks.ListBlock(
#         blocks.StructBlock([
#             ('name', blocks.CharBlock(max_length=255, label="產品名稱")),
#             ('price', blocks.CharBlock(max_length=50, label="價格")),
#             ('description', blocks.TextBlock(label="產品描述")),
#             ('image', ImageChooserBlock(label="產品圖片")),
#             ('category', blocks.ChoiceBlock(
#                 choices=[
#                     ('vegetables', '蔬菜類'),
#                     ('fruits', '水果類'),
#                     ('grains', '穀物類'),
#                 ],
#                 label="產品分類"
#             )),
#         ]),
#         label="產品列表",
#         min_num=1,
#         max_num=12
#     )
    
#     class Meta:
#         template = 'home/blocks/product_showcase_block.html'
#         icon = 'pick'
#         label = '產品展示'


class ServiceTabsBlock(blocks.StructBlock):
    """服務標籤頁區塊"""
    title = blocks.CharBlock(required=True, max_length=255, label="區塊標題")
    subtitle = blocks.CharBlock(required=False, max_length=255, label="副標題")
    services = blocks.ListBlock(
        blocks.StructBlock([
            ('tab_title', blocks.CharBlock(max_length=255, label="標籤標題")),
            ('service_title', blocks.CharBlock(max_length=255, label="服務標題")),
            ('description', blocks.RichTextBlock(label="服務描述")),
            ('image', ImageChooserBlock(label="服務圖片")),
        ]),
        label="服務列表",
        min_num=1,
        max_num=8
    )
    
    class Meta:
        template = 'home/blocks/service_tabs_block.html'
        icon = 'folder-open-1'
        label = '服務標籤頁'


class EventSliderBlock(blocks.StructBlock):
    """活動輪播區塊"""
    background_image = ImageChooserBlock(required=True, label="背景圖片")
    events = blocks.ListBlock(
        blocks.StructBlock([
            ('title', blocks.CharBlock(max_length=255, label="活動標題")),
            ('subtitle', blocks.CharBlock(max_length=50, label="副標題", required=False)),
            ('description', blocks.RichTextBlock(label="活動描述")),
            ('image', ImageChooserBlock(label="活動圖片")),
            ('features', blocks.ListBlock(
                blocks.CharBlock(max_length=255, label="活動特色"),
                label="特色列表",
                min_num=0,
                max_num=5
            )),
        ]),
        label="活動列表",
        min_num=1,
        max_num=6
    )
    
    class Meta:
        template = 'home/blocks/event_slider_block.html'
        icon = 'date'
        label = '活動輪播'


# class NewsPreviewBlock(blocks.StructBlock):
#     """最新消息預覽區塊"""
#     title = blocks.CharBlock(required=True, max_length=255, label="區塊標題")
#     subtitle = blocks.CharBlock(required=False, max_length=255, label="副標題")
#     news_count = blocks.IntegerBlock(
#         default=6,
#         min_value=3,
#         max_value=12,
#         label="顯示消息數量"
#     )
#     show_more_button = blocks.BooleanBlock(
#         default=True,
#         required=False,
#         label="顯示更多按鈕"
#     )
#     more_button_text = blocks.CharBlock(
#         default="查看更多消息",
#         max_length=50,
#         label="更多按鈕文字"
#     )
#     more_button_url = blocks.URLBlock(required=False, label="更多按鈕連結")
    
#     class Meta:
#         template = 'home/blocks/news_preview_block.html'
#         icon = 'doc-full'
#         label = '最新消息預覽'


class TestimonialBlock(blocks.StructBlock):
    """合作單位區塊"""
    title = blocks.CharBlock(required=True, max_length=255, label="區塊標題")
    subtitle = blocks.CharBlock(required=False, max_length=255, label="副標題")
    testimonials = blocks.ListBlock(
        blocks.StructBlock([
            ('quote', blocks.TextBlock(label="內容")),
            ('name', blocks.CharBlock(max_length=255, label="合作單位")),
            ('title', blocks.CharBlock(max_length=255, label="合作單位標題")),
            ('avatar', ImageChooserBlock(label="合作單位圖片")),
        ]),
        label="合作單位列表",
        min_num=1,
        max_num=10
    )
    
    class Meta:
        template = 'home/blocks/testimonial_block.html'
        icon = 'openquote'
        label = '合作單位'


class GalleryBlock(blocks.StructBlock):
    """圖片廊區塊"""
    title = blocks.CharBlock(required=True, max_length=255, label="區塊標題")
    subtitle = blocks.CharBlock(required=False, max_length=255, label="副標題")
    gallery_images = blocks.ListBlock(
        blocks.StructBlock([
            ('image', ImageChooserBlock(label="圖片")),
            ('caption', blocks.CharBlock(max_length=255, label="圖片說明", required=False)),
            ('alt_text', blocks.CharBlock(max_length=255, label="替代文字", required=False)),
        ]),
        label="圖片列表",
        min_num=1,
        max_num=20
    )
    
    class Meta:
        template = 'home/blocks/gallery_block.html'
        icon = 'image'
        label = '圖片廊'


class TeamBlock(blocks.StructBlock):
    """團隊成員區塊"""
    title = blocks.CharBlock(required=True, max_length=255, label="區塊標題")
    subtitle = blocks.CharBlock(required=False, max_length=255, label="副標題")
    team_members = blocks.ListBlock(
        blocks.StructBlock([
            ('name', blocks.CharBlock(max_length=255, label="姓名")),
            ('position', blocks.CharBlock(max_length=255, label="職位")),
            ('photo', ImageChooserBlock(label="照片")),
            ('bio', blocks.TextBlock(label="簡介", required=False)),
            ('social_twitter', blocks.URLBlock(label="Twitter", required=False)),
            ('social_facebook', blocks.URLBlock(label="Facebook", required=False)),
            ('social_instagram', blocks.URLBlock(label="Instagram", required=False)),
            ('social_linkedin', blocks.URLBlock(label="LinkedIn", required=False)),
        ]),
        label="團隊成員",
        min_num=1,
        max_num=12
    )
    
    class Meta:
        template = 'home/blocks/team_block.html'
        icon = 'group'
        label = '團隊成員'


class ContactBlock(blocks.StructBlock):
    """聯絡我們區塊"""
    title = blocks.CharBlock(required=True, max_length=255, label="區塊標題")
    subtitle = blocks.CharBlock(required=False, max_length=255, label="副標題")
    map_embed_code = blocks.TextBlock(
        required=False, 
        label="地圖嵌入代碼",
        help_text="請直接貼上 Google Maps 或其他地圖服務的完整 iframe 嵌入代碼"
    )
    contact_info = blocks.ListBlock(
        blocks.StructBlock([
            ('icon', blocks.CharBlock(
                max_length=50,
                help_text="Bootstrap Icon 類別名稱 (例: bi-geo-alt)",
                label="圖示"
            )),
            ('title', blocks.CharBlock(max_length=255, label="標題")),
            ('content', blocks.RichTextBlock(label="內容")),
        ]),
        label="聯絡資訊",
        min_num=0,
        max_num=8
    )
    
    class Meta:
        template = 'home/blocks/contact_block.html'
        icon = 'mail'
        label = '聯絡我們'


class TextImageBlock(blocks.StructBlock):
    """文字圖片區塊"""
    title = blocks.CharBlock(required=True, max_length=255, label="標題")
    content = blocks.RichTextBlock(required=True, label="內容")
    image = ImageChooserBlock(required=True, label="圖片")
    image_position = blocks.ChoiceBlock(
        choices=[
            ('left', '圖片在左'),
            ('right', '圖片在右'),
        ],
        default='right',
        label="圖片位置"
    )
    
    class Meta:
        template = 'home/blocks/text_image_block.html'
        icon = 'doc-full'
        label = '文字圖片'


# class CallToActionBlock(blocks.StructBlock):
#     """呼籲行動區塊"""
#     title = blocks.CharBlock(required=True, max_length=255, label="標題")
#     subtitle = blocks.CharBlock(required=False, max_length=255, label="副標題")
#     description = blocks.TextBlock(required=False, label="描述")
#     button_text = blocks.CharBlock(required=True, max_length=50, label="按鈕文字")
#     button_url = blocks.URLBlock(required=True, label="按鈕連結")
#     button_style = blocks.ChoiceBlock(
#         choices=[
#             ('btn-primary', '主要'),
#             ('btn-secondary', '次要'),
#             ('btn-success', '成功'),
#             ('btn-warning', '警告'),
#             ('btn-danger', '危險'),
#         ],
#         default='btn-primary',
#         label="按鈕樣式"
#     )
#     background_color = blocks.ChoiceBlock(
#         choices=[
#             ('', '預設'),
#             ('bg-light', '淺色背景'),
#             ('bg-dark', '深色背景'),
#             ('bg-primary', '主色背景'),
#         ],
#         default='bg-light',
#         label="背景顏色"
#     )
    
#     class Meta:
#         template = 'home/blocks/cta_block.html'
#         icon = 'pick'
#         label = '呼籲行動'


# class CustomHTMLBlock(blocks.StructBlock):
#     """自訂 HTML 區塊"""
#     title = blocks.CharBlock(required=False, max_length=255, label="區塊標題")
#     html_content = blocks.TextBlock(
#         required=True,
#         label="HTML 內容",
#         help_text="請輸入自訂的 HTML 代碼"
#     )
#     css_classes = blocks.CharBlock(
#         required=False,
#         max_length=255,
#         label="CSS 類別",
#         help_text="額外的 CSS 類別名稱"
#     )
    
#     class Meta:
#         template = 'home/blocks/custom_html_block.html'
#         icon = 'code'
#         label = '自訂 HTML'


class HomePageStreamBlock(blocks.StreamBlock):
    """首頁內容串流區塊"""
    hero = HeroBlock()
    about = AboutBlock()
    features = FeatureBlock()
    # products = ProductShowcaseBlock()
    services = ServiceTabsBlock()
    events = EventSliderBlock()
    # news = NewsPreviewBlock()
    testimonials = TestimonialBlock()
    gallery = GalleryBlock()
    team = TeamBlock()
    contact = ContactBlock()
    text_image = TextImageBlock()
    # cta = CallToActionBlock()
    # custom_html = CustomHTMLBlock()
    
    class Meta:
        block_counts = {
            'hero': {'max_num': 1},
            'contact': {'max_num': 1},
        }
