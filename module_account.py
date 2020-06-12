from flask_app import app, load_user, db, Teacher, Student, send_confirmation_email, EMAIL_CONFIRMATION_SALT, RESET_PASSWORD_SALT, send_reset_password_email

from flask_login import current_user, login_user, login_required, logout_user
from flask import redirect, render_template, url_for, request, flash
from werkzeug.security import generate_password_hash
from itsdangerous import URLSafeTimedSerializer

from datetime import datetime

################################################################################
# Definition of account parameters (password, email, etc)
# Definition of login page
################################################################################



@app.route("/account/login/", methods=["GET", "POST"])
def login():
    template_html = "account/login.html"
    logout_user()
    if request.method == "GET":
        return render_template(template_html)

    user = load_user(request.form["username"])
    invalid_msg = "Utilisateur ou mot de passe incorrect"
    if user is None:
        flash(invalid_msg)
        return render_template(template_html)

    if not user.check_password(request.form["password"]):
        flash(invalid_msg)
        return render_template(template_html)

    if not user.email_confirmed:
        send_confirmation_email(user.email)
        flash("email de confirmation envoyé")
        return redirect(url_for('index'))

    login_user(user)
    user.last_connection = datetime.now()
    db.session.commit()
    flash(f"Bonjour {user.name} {user.surname}")
    return redirect(url_for('index'))


@app.route("/account/reset-password/", methods=["GET", "POST"])
def reset_password():
    if request.method == "GET":
        return render_template("account/reset_password.html")
    user = load_user(request.form["username"])
    if user is None:
        flash("Adresse mail incorrecte")
        return redirect(url_for("reset_password"))
    if not user.email_confirmed:
        send_confirmation_email(user.email)
        flash("Vous devez d'abord confirmer votre adresse email. Un email de confirmation vient de vous être envoyé")
        return redirect(url_for('login'))
    send_reset_password_email(user.email)
    flash("Un lien de réinitialisation de votre mot de passe vient de vous être envoyé par email")
    return redirect(url_for('login'))

@app.route("/account/reset-password/<token>/", methods=["GET", "POST"])
def reset_password_token(token):
    try:
        confirm_serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
        email = confirm_serializer.loads(token, salt=RESET_PASSWORD_SALT, max_age=3600*24)
    except:
        flash('Le lien est invalide ou a expiré.')
        return redirect(url_for('login'))

    if request.method == "GET":
        flash(f"Bonjour {email}")
        return render_template("account/reset_password_token.html")
    elif request.method == "POST":
        user = load_user(email)
        user.password_hash = generate_password_hash(request.form["password"])
        db.session.commit()
        flash('Votre mot de passe a été modifié !')
        return redirect(url_for('login'))

@app.route("/account/confirm-email/<token>/")
def confirm_email(token):
    try:
        confirm_serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
        email = confirm_serializer.loads(token, salt=EMAIL_CONFIRMATION_SALT, max_age=3600*24)
    except:
        flash('Le lien est invalide ou a expiré. Connectez-vous afin de recevoir un nouveau lien de validation par email.')
        return redirect(url_for('login'))

    user = load_user(email)

    if user.email_confirmed:
        flash('Email déjà confirmé')
    else:
        user.email_confirmed = True
        user.email_confirmed_on = datetime.now()
        #db.session.add(user)
        db.session.commit()
        flash('Votre adresse mail est confirmée !')
    return redirect(url_for('login'))


def _create_account(User):
    template_html = "account/create_account.html"
    if request.method == "GET":
        return render_template(template_html)
    user = load_user(request.form["email"])
    invalid_msg = "Un utilisateur est déjà enregistré à cette adresse email"
    if user is not None:
        logout_user()
        flash(invalid_msg)
        return render_template(template_html)
    try:
        user = User(
            username=request.form["email"],
            email=request.form["email"],
            name=request.form["name"],
            surname=request.form["surname"],
            password_hash=generate_password_hash(request.form["password"]),
            email_confirmed=False
        )
        db.session.add(user)
        db.session.commit()
        send_confirmation_email(request.form["email"])
    except Exception as e:
        print('Account creation error', e)
        flash("Unknown error")

        return render_template(template_html)
    flash("Votre compte a été créé. Un lien de vérification vient de vous être envoyé par email (penser à aussi vérifier les spams).")
    return redirect(url_for('index'))


@app.route("/account/create-account/", methods=["GET", "POST"])
def create_account():
    return _create_account(User=Student)

@app.route("/account/create-account-admin/", methods=["GET", "POST"])
def create_account_admin():
    flash("Création d'un compte professeur")
    return _create_account(User=Teacher)


@app.route("/account/")
def account():
    template_html = "account/index.html"
    return render_template(template_html)

@app.route("/account/logout/")
@login_required
def logout():
    logout_user()
    flash("Vous êtes déconnecté")
    return redirect(url_for('index'))


@app.route("/account/change-psswrd/", methods=["GET", "POST"])
@login_required
def change_psswrd():
    template_html = "account/change_psswrd.html"
    if request.method == "GET":
        return render_template(template_html)

    if not current_user.check_password(request.form["old_password"]):
        flash("Mot de passe incorrect")
        return render_template(template_html)

    # send a SQL request to change the password hash
    current_user.password_hash = generate_password_hash(request.form["new_password"])
    db.session.commit()
    flash("Mot de passe changé")
    return redirect(url_for('account'))