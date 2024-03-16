# =============================================================================================================
# This script sets up a Flask application with email sending capabilities using the Flask-Mail extension.
# It configures the SMTP server settings and provides a function to send a welcome email to new users.

# The main elements of this script are:

# 1. Flask application setup with email server configuration.
# 2. Mail extension initialization.
# 3. SendWelcomeEmail function to send a welcome email with an HTML template and an attached PDF file.
# 4. A main block to test the SendWelcomeEmail function with a sample user email and username.

# This script can be integrated into a larger application or used as a standalone email sending utility.
# It demonstrates how to configure Flask-Mail, render HTML templates, and attach files to email messages.
# =============================================================================================================


# ==================================================================
# Imports/Packages
# ==================================================================
from flask import Flask, render_template
from flask_mail import Mail, Message
from pathlib import Path

app = Flask(__name__, template_folder='Email')
app.config['MAIL_SERVER'] = 'sandbox.smtp.mailtrap.io'
app.config['MAIL_PORT'] = 2525
app.config['MAIL_USERNAME'] = '84bf29d19067ee'
app.config['MAIL_PASSWORD'] = '73948546b0301c'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['SERVER_NAME'] = 'localhost:8080'

mail = Mail(app)


# ========================================================================================================
# SendWelcomeEmail() --> function to send a welcome email with an HTML template and an attached PDF file.
# ========================================================================================================
def SendWelcomeEmail(email_id, user_name):
    """
    Sends a welcome email to the provided email address with the user's name and an attached PDF guide.

    Args:
        email_id (str): The email address of the user to send the welcome email to.
        user_name (str): The name of the user to be included in the email.

    This function performs the following tasks:
    1. Creates a new email message with the subject "Welcome to QuickByte!"
    2. Renders an HTML template named "WelcomeEmailTemplate.html" with the provided user_name.
    3. Constructs the path to a PDF file named "QuickByteGuide.pdf" in the "Docs" directory.
    4. Attaches the PDF file to the email message.
    5. Sends the email using the configured SMTP server settings.
    6. Prints a success message if the email is sent successfully.
    7. Prints an error message if an exception occurs during the email sending process.

    Note: This function assumes that the Flask application context is active before calling it.
    """
    
    try:
        msg = Message('Welcome to QuickByte!', sender='quickbyte172@gmail.com', recipients=[email_id])

        # Render the HTML template
        html_body = render_template('WelcomeEmailTemplate.html', username=user_name)
        msg.html = html_body

        # Construct the dynamic path to the guide file
        guide_filename = 'QuickByteGuide.pdf'  # Change this to the actual filename
        guide_path = Path(__file__).resolve().parent.parent.parent / 'Docs' / guide_filename

        # Attach the guide file
        with app.open_resource(str(guide_path)) as guide:
            msg.attach(guide_filename, 'application/pdf', guide.read())

        # Send the email
        mail.send(msg)
        print('Email sent successfully!')
    except Exception as e:
        print(f'Error sending email: {e}')


if __name__ == '__main__':
    user_email = "kalyankanuri497@gmail.com"
    username = "Kalyan"

    with app.app_context():
        SendWelcomeEmail(user_email, username)
