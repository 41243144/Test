import json
from django.test import RequestFactory
from django.contrib.auth.models import User
from api.v1.order.models import Order
from api.v1.payment.views import ecpay_checkout  # your view

# 1. Pick an existing user
user = User.objects.first()

# 2. Pick an existing order
order = Order.objects.first()  # make sure this order exists

# 3. Create a fake GET request (or POST if your view expects POST)
factory = RequestFactory()
request = factory.get(f'/ecpay-checkout/{order.id}/')  # path doesn't matter
request.user = user  # attach the authenticated user

# 4. Call the view
response = ecpay_checkout(request, order_id=order.id)

# 5. Print the response
print(response.content.decode())
