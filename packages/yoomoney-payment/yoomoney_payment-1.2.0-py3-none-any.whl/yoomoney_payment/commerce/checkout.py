import secrets
import hashlib
import json
import logging
from decimal import Decimal, ROUND_DOWN

from yoomoney_payment.commerce import conf 

from django.conf import settings
from django.http import Http404
from importlib import import_module


module, _class = settings.PZ_SERVICE_CLASS.rsplit(".", 1)
Service = getattr(import_module(module), _class)

logger = logging.getLogger(__name__)


class CheckoutService(Service):
    def get_data(self, request):
        salt = self.generate_salt()
        session_id = request.GET.get("sessionId")
        
        hash_ = self.generate_hash(session_id, salt)
        basket_items = self._get_basket_items(request)

        return {
            "hash": hash_,
            "salt": salt,
            "data": json.dumps({"order_items": basket_items}),
        }

    def generate_salt(self):
        salt = secrets.token_hex(10)
        return salt

    def generate_hash(self, session_id, salt):
        hash_key = conf.HASH_SECRET_KEY
        return hashlib.sha512(
            f"{salt}|{session_id}|{hash_key}".encode("utf-8")
        ).hexdigest()

    def _get_product_name(self, product_name):
        if not product_name:
            product_name = "none"
        return product_name if len(product_name) <= 255 else product_name[:255]
  
    def _validate_checkout_step(self, response):
        if "pre_order" not in response.data:
            raise Http404()
        
        if response.data["pre_order"].get("shipping_option") is None:
            raise Http404()
        
        page_names = [page["page_name"] for page in response.data["context_list"]]
        if "PaymentOptionSelectionPage" not in page_names:
            raise Http404()
    
    def _find_decimal_places(self, price):
        if '.' in price:
            return len(price.split('.')[1])
        return 0
    
    def _get_quantize_format(self, price_as_string):
        decimal_places = self._find_decimal_places(price_as_string)
        if decimal_places == 0:
            return Decimal(0)
        quantize_format = Decimal(f".{'0' * (decimal_places-1)}1")
        return quantize_format
    
    def _get_basket_items(self, request):
        response = self._retrieve_pre_order(request)
        self._validate_checkout_step(response=response)
        unpaid_amount = Decimal(response.data["pre_order"].get("unpaid_amount", 0))

        if unpaid_amount == Decimal(0):
            logger.info("Yoomoney Payment Unpaid amount is Zero")
            return []

        response_basket_items = response.data["pre_order"]["basket"]["basketitem_set"]
        quantize_format = self._get_quantize_format(response.data["pre_order"]["unpaid_amount"])
        total_product_amount = Decimal(response.data["pre_order"]["basket"]["total_product_amount"])
        remaining_amount = unpaid_amount - total_product_amount

        basket_items = []
        cumulative_amount = Decimal(0)

        for index, item in enumerate(response_basket_items):
            basket_item_amount = Decimal(item["total_amount"])
            weight = basket_item_amount / total_product_amount
            amount = (remaining_amount * weight + basket_item_amount).quantize(quantize_format, ROUND_DOWN)
            cumulative_amount += amount

            if index == len(response_basket_items) - 1:
                # Adjust the amount for the last item to ensure the total matches unpaid amount
                delta = unpaid_amount - cumulative_amount
                amount = amount + delta

            basket_items.append({
                "amount": str(amount),
                "product_name": self._get_product_name(item["product"]["name"])
            })

        return basket_items

    def _retrieve_pre_order(self, request):
        path = "/orders/checkout/"
        response = self.get(
            path, request=request, headers={"X-Requested-With": "XMLHttpRequest"}
        )
        return self.normalize_response(response)
