# ===============================================================================================================
# Module for defining the PaymentDetails class and related functions.

# This module contains the definition of the PaymentDetails class, which represents payment details
# in the database. It also includes a function for creating new payment details entries in the database.

# The PaymentDetails class maps to the 'payment_details' table in the database.

# ===============================================================================================================


# =============================================================================
# Imports/Packages
# =============================================================================
from Backend.Connections.QBcDBConnector import db


# =================================================================
# PaymentDetails table Database schema
# =================================================================
class PaymentDetails(db.Model):
    """
    Model class for representing payment details in the database.

    Attributes:
        id (int): The primary key ID of the payment details entry.
        user_name (str): The username associated with the payment details.
        card_number (str): The card number associated with the payment.
        expiry_date (str): The expiry date of the payment card.
        cvv (str): The CVV of the payment card.
        upi_id (str): The UPI ID associated with the payment.
        last_paid_on (datetime): The datetime of the last payment made.
        last_paid_amount (float): The amount of the last payment made.
        payment_type (str): The type of payment.
        payment_status (str): The status of the payment.
        payment_mode (str): The mode of payment.
    """
    
    __tablename__ = 'payment_details'
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(50))
    card_number = db.Column(db.String(50))
    expiry_date = db.Column(db.String(50))
    cvv = db.Column(db.String(50))
    upi_id = db.Column(db.String(50))
    last_paid_on = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())
    last_paid_amount = db.Column(db.Float)
    payment_type = db.Column(db.String(50))
    payment_status = db.Column(db.String(50))
    payment_mode = db.Column(db.String(50))


# =========================================================================================================
# CreatePaymentDetails() --> creates a new payment details entry in the database.
# =========================================================================================================
def CreatePaymentDetails(user_name, card_number, expiry_date, cvv, upi_id, last_paid_on, last_paid_amount, payment_type,
                         payment_status, payment_mode):
    """
    Creates a new payment details entry in the database.

    Args:
        user_name (str): The username associated with the payment details.
        card_number (str): The card number associated with the payment.
        expiry_date (str): The expiry date of the payment card.
        cvv (str): The CVV of the payment card.
        upi_id (str): The UPI ID associated with the payment.
        last_paid_on (datetime): The datetime of the last payment made.
        last_paid_amount (float): The amount of the last payment made.
        payment_type (str): The type of payment.
        payment_status (str): The status of the payment.
        payment_mode (str): The mode of payment.

    Returns:
        None
    """
    
    payment_details = PaymentDetails(user_name=user_name,
                                     card_number=card_number,
                                     expiry_date=expiry_date,
                                     cvv=cvv,
                                     upi_id=upi_id,
                                     last_paid_on=last_paid_on,
                                     last_paid_amount=last_paid_amount,
                                     payment_type=payment_type,
                                     payment_status=payment_status,
                                     payment_mode=payment_mode)
    db.session.add(payment_details)
    db.session.commit()
