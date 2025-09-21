from wagtail import hooks

@hooks.register("construct_page_listing_queryset")
def limit_page_listing_to_owner(request, parent_page, pages):
    # 超級使用者看所有
    if request.user.is_superuser:
        return pages
    # 只顯示 owner 欄位等於當前使用者的頁面
    return pages.filter(owner=request.user)

@hooks.register("construct_explorer_page_queryset")
def limit_explorer_queryset(parent_page, pages, request):
    # 超級使用者不受限
    if request.user.is_superuser:
        return pages
    # 正確過濾 owner 欄位，而不是 user
    return pages.filter(owner=request.user)
