import django
from django.conf import settings
from django.http import Http404
from django.template.response import TemplateResponse
from django.test import SimpleTestCase
from django.test import override_settings
from django.test.client import RequestFactory
from mock.mock import patch
from rest_framework import status

from yoomoney_payment.tests.mixins import MockResponseMixin

try:
    settings.configure()
except RuntimeError:
    pass


@override_settings(
    PZ_SERVICE_CLASS="yoomoney_payment.commerce.dummy.Service",
)
class TestYooMoneyPaymentRedirectView(SimpleTestCase, MockResponseMixin):

    def setUp(self):
        from yoomoney_payment.views import YooMoneyPaymentView
        django.setup()
        self.view = YooMoneyPaymentView
        self.request_factory = RequestFactory()

    def test_none_yoomoney_extension_url(self):
        request = self.request_factory.get("/payment-gateway/yoomoney/")
        request.GET = {"sessionid": "test-session-id"}
        with self.assertRaises(Http404):
            response = self.view.as_view()(request)
    
    @patch("yoomoney_payment.views.conf.YOOMONEY_EXTENSION_URL", new="https://www.test.com")
    @patch("yoomoney_payment.commerce.dummy.Service.get")
    def test_none_pre_order(self, mock_get):
        response = self._mock_response(
            status_code=200,
            content={},
            headers={"Content-Type": "application/json"},
        )
        mock_get.return_value = response

        request = self.request_factory.get("/payment-gateway/yoomoney/")
        request.GET = {"sessionid": "test-session-id"}
        with self.assertRaises(Http404):
            response = self.view.as_view()(request)
    
    @patch("yoomoney_payment.views.conf.YOOMONEY_EXTENSION_URL", new="https://www.test.com")
    @patch("yoomoney_payment.commerce.dummy.Service.get")
    @patch("yoomoney_payment.commerce.checkout.CheckoutService.generate_hash")
    @patch("secrets.token_hex")
    def test_get(self, mock_token_hex, mock_generate_hash, mock_get):
        response = self._mock_response(
            status_code=200,
            content=self._get_response("orders_checkout_response"),
            headers={"Content-Type": "application/json"},
        )
        mock_get.return_value = response
        mock_generate_hash.return_value = "test-hash"
        mock_token_hex.return_value = "test-salt"

        request = self.request_factory.get("/payment-gateway/yoomoney/")
        request.GET = {"sessionId": "test-session-id"}
        response = self.view.as_view()(request)
        mock_generate_hash.assert_called_once_with("test-session-id", "test-salt")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response, TemplateResponse)
        self.assertEqual(response.template_name, "yoomoney_payment.html")

        context = response.context_data
        self.assertIn("yoo_money_form", context)
