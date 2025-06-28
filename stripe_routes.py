import stripe
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
import os

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
stripe_router = APIRouter()
templates = Jinja2Templates(directory="templates")

@stripe_router.get("/payment", response_class=HTMLResponse)
def show_payment_page(request: Request):
    return templates.TemplateResponse("payment.html", {"request": request})

@stripe_router.post("/create-checkout-session")
def create_checkout_session():
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'product_data': {'name': 'XtremeReversal Full Access'},
                    'unit_amount': 49900,
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url="https://xtremereversal.onrender.com/success",
            cancel_url="https://xtremereversal.onrender.com/payment",
        )
        return RedirectResponse(session.url, status_code=303)
    except Exception as e:
        return {"error": str(e)}

@stripe_router.get("/success", response_class=HTMLResponse)
def payment_success(request: Request):
    return templates.TemplateResponse("success.html", {"request": request})