"""Util that calls Stripe."""

from __future__ import annotations

import json
import stripe
from typing import Optional
from pydantic import BaseModel

from .configuration import Context

from .functions import (
    create_customer,
    list_customers,
    create_product,
    list_products,
    create_price,
    list_prices,
    create_payment_link,
    create_invoice,
    create_invoice_item,
    finalize_invoice,
    retrieve_balance,
)


class StripeAPI(BaseModel):
    """ "Wrapper for Stripe API"""

    _context: Context

    def __init__(self, secret_key: str, context: Optional[Context]):
        super().__init__()

        self._context = context if context is not None else Context()

        stripe.api_key = secret_key
        stripe.set_app_info(
            "stripe-agent-toolkit-python",
            version="0.2.0",
            url="https://github.com/stripe/agent-toolkit",
        )

    def run(self, method: str, *args, **kwargs) -> str:
        if method == "create_customer":
            return json.dumps(create_customer(self._context, *args, **kwargs))
        elif method == "list_customers":
            return json.dumps(list_customers(self._context, *args, **kwargs))
        elif method == "create_product":
            return json.dumps(create_product(self._context, *args, **kwargs))
        elif method == "list_products":
            return json.dumps(list_products(self._context, *args, **kwargs))
        elif method == "create_price":
            return json.dumps(create_price(self._context, *args, **kwargs))
        elif method == "list_prices":
            return json.dumps(list_prices(self._context, *args, **kwargs))
        elif method == "create_payment_link":
            return json.dumps(
                create_payment_link(self._context, *args, **kwargs)
            )
        elif method == "create_invoice":
            return json.dumps(create_invoice(self._context, *args, **kwargs))
        elif method == "create_invoice_item":
            return json.dumps(
                create_invoice_item(self._context, *args, **kwargs)
            )
        elif method == "finalize_invoice":
            return json.dumps(finalize_invoice(self._context, *args, **kwargs))
        elif method == "retrieve_balance":
            return json.dumps(retrieve_balance(self._context, *args, **kwargs))
        else:
            raise ValueError("Invalid method " + method)
