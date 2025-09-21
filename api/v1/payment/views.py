from django.conf import settings
from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest, HttpResponseServerError
from .ecpay_payment_sdk import ECPayPaymentSdk, verify_check_mac_value
from api.v1.order.models import Order
from django.views.decorators.csrf import csrf_exempt
from decimal import Decimal, ROUND_HALF_UP
import logging
from django.conf import settings
from django.utils import timezone
from django.urls import reverse

logger = logging.getLogger(__name__)

def ecpay_checkout(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    item_names = "#".join([f"{item.product.name}*{item.quantity}" for item in order.items.all()])

    ecpay_payment_sdk = ECPayPaymentSdk(
        MerchantID=str(settings.MERCHANT_ID),
        HashKey=str(settings.HASH_KEY),
        HashIV=str(settings.HASH_IV),
    )

    total_amount = int(Decimal(order.total_amount).quantize(Decimal('1'), rounding=ROUND_HALF_UP))

    return_url = request.build_absolute_uri(reverse('api.v1.payment:notify_url'))
    order_result_url = request.build_absolute_uri(reverse('api.v1.payment:order_result'))
    client_back_url = request.build_absolute_uri(reverse('api.v1.order:order_result') + f"?order_id={order_id}")

    order_params = {
        'MerchantTradeNo': order.merchant_trade_no,
        'MerchantTradeDate': timezone.localtime(timezone.now()).strftime("%Y/%m/%d %H:%M:%S"),
        'PaymentType': 'aio',
        'TotalAmount': total_amount,
        'TradeDesc': '訂單付款',
        'ItemName': item_names,
        'ReturnURL': return_url,
        'ChoosePayment': 'ALL',
        'ClientBackURL': client_back_url,
        'OrderResultURL': order_result_url,
    }

    try:
        final_order_params = ecpay_payment_sdk.create_order(order_params)

        if settings.DEBUG:
            action_url = 'https://payment-stage.ecpay.com.tw/Cashier/AioCheckOut/V5' # 測試環境
        else:
            action_url = 'https://payment.ecpay.com.tw/Cashier/AioCheckOut/V5' # 正式環境
        
        html = ecpay_payment_sdk.gen_html_post_form(action_url, final_order_params)
        return HttpResponse(html)

    except Exception as exc:
        logger.exception("ECPay checkout failed for order %s", order_id)
        return HttpResponseServerError("無法建立綠界訂單，請稍後再試。")

@csrf_exempt
def ecpay_notify_url(request):
    if request.method != "POST":
        return HttpResponseBadRequest("Only POST")

    data = request.POST.dict()
    logger.info("ECPay notify received: %s", data)

    # 1. 驗證檢查碼
    if not verify_check_mac_value(data, settings.HASH_KEY, settings.HASH_IV):
        logger.warning("ECPay notify: checkmac validation failed.")
        return HttpResponse("CheckMacValue error", status=400)

    # 2. 取得欄位（範例欄位名，依綠界定義）
    merchant_trade_no = data.get("MerchantTradeNo")
    rtn_code = data.get("RtnCode")  # 1 代表交易成功
    rtn_msg = data.get("RtnMsg")

    # 3. 找到訂單並更新狀態
    try:
        order = get_object_or_404(Order, merchant_trade_no=merchant_trade_no)
    except Exception:
        logger.exception("ECPay notify: 訂單找不到 MerchantTradeNo=%s", merchant_trade_no)
        return HttpResponse("Order not found", status=404)

    # 你需要根據 rtn_code 更新：成功->已付款、失敗->付款失敗 等
    if rtn_code == "1":  # 請確認官方文件的成功判斷值
        order.status = Order.STATUS_PAID
        order.paid_at = timezone.now()
        order.save()
        logger.info("Order %s marked as paid via ECPay", order.id)
        return HttpResponse("1|OK")
    else:
        order.status = Order.STATUS_FAILED
        order.save()
        logger.info("Order %s payment failed: %s", order.id, rtn_msg)
        return HttpResponse("0|Fail", status=200)

@csrf_exempt
def ecpay_order_result(request):
    if request.method != "POST":
        return HttpResponseBadRequest("Only POST")
    
    data = request.POST.dict()
    if not verify_check_mac_value(data, settings.HASH_KEY, settings.HASH_IV):
        logger.warning("ECPay order result: checkmac validation failed.")
        return HttpResponse("CheckMacValue error", status=400)
    
    merchant_trade_no = data.get("MerchantTradeNo")

    try:
        order = get_object_or_404(Order, merchant_trade_no=merchant_trade_no)
    except Exception:
        logger.exception("ECPay notify: 訂單找不到 MerchantTradeNo=%s", merchant_trade_no)
        return HttpResponse("Order not found", status=404)

    order_id = order.id
    rtn_code = data.get("RtnCode")
    rtn_msg = data.get("RtnMsg", "交易結果未知")

    # 要跳轉的目標頁面
    redirect_url = request.build_absolute_uri(
        reverse("api.v1.order:order_result") + f"?order_id={order_id}"
    )

    if rtn_code == "1":
        status_text = "付款成功"
    else:
        status_text = "付款失敗"

    html = f"""
    <html>
      <head>
        <meta charset="utf-8">
        <meta http-equiv="refresh" content="1;url={redirect_url}" />
      </head>
      <body>
        <h2>{status_text}</h2>
        <p>訊息：{rtn_msg}</p>
        <p>訂單編號：{order_id}</p>
        <p>1 秒後將自動跳轉，如果沒有跳轉 <a href="{redirect_url}">點此返回</a></p>
      </body>
    </html>
    """
    return HttpResponse(html)
