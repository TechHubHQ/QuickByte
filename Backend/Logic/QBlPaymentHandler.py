from Backend.Models.QBmPaymentModel import CreatePaymentDetails
from datetime import datetime


def HandlePayment(payment_type, **kwargs):
    if payment_type == "CARD":
        # Populate details for card payment
        user_name = kwargs.get('username')
        card_number = kwargs.get('card_number')
        expiry_date = kwargs.get('expiry_date')
        cvv = kwargs.get('cvv')
        paid_amount = kwargs.get('last_paid_amount')
        print(paid_amount)
        payment_details = CreatePaymentDetails(
            user_name=user_name,
            card_number=card_number,
            expiry_date=expiry_date,
            cvv=cvv, upi_id=None,
            last_paid_amount=paid_amount,
            last_paid_on=datetime.now(),
            payment_type=payment_type,
            payment_status="Success",
            payment_mode="Card"
        )
        print(f"card payment {payment_details}")
        return {"message": "Card payment details recorded successfully"}

    elif payment_type == "UPI":
        user_name = kwargs.get('username')
        upi_id = kwargs.get('upi_id')
        paid_amount = kwargs.get('last_paid_amount')
        payment_details = CreatePaymentDetails(
            user_name=user_name,
            card_number=None,
            expiry_date=None,
            cvv=None,
            upi_id=upi_id,
            last_paid_amount=paid_amount,
            payment_type=payment_type,
            payment_status="Success",
            payment_mode="UPI",
            last_paid_on=datetime.now()
        )
        print(f"upi payment {payment_details}")
        return {"message": "UPI payment details recorded successfully"}

    else:
        return {"error": "Unsupported payment type"}
