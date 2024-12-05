import secrets
import hashlib
import json

from yoomoney_payment.commerce import conf 

from django.conf import settings
from django.http import Http404
from importlib import import_module


module, _class = settings.PZ_SERVICE_CLASS.rsplit(".", 1)
Service = getattr(import_module(module), _class)


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
        
    
    def _get_basket_items(self, request):
        response = self._retrieve_pre_order(request)
         
        if "pre_order" not in response.data:
            raise Http404
         
        basket_items = response.data["pre_order"]["basket"]["basketitem_set"]
        return [
            {
                "amount": item["total_amount"],
                "product_name": self._get_product_name(item["product"]["name"])
            }
            for item in basket_items
        ]

    def _retrieve_pre_order(self, request):
        path = "/orders/checkout/"
        response = self.get(
            path, request=request, headers={"X-Requested-With": "XMLHttpRequest"}
        )
        return self.normalize_response(response)
