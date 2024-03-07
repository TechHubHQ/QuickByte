from Backend.Connections.QBcDBConnector import db


class PaymentDetails(db.Model):
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


def CreatePaymentDetails(user_name, card_number, expiry_date, cvv, upi_id, last_paid_on, last_paid_amount, payment_type,
                         payment_status, payment_mode):
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
    return payment_details
