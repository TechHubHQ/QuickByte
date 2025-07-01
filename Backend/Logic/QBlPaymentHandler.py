# ================================================================================================
# This script provides functionality to handle different payment methods and
# record payment details in a database.

# The script imports the necessary functions and models from other modules:
# - CreatePaymentDetails from Backend.Models.QBmPaymentModel is used to create
#   and save payment details in the database.
# - datetime is used to record the timestamp of the payment.

# The main functionality is encapsulated in the HandlePayment function, which takes the payment type
# and associated payment details as input.
# ================================================================================================

# ===============================================================
# Imports/Packages
# ===============================================================

from Backend.Models.QBmPaymentModel import CreatePaymentDetails
from datetime import datetime


# ============================================================================
# HandlePayment -- creates entry into DB as per payment method
# =============================================================================

def HandlePayment(payment_type, **kwargs):
    """
    Handles payment processing and recording of payment details based on the provided payment type.

    Args:
        payment_type (str): The type of payment, either "CARD" or "UPI".
        **kwargs: Additional keyword arguments containing payment details specific to the payment type.
            For "CARD" payment:
                - username (str): The name of the user making the payment.
                - card_number (str): The card number used for payment.
                - expiry_date (str): The expiry date of the card.
                - cvv (str): The CVV code of the card.
                - last_paid_amount (float): The amount paid.
            For "UPI" payment:
                - username (str): The name of the user making the payment.
                - upi_id (str): The UPI ID used for payment.
                - last_paid_amount (float): The amount paid.

    Returns:
        dict: A dictionary containing a success message if the payment details were recorded successfully,
              or an error message if the payment type is unsupported.
    """

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
        return {"message": "UPI payment details recorded successfully"}

    else:
        return {"error": "Unsupported payment type"}
