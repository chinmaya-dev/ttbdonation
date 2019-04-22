from flask import render_template, url_for, flash, redirect, request, redirect, g, current_app, Markup
import os
from flask_login import login_user, current_user, logout_user, login_required
from .. import db, bcrypt
import secrets
from werkzeug.urls import url_parse
from flask_dance.consumer.backend.sqla import SQLAlchemyBackend
from . import bp, batman_example, googlex
from flask_dance.contrib.google import google
from ..decorators import admin_required, permission_required
from .email import send_reset_email
from datetime import datetime
from sqlalchemy import and_
from ..models import User, Role, Permission, OAuth, Rewards
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_dance.consumer import oauth_authorized
from .forms import (SignUpForm, LoginForm, RequestResetForm, WelcomeForm, ResetPasswordForm, ProtagonistCatForm, ProtagonistSubCatASportsForm,
                    ProtagonistSubCatSportsForm, ProtagonistSubCatMusicForm, WTKForm)
from app.main.forms import SearchForm
from sqlalchemy.orm.exc import NoResultFound

batman_example.backend = SQLAlchemyBackend(
    OAuth, db.session, user=current_user, user_required=False)

googlex.backend = SQLAlchemyBackend(
    OAuth, db.session, user=current_user, user_required=False)


@bp.route("/register", methods=['GET', 'POST'])
def register():
    form = SignUpForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data,
                    password=hashed_password,  tandc=form.tandc.data)
        db.session.add(user)
        db.session.commit()
        message = Markup(
            '''Welcome! to THE TRIBAL BOX the one stop Platform please update your profile and choose your <a href="/role">role</a>''')
        flash(message, 'success')
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
        re = Rewards.query.filter_by(user_id=user.id).first()
        try:
            if re.action != "sign up":
                random_hex = secrets.token_hex(8)
                rewards = Rewards(points=10, action="sign up",address=random_hex, Protagonist=user)
                db.session.add(rewards)
                db.session.commit()
        except:
            if re == None:
                random_hex = secrets.token_hex(8)
                rewards = Rewards(points=10, action="sign up",address=random_hex, Protagonist=user)
                db.session.add(rewards)
                db.session.commit()
            return redirect(url_for('main.home'))
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('auth/register.html', title='Register', form=form)

@bp.route('/facebook')
def facebook():
    if not batman_example.session.authorized:
        return redirect(url_for("batman-example.login"))
    resp = batman_example.session.get("me")
    assert resp.ok
    return resp.text


@oauth_authorized.connect_via(batman_example)
def facebook_logged_in(blueprint, token):

    account_info = blueprint.session.get('me')
    email_a = blueprint.session.get('me?fields=email')
    if email_a.ok:
        email_a_json = email_a.json()
        email = email_a_json["email"]

    if account_info.ok:
        account_info_json = account_info.json()
        username = account_info_json["name"]
        password = account_info_json["id"]
        

        query = User.query.filter_by(username=username)

        try:
            user = query.one()
        except NoResultFound:
            user = User(username=username,
                        password=password,
                        email=email
                        )
            db.session.add(user)
            db.session.commit()
            flash('Welcome to THE TRIBAL BOX the one stop Platform please update your profile and choose your role in our platform', 'success')
        login_user(user)
        return redirect(url_for('main.home'))


@bp.route('/googlelogin')
def googlelogin():
    if not google.authorized:
        return redirect(url_for("google.login"))
    resp = google.get("/oauth2/v2/userinfo")
    assert resp.ok
    return resp.text


@oauth_authorized.connect_via(googlex)
def google_logged_in(blueprint, token):

    account_info = blueprint.session.get('/oauth2/v2/userinfo')

    if account_info.ok:
        account_info_json = account_info.json()
        username = account_info_json["name"]
        password = account_info_json["id"]
        email = account_info_json["email"]

        query = User.query.filter_by(username=username)

        try:
            user = query.one()
        except NoResultFound:
            user = User(username=username,
                        password=password,
                        email=email
                        )
            db.session.add(user)
            db.session.commit()
            flash('Welcome to THE TRIBAL BOX the one stop Platform please update your profile and choose your role in our platform', 'success')
        login_user(user)
        return redirect(url_for('main.home'))





# Now we are going to use the Blueprint we have created in the __init__.py file in auth directory
@bp.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        g.search_form = SearchForm()
        db.session.commit()




@bp.route('/admin')
@login_required
@admin_required
def for_admins_only():
    return "For administrators!"

@bp.route('/moderate')
@login_required
@permission_required(Permission.MODERATE)
def for_moderators_only():
    return "For comment moderators!"




@bp.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
            return redirect(url_for('donation.donation_view'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        re = Rewards.query.filter_by(user_id=user.id).first()       
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            try:
                if  re.action!="login" :
                    random_hex = secrets.token_hex(8)
                    rewards = Rewards(points=4, action="login", address=random_hex, Protagonist=user)
                    db.session.add(rewards)
                    db.session.commit()
            except:
                if re == None:
                    random_hex = secrets.token_hex(8)
                    rewards = Rewards(points=4, action="login",address=random_hex, Protagonist=user)
                    db.session.add(rewards)
                    db.session.commit()
            if user.is_role == "Creators":
                return redirect(url_for('donation.donation_view'))
            if user.is_role == "Brand":
                return redirect(url_for('donation.donation_view'))
            if user.is_role == "Mentor":
                return redirect(url_for('donation.donation_view'))
            else:
                return redirect(url_for('donation.donation_view'))
    return render_template('auth/login.html', title='Sign In', form=form)


@bp.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.landing'))


# This part of the code is related to resetting of password and other user authentication
@bp.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_request.html', title='Reset Password', form=form)


@bp.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('auth.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated! You are now able to log in', 'success')
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_token.html', title='Reset Password', form=form)
