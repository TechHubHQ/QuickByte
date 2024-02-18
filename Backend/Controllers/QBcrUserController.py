import os
from datetime import datetime
from werkzeug.utils import secure_filename
from flask import current_app


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