import logging

from django.http import Http404
from django.views.generic import View
from django.template.response import TemplateResponse

from yoomoney_payment.commerce.checkout import CheckoutService
from yoomoney_payment.forms import YooMoneyForm
from yoomoney_payment.commerce import conf


logger = logging.getLogger(__name__)


class YooMoneyPaymentView(View):
    checkout_service = CheckoutService()

    def get(self, request):
        if not conf.YOOMONEY_EXTENSION_URL:
            logging.exception("Missing YOOMONEY_EXTENSION_URL")            
            raise Http404
        
        data = self.checkout_service.get_data(request)
        session_id = request.GET.get("sessionId")
  
        yoo_money_form = YooMoneyForm(
            initial=data
        )

        return TemplateResponse(
            request=request,
            template="yoomoney_payment.html",
            context={
                "action_url": f"{conf.YOOMONEY_EXTENSION_URL}/form-page?sessionId={session_id}",
                "action_method": "POST",
                "yoo_money_form": yoo_money_form,
            },
        )
