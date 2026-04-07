import os
import django
import time
import hmac
import hashlib
import json
import urllib.request
import urllib.error

# Configure Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from store.models import Product, Order
from django.contrib.auth.models import User

print("1. Creating dummy Order for testing...")
user, _ = User.objects.get_or_create(username="webhook_test", email="test@test.com")
product = Product.objects.first()
test_order = Order.objects.create(
    user=user,
    product=product,
    quantity=1,
    total_price_cents=product.price_cents,
    status='PENDING'
)
print(f"Created Order #{test_order.id} with status: {test_order.status}")

# 2. Define our secret and endpoint
WEBHOOK_SECRET = "whsec_testdomainsecret"
URL = "http://127.0.0.1:8000/webhook/"

# 3. Build a fake payload replicating Stripe's checkout.session.completed
payload_dict = {
    "object": "event",
    "id": "evt_test_123",
    "type": "checkout.session.completed",
    "data": {
        "object": {
            "object": "checkout.session",
            "id": "cs_test_123",
            "payment_status": "paid",
            "client_reference_id": str(test_order.id)
        }
    }
}
payload_raw = json.dumps(payload_dict)

# 4. Create Stripe-compliant signature
timestamp = str(int(time.time()))
signed_payload = f"{timestamp}.{payload_raw}"
signature = hmac.new(
    WEBHOOK_SECRET.encode(),
    signed_payload.encode(),
    hashlib.sha256
).hexdigest()

stripe_signature_header = f"t={timestamp},v1={signature}"

print("2. Firing spoofed Stripe Webhook to server...")
req = urllib.request.Request(URL, data=payload_raw.encode('utf-8'))
req.add_header('Content-Type', 'application/json')
req.add_header('Stripe-Signature', stripe_signature_header)

try:
    response = urllib.request.urlopen(req)
    print(f"Success! Server responded HTTP {response.getcode()}")
except urllib.error.HTTPError as e:
    print(f"Failed! Server responded HTTP {e.code}")
    with open("error_500.html", "w") as f:
        f.write(e.read().decode('utf-8'))

# 5. Check if the database actually changed
test_order.refresh_from_db()
print(f"3. Verification -> Order #{test_order.id} status is now: {test_order.status}")
