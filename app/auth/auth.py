#!/usr/bin/env python3

from flask import Blueprint, redirect, url_for, session, flash, render_template
from app.models import Contributor
from app.forms import LoginForm
from flask_login import current_user, login_user, logout_user

auths = Blueprint(
    "auths", __name__, template_folder="templates"
)


@auths.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('cats.index'))
    navbar_links = (('cancel', url_for('cats.index')), )
    form = LoginForm()
    if form.validate_on_submit():
        contributor_by_name = Contributor.query.filter_by(name=form.username.data).first()
        contributor_by_email = Contributor.query.filter_by(email=form.email.data).first()
        if contributor_by_name is not None and contributor_by_name.check_password(form.password.data):
            if contributor_by_name.use_totp:
                session['id'] = contributor_by_name.id
                session['remember_me'] = form.remember_me.data
                return redirect(url_for('totps.two_factor_input'))
            else:
                login_user(contributor_by_name, remember=form.remember_me.data)
                flash("Congratulations, you are now logged in!")
                return redirect(url_for('cats.index'))
        elif contributor_by_email is not None and contributor_by_email.check_password(form.password.data):
            if contributor_by_email.use_totp:
                session['id'] = contributor_by_email.id
                session['remember_me'] = form.remember_me.data
                return redirect(url_for('totps.two_factor_input'))
            else:
                login_user(contributor_by_email, remember=form.remember_me.data)
                flash("Congratulations, you are now logged in!")
                return redirect(url_for('cats.index'))
        else:
            flash("Error Invalid Contributor (Username or Email) or Password")
            return(redirect(url_for('auths.login')))
    return render_template('login.html', title='Sign In', form=form, navbar_links=navbar_links)


@auths.route("/logout")
def logout():
    is_authenticated = current_user.is_authenticated
    logout_user()
    if is_authenticated:
        flash("Congratulations, you are now logged out!")
    return redirect(url_for('cats.index'))
