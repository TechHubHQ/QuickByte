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
app.config['SERVER_NAME'] = 'localhost:5000'  # Adjust this based on your setup

mail = Mail(app)


def SendWelcomeEmail(email_id, user_name):
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
