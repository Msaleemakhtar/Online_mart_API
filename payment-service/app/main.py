import logging
from typing import Annotated, List
from uuid import UUID

from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException, Request, Header
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import stripe


from app import settings
from sqlmodel import Session
from app.db import create_db_and_tables, get_session
from app.model import Payment, PaymentRequest
from app.cruds import get_payment_by_order_id, create_or_update_payment, get_all_payments


stripe.api_key = settings.STRIPE_SECRET_KEY


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("LifeSpan Event..")
    create_db_and_tables()
    #loop = asyncio.get_event_loop()
    #loop.create_task(consume_orders())
    
    yield


app = FastAPI(lifespan=lifespan,
    title="Payment-service",
    description="Payment Microservice API allows you to manage order payment",
    version="0.0.1",
    terms_of_service="http://example.com/terms/",
    contact={
        "name": "Muhammad Saleem Akhtar",
        "email": "saleemakhtar864@gmail.com",
    },
    license_info={
        "name": "Apache 2.0",
        "identifier": "MIT",
    },
     servers=[
        {
            "url": "http://127.0.0.1:8011", # ADD NGROK URL Here Before Creating GPT Action
            "description": "Development Server"
        }
        ],
    root_path="/payment-service",
    root_path_in_servers=True
)



templates = Jinja2Templates(directory="app/templates")
# Mount the static files directory
app.mount("/static", StaticFiles(directory="app/templates"), name="static")



@app.get("/")
async def root():
    return {"Payment-service"}


@app.get("/success")
async def success(request: Request):
    return templates.TemplateResponse("success.html", {"request": request})

@app.get("/cancel")
async def cancel(request: Request):
    return templates.TemplateResponse("cancel.html", {"request": request})

#check-out session creation
@app.post("/checkout/")
async def create_checkout_session(payment_request: PaymentRequest):
    try:
        checkout_session = stripe.checkout.Session.create(
            customer_email=payment_request.user_email,
            line_items=[
                {
                    "price_data": {
                        "currency": payment_request.currency,
                        "product_data": {
                            "name": "FastAPI Stripe Checkout",
                        },
                        "unit_amount": payment_request.total_price* 100,
                    },
                    "quantity": 1,
                }
            ],
            mode="payment",
            success_url="http://localhost:8011/success",
            cancel_url="http://localhost:8011/cancel",
            metadata={
                "order_id": str(payment_request.order_id)
            }
        )
        return {"checkout_url": checkout_session.url}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# stripe webhook
@app.post("/webhook")
async def webhook_received(db:Annotated[Session, Depends(get_session)], request: Request, stripe_signature: str = Header(None)):
    webhook_secret = settings.STRIPE_WEBHOOK_SECRET
    data = await request.body()
    try:
        event = stripe.Webhook.construct_event(
            payload=data,
            sig_header=stripe_signature,
            secret=webhook_secret
        )
    except ValueError as e:
        # Invalid payload
        print(f"Invalid payload: {e}")
        raise HTTPException(status_code=400, detail="Invalid payload")
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        print(f"Invalid signature: {e}")
        raise HTTPException(status_code=400, detail="Invalid signature")
    
    event_type = event['type']
    if event_type == 'checkout.session.completed':
        session = event['data']['object']
        checkout_session_id = session['id']
        order_id = session['metadata']['order_id']
        amount = session['amount_total']/100
        currency = session['currency']
        user_email = session['customer_email']
        payment_status = session['payment_status']
      

        # Create or update payment record
        payment = create_or_update_payment(
            db,
            order_id=order_id,
            amount=amount,
            currency=currency,
            user_email=user_email,
            status=payment_status,
            checkout_session_id=checkout_session_id
        )

        return {"status": "success"}

    # Handle other event types if needed

    return {"status": "ignored"}



# Get payments by Id 
@app.get("/payments/{order_id}", response_model=dict())
def get_payment(order_id: UUID, db: Annotated[Session, Depends(get_session)]):
    return get_payment_by_order_id(db, order_id)

#Get all payments
@app.get("/payments/", response_model=List[Payment])
def get_all_payment_list(db: Annotated[Session, Depends(get_session)]):
    return get_all_payments(db)