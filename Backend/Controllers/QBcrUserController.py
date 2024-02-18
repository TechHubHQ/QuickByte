import os
from werkzeug.utils import secure_filename
from flask import current_app
from Backend.Models.QBmUserModel import QBUser
from Backend.Models.QBmAddressModel import Address
from Backend.Models.QBmNotificationModel import NotificationControl
from Backend.Connections.QBcDBConnector import db, bcrypt


class UserController:
    @staticmethod
    def SaveImage(username, image_file):
        if image_file:
            original_file = secure_filename(image_file.filename)
            file_extension = original_file.split(".")[-1]
            username = username.replace(" ", "_")
            new_file = f"{username}.{file_extension}"
            image_file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], new_file))
            print(f"Image saved to {current_app.config['UPLOAD_FOLDER']}")
        else:
            print("No image selected")

    @staticmethod
    def UpdateUser(username, password):
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        QBUser.query.filter_by(username=username).update({"password": hashed_password})
        db.session.commit()

    @staticmethod
    def UpdatePreferences(username, flag):
        user = NotificationControl.query.filter_by(username=username).first()
        if user is None:
            user = NotificationControl(username=username, notify_flag=flag)
            db.session.add(user)
            db.session.commit()
        else:
            NotificationControl.query.filter_by(username=username).update({"notify_flag": flag})
            db.session.commit()

    @staticmethod
    def UpdateDelivery(email, line1, landmark, state, district, preferred_delv_start_time, preferred_delv_end_time):
        Address.query.filter_by(email=email).update({
            "line1": line1,
            "landmark": landmark,
            "state": state,
            "district": district,
            "preferred_delv_start_time": preferred_delv_start_time,
            "preferred_delv_end_time": preferred_delv_end_time
        })
        db.session.commit()
