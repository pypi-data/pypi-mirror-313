from django.urls import path


from click_up.views import ClickWebhook


urlpatterns = [
    path('payments/prepare/update/', ClickWebhook.as_view())
]
