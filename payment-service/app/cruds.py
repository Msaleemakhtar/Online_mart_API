from sqlmodel import Session, select
from app.model import Payment, PaymentStatus
from datetime import datetime
from uuid import UUID





def get_payment_by_order_id(db: Session, order_id: UUID) -> Payment:
    statement = select(Payment).where(Payment.order_id == order_id)
    return db.exec(statement).first()

def get_all_payments(db) -> Payment:
    statement = select(Payment)
    return db.exec(statement).all()

def create_or_update_payment(db: Session, order_id: str, amount: int, currency: str, user_email: str, status: str, checkout_session_id: str):
    # Example function to create or update payment record
    # This is a simplified example, adjust as per your actual data model and business logic

    # Check if payment record exists
    existing_payment = db.exec(select(Payment).where(Payment.order_id == order_id)).first()
    if existing_payment:
        # Update existing payment record
        existing_payment.total_price = amount
        existing_payment.currency = currency
        existing_payment.user_email = user_email
        existing_payment.status = PaymentStatus[status.upper()]  # Convert status string to enum
        existing_payment.updated_at = datetime.now()
    else:
        # Create new payment record
        new_payment = Payment(
            order_id=order_id,
            total_price=amount,
            currency=currency,
            user_email=user_email,
            status=PaymentStatus[status.upper()],  # Convert status string to enum
            checkout_session_id=checkout_session_id
        )
        db.add(new_payment)

    db.commit()
    db.refresh(new_payment if not existing_payment else existing_payment)

    return new_payment if not existing_payment else existing_payment