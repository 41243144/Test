from django import forms
from .models import Vendor


class VendorSelfEditForm(forms.ModelForm):
    """保留示例：目前未與 ModelAdmin 綁定，邏輯已移至視圖層。"""

    class Meta:
        model = Vendor
        fields = ["name", "intro", "description", "address", "phone", "category"]
