#!/usr/bin/env python3

from flask import Blueprint, redirect, url_for, flash, render_template
from flask_login import current_user
from app.forms import ResetPasswordRequestForm, ResetPasswordForm
from app.models import Contributor
from flask import current_app as app
from .. import db
from .email import send_password_reset_email

pwd = Blueprint(
    "pwd", __name__, template_folder="templates"
)


@pwd.route('/reset-password-request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return(redirect(url_for('cats.index')))
    nl = (('cancel', url_for('cats.index')), )
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        contributor = Contributor.query.filter_by(email=form.email.data).first()
        if contributor:
            send_password_reset_email(contributor, app.config['EXTERNAL_URL'])
            flash('Check your email for the instructions to reset your password')
            return redirect(url_for('auths.login'))
        else:
            flash('Sorry, invalid email')
            return redirect(url_for('auths.login'))
    return render_template('reset_password_request.html', title='Reset Password', form=form, navbar_links=nl)


@pwd.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('cats.index'))
    nl = (('cancel', url_for('cats.index')), )
    contributor = Contributor.verify_reset_password_token(token)
    if not contributor:
        return redirect(url_for('cats.index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        contributor.set_password(form.password.data)
        db.session.commit()
        flash('Your password has been reset.')
        return redirect(url_for('auths.login'))
    return render_template('reset_password.html', title="New Password?", form=form, navbar_links=nl)
