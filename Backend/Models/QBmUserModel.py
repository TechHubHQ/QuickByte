# QBmUserModel.py

from Backend.Connections.QBcDBConnector import db, bcrypt


# QBUser Table DataBase Schema
class QBUser(db.Model):
    __tablename__ = 'qb_user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)


def ValidateUser(username, email, password, confirm_password):
    existing_username = QBUser.query.filter_by(username=username).first()
    if existing_username:
        return "Username is already taken. Please choose another."

    # Check for email uniqueness
    existing_email = QBUser.query.filter_by(email=email).first()
    if existing_email:
        return "Email is already registered. Please use another email."

    # Check password length
    if len(password) < 8:
        return "Password must be at least 8 characters long."

    # Check password complexity (you can add more checks based on your requirements)
    if not any(char.isalpha() for char in password) or not any(char.isdigit() for char in password):
        return "Password must contain both letters and numbers."

    # Check if passwords match (for sign-up)
    if confirm_password is not None and password != confirm_password:
        return "Passwords do not match."

    # If all checks pass, return None (indicating successful validation)
    return None


def CheckUser(username, password):
    user = QBUser.query.filter_by(username=username).first()
    if user and bcrypt.check_password_hash(user.password, password):
        return user
    return None


def CreateUser(username, email, password):
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    user = QBUser(username=username, email=email, password=hashed_password)
    db.session.add(user)
    db.session.commit()
