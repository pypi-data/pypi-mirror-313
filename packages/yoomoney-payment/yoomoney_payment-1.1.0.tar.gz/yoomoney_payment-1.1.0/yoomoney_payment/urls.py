from django.conf.urls import url

from yoomoney_payment.views import YooMoneyPaymentView

urlpatterns = [
    url(r"^$", YooMoneyPaymentView.as_view(), name="yoomoney-payment"),
]
