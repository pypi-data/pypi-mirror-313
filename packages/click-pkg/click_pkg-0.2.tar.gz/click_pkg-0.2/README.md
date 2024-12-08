<h1 align="center">Click Software Development Kit</h1>

<p align="center">
  <a href="https://t.me/+lO97J78xBj45MzBi">
    <img src="https://img.shields.io/badge/Support%20Group-blue?logo=telegram&logoColor=white" alt="Support Group on Telegram"/>
  </a>
</p>


## Installation

```shell
pip install click-pkg
```

## Installation to Django

Add `'click_up'` in to your settings.py

```python
INSTALLED_APPS = [
    ...
    'click_up',
    ...
]
```

Add `'click_up'` credentials inside to settings.py

Click configuration settings.py
```python
CLICK_SERVICE_ID = "your-service-id"
CLICK_MERCHANT_ID = "your-merchant-id"
CLICK_SECRET_KEY = "your-secret-key"
CLICK_ACCOUNT_MODEL = "order.models.Order" # your order model path.
CLICK_AMOUNT_FIELD = "amount" # your amount field that's belongs to your order model
```

Create a new View that about handling call backs
```python
from click_up.views import ClickWebhook


class ClickWebhookAPIView(ClickWebhook):
    def successfully_payment(self, params):
        """
        successfully payment method process you can ovveride it
        """
        print(f"payment successful params: {params}")

    def cancelled_payment(self, params):
        """
        cancelled payment method process you can ovveride it
        """
        print(f"payment cancelled params: {params}")
```

Add a `payme` path to core of urlpatterns:

```python
from django.urls import path
from django.urls import include

from your_app.views import ClickWebhookAPIView


urlpatterns = [
    ...
    path("payment/click/update/", ClickWebhookAPIView.as_view()),
    ...
]
```

Run migrations
```shell
python3 manage.py makemigrations && python manage.py migrate
```

🎉 Congratulations you have been integrated click with django, keep reading docs. After successfull migrations check your admin panel and see results what happened.


## Generate Pay Link
Example to generate link:

- Input

```python
from click_up import ClickUp


click_up = ClickUp(service_id="your-service-id", merchant_id="your-merchant-id") # alternatively you can use settings variables as well here.


# Generate Paylik payment link
paylink = click_up.initializer.generate_pay_link(
  id=1, # id maybe order_id or acount_id (user_id, chat_id and etc..)
  amount=100,
  return_url="https://example.com"
)
```

- Output
```
https://my.click.uz/services/pay?service_id=service_id&merchant_id=merchant_id&amount=1000&transaction_param=1&return_url=https://example.com
```
