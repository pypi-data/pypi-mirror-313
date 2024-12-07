from decimal import Decimal
import json

from unittest.mock import Mock
from django.http import Http404
from django.conf import settings
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
    HASH_SECRET_KEY="test-hash-secret-key",
    PZ_SERVICE_CLASS="yoomoney_payment.commerce.dummy.Service",
)
class TestCheckoutService(SimpleTestCase, MockResponseMixin):
    def setUp(self):
        from yoomoney_payment.commerce.checkout import CheckoutService

        self.service = CheckoutService()
        self.request_factory = RequestFactory()

    @patch("yoomoney_payment.commerce.dummy.Service.get")
    @patch("yoomoney_payment.commerce.checkout.CheckoutService.generate_hash")
    @patch("yoomoney_payment.commerce.checkout.CheckoutService.generate_salt")
    def test_get_data(self, mock_generate_salt, mock_generate_hash, mock_get):
        mock_generate_hash.return_value = "test-hash"
        mock_generate_salt.return_value = "test-salt"
        mocked_response = self._mock_response(
            status_code=200,
            content=self._get_response("orders_checkout_response"),
            headers={"Content-Type": "application/json"},
        )
        mock_get.return_value = mocked_response

        request = self.request_factory.get("/payment-gateway/yoomoney/")
        basket_data = self.service.get_data(request)

        self.assertEqual(basket_data["salt"], "test-salt")
        self.assertEqual(basket_data["hash"], "test-hash")
        
        basket_items = [
            {'amount': '246.86', 'product_name': 'Petıt / 110x170cm Dijital Baskılı Halı'},
            {'amount': '87.69', 'product_name': '50cm Bombeli Saat Desen 13'},
            {'amount': '34.01', 'product_name': 'Demet Lavanta Çiçek 62cm'}]
        self.assertEqual(
            basket_data["data"], json.dumps({"order_items": basket_items})
        )
        total_amount = sum([Decimal(item["amount"]) for item in json.loads(basket_data["data"])["order_items"]])
        self.assertAlmostEqual(total_amount, Decimal(368.56))

    @patch("yoomoney_payment.commerce.dummy.Service.get")
    def test_retrieve_pre_oder(self, mock_get):
        mocked_response = self._mock_response(
            status_code=200,
            content=self._get_response("orders_checkout_response"),
            headers={"Content-Type": "application/json"},
        )
        mock_get.return_value = mocked_response

        request = self.request_factory.get("/payment-gateway/yoomoney/")
        response = self.service._retrieve_pre_order(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("pre_order", response.data)

    @patch("yoomoney_payment.commerce.dummy.Service.get")
    def test_get_basket_items(self, mock_get):
        mocked_response = self._mock_response(
            status_code=200,
            content=self._get_response("orders_checkout_response"),
            headers={"Content-Type": "application/json"},
        )
        mock_get.return_value = mocked_response

        request = self.request_factory.get("/payment-gateway/yoomoney/")
        basket_items = self.service._get_basket_items(request)
        self.assertEqual(
            basket_items,
         [{'amount': '246.86', 'product_name': 'Petıt / 110x170cm Dijital Baskılı Halı'},
          {'amount': '87.69', 'product_name': '50cm Bombeli Saat Desen 13'},
          {'amount': '34.01', 'product_name': 'Demet Lavanta Çiçek 62cm'}],
        )

    @patch("hashlib.sha512")
    @patch("yoomoney_payment.commerce.checkout.conf.HASH_SECRET_KEY", new="test-hash-secret-key")
    def test_get_hash(self, mock_sha512):
        session_id = "test-session-id"
        self.service.generate_hash(session_id, "test-salt")
        mock_sha512.assert_called_once_with(
            "test-salt|test-session-id|test-hash-secret-key".encode("utf-8")
        )

    @patch("secrets.token_hex")
    def test_generate_salt(self, mock_token_hex):
        self.service.generate_salt()
        mock_token_hex.assert_called_once()
        
    def test_get_product_name(self):
        product_name = None
        self.assertEqual(self.service._get_product_name(product_name), "none")
        
        product_name = "t" * 254
        self.assertEqual(self.service._get_product_name(product_name), product_name)
             
        product_name = "t" * 255
        self.assertEqual(self.service._get_product_name(product_name), product_name)
        
        product_name = "t" * 256
        self.assertEqual(self.service._get_product_name(product_name), "t" * 255)
        
    def test__find_decimal_places(self):
        self.assertEqual(self.service._find_decimal_places("10.000"), 3)
        self.assertEqual(self.service._find_decimal_places("10.00"), 2)
        self.assertEqual(self.service._find_decimal_places("10.0"), 1)
        self.assertEqual(self.service._find_decimal_places("10"), 0)
        
    def test__get_quantize_format(self):
        self.assertEqual(self.service._get_quantize_format("10.000"), Decimal(".001"))
        self.assertEqual(self.service._get_quantize_format("10.00"), Decimal(".01"))
        self.assertEqual(self.service._get_quantize_format("10.0"), Decimal(".1"))
        self.assertEqual(self.service._get_quantize_format("10"), Decimal("0"))
    
    def test__validate_checkout_step(self):
        mock_resp = Mock()
        mock_resp.data = {}
        
        with self.assertRaises(Http404):
            self.service._validate_checkout_step(mock_resp)
        
        mock_resp.data = {"pre_order": {"shipping_option": None}}
        with self.assertRaises(Http404):
            self.service._validate_checkout_step(mock_resp)

        mock_resp.data = {
            "context_list": [{"page_name": "ShippingOptionSelectionPage"}],
            "pre_order": {
                "shipping_option": {
                    "pk": 2,
                    "name": "Yurtici Kargo",
                    "slug": "yurtici",
                    "logo": None,
                    "shipping_amount": "9.99",
                    "description": None,
                    "kwargs": {}
                        }
                }
        }
        with self.assertRaises(Http404):
            self.service._validate_checkout_step(mock_resp)
            
        mock_resp.data = {
            "context_list": [{"page_name": "PaymentOptionSelectionPage"}],
            "pre_order": {
                "shipping_option": {
                    "pk": 2,
                    "name": "Yurtici Kargo",
                    "slug": "yurtici",
                    "logo": None,
                    "shipping_amount": "9.99",
                    "description": None,
                    "kwargs": {}
                },
                 "unpaid_amount": 10,
            },
        }
        self.service._validate_checkout_step(mock_resp)
