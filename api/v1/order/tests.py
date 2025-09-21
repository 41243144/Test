import json
from django.test import RequestFactory
from api.v1.account.models import User
from api.v1.order.views import create_order
from api.v1.product.models import Product

# Get the first user
user = User.objects.first()

payload = {
    "items": [
        {"product_id": 1, "quantity": 2},
        {"product_id": 2, "quantity": 1}
    ]
}


# Create POST request
factory = RequestFactory()
request = factory.post('/create_order/', data=json.dumps(payload), content_type='application/json')

# Authenticate request with first user
request.user = user

# Call the view
response = create_order(request)

# Print the result
print(response.content.decode())
