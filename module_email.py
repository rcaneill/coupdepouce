from flask_app import app, url_for, render_template, mail
from flask_mail import Message

from smtplib import SMTPRecipientsRefused
from flask import flash
from itsdangerous import URLSafeTimedSerializer

EMAIL_CONFIRMATION_SALT="ladnv98768whBSDV84W79EFHONCJnhju756y5tergdfbngjmhngfgeR"
RESET_PASSWORD_SALT="hbgfyui89tyughujknbhgfyt687uoijoJOIUY76TYGTY6789IOLKl,cvf"

def send_email(subject, recipients, text_body, html_body):
    msg = Message(subject, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    mail.send(msg)


def send_confirmation_email(user_email):
    confirm_serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])

    confirm_url = url_for(
        'confirm_email',
        token=confirm_serializer.dumps(user_email, salt=EMAIL_CONFIRMATION_SALT),
        _external=True)

    html = render_template(
        'email/email_address_confirmation.html',
        confirm_url=confirm_url)
    msg = Message(
        '[coupdepouce] Confirmer votre adresse email',
        sender=app.config['MAIL_SENDER'],
        recipients=[user_email]
    )
    msg.html = html
    with app.app_context():
        try:
            mail.send(msg)
        except SMTPRecipientsRefused:
            flash("Adresse email invalide")


def send_reset_password_email(user_email):
    confirm_serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])

    reset_url = url_for(
        'reset_password_token',
        token=confirm_serializer.dumps(user_email, salt=RESET_PASSWORD_SALT),
        _external=True)

    html = render_template(
        'email/email_reset_password.html',
        reset_url=reset_url)
    msg = Message(
        '[coupdepouce] Réinitialiser votre mot de passe',
        sender=app.config['MAIL_SENDER'],
        recipients=[user_email]
    )
    msg.html = html
    with app.app_context():
        mail.send(msg)