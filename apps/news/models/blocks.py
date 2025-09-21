from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock
from wagtail.embeds.blocks import EmbedBlock
from wagtail.documents.blocks import DocumentChooserBlock


class HeadingBlock(blocks.StructBlock):
    """標題區塊"""
    heading_text = blocks.CharBlock(required=True, help_text="標題文字", label="標題")
    size = blocks.ChoiceBlock(
        choices=[
            ('h2', 'H2'),
            ('h3', 'H3'),
            ('h4', 'H4'),
            ('h5', 'H5'),
            ('h6', 'H6'),
        ],
        default='h2',
        help_text="標題大小",
        label="標題大小"
    )
    
    class Meta:
        template = 'news/blocks/heading_block.html'
        icon = 'title'
        label = '標題'


class ParagraphBlock(blocks.RichTextBlock):
    """段落文字區塊"""
    
    class Meta:
        template = 'news/blocks/paragraph_block.html'
        icon = 'pilcrow'
        label = '段落'


class ImageBlock(blocks.StructBlock):
    """圖片區塊"""
    image = ImageChooserBlock(required=True, label="圖片")
    caption = blocks.CharBlock(required=False, max_length=250, label="圖片說明")
    alt_text = blocks.CharBlock(required=False, max_length=100, label="替代文字")
    alignment = blocks.ChoiceBlock(
        choices=[
            ('left', '靠左'),
            ('center', '置中'),
            ('right', '靠右'),
        ],
        default='center',
        label="對齊方式"
    )
    
    class Meta:
        template = 'news/blocks/image_block.html'
        icon = 'image'
        label = '圖片'


class QuoteBlock(blocks.StructBlock):
    """引言區塊"""
    text = blocks.TextBlock(required=True, label="引言內容")
    author = blocks.CharBlock(required=False, max_length=255, label="作者")
    
    class Meta:
        template = 'news/blocks/quote_block.html'
        icon = 'openquote'
        label = '引言'


class CallToActionBlock(blocks.StructBlock):
    """呼籲行動區塊"""
    title = blocks.CharBlock(required=True, max_length=255, label="標題")
    text = blocks.TextBlock(required=False, label="描述文字")
    button_text = blocks.CharBlock(required=True, max_length=50, label="按鈕文字")
    button_url = blocks.URLBlock(required=True, label="按鈕連結")
    button_style = blocks.ChoiceBlock(
        choices=[
            ('primary', '主要'),
            ('secondary', '次要'),
            ('success', '成功'),
            ('warning', '警告'),
        ],
        default='primary',
        label="按鈕樣式"
    )
    
    class Meta:
        template = 'news/blocks/cta_block.html'
        icon = 'pick'
        label = '呼籲行動'


class EmbedVideoBlock(EmbedBlock):
    """嵌入影片區塊"""
    
    class Meta:
        template = 'news/blocks/embed_block.html'
        icon = 'media'
        label = '嵌入影片'


class DocumentBlock(blocks.StructBlock):
    """文件下載區塊"""
    document = DocumentChooserBlock(required=True, label="文件")
    title = blocks.CharBlock(required=False, max_length=255, label="顯示標題")
    description = blocks.TextBlock(required=False, label="描述")
    
    class Meta:
        template = 'news/blocks/document_block.html'
        icon = 'doc-full'
        label = '文件下載'


class TableBlock(blocks.StructBlock):
    """表格區塊"""
    caption = blocks.CharBlock(required=False, max_length=255, label="表格標題")
    table_html = blocks.TextBlock(
        help_text="請輸入 HTML 表格代碼",
        label="表格 HTML"
    )
    
    class Meta:
        template = 'news/blocks/table_block.html'
        icon = 'table'
        label = '表格'


class CodeBlock(blocks.StructBlock):
    """程式碼區塊"""
    language = blocks.ChoiceBlock(
        choices=[
            ('python', 'Python'),
            ('javascript', 'JavaScript'),
            ('html', 'HTML'),
            ('css', 'CSS'),
            ('bash', 'Bash'),
            ('json', 'JSON'),
            ('xml', 'XML'),
            ('sql', 'SQL'),
        ],
        default='python',
        label="程式語言"
    )
    code = blocks.TextBlock(required=True, label="程式碼")
    
    class Meta:
        template = 'news/blocks/code_block.html'
        icon = 'code'
        label = '程式碼'


class NewsContentStreamBlock(blocks.StreamBlock):
    """新聞內容串流區塊"""
    heading = HeadingBlock()
    paragraph = ParagraphBlock()
    image = ImageBlock()
    quote = QuoteBlock()
    call_to_action = CallToActionBlock()
    embed_video = EmbedVideoBlock()
    document = DocumentBlock()
    table = TableBlock()
    code = CodeBlock()
    
    class Meta:
        block_counts = {
            'heading': {'max_num': 10},
            'call_to_action': {'max_num': 3},
        }
