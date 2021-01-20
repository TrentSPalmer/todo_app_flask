#!/usr/bin/env python3

from flask import Blueprint, session, redirect, url_for, flash, render_template
from flask import current_app as app
from app.models import Contributor
from app.forms import GetTotp, DisableTotp, ConfirmTotp
from flask_login import current_user, login_user
from pyotp.totp import TOTP
from .totp_utils import disable_2fa, validate_totp, get_totp_qr

totps = Blueprint(
    "totps", __name__, template_folder="templates"
)


@totps.route("/two-factor-input", methods=["GET", "POST"])
def two_factor_input():
    if current_user.is_authenticated or 'id' not in session:
        return redirect(url_for('cats.index'))
    nl = (('cancel', url_for('cats.index')), )
    contributor = Contributor.query.get(session['id'])
    if contributor is None:
        return redirect(url_for('cats.index'))
    form = GetTotp()
    if form.validate_on_submit():
        if TOTP(contributor.totp_key).verify(int(form.totp_code.data), valid_window=5):
            login_user(contributor, remember=session['remember_me'])
            flash("Congratulations, you are now logged in!")
            return redirect(url_for('cats.index'))
        else:
            flash("Oops, the pin was wrong")
            form.totp_code.data = None
            return render_template('two_factor_input.html', form=form, inst="Code was wrong, try again?")
    return render_template(
        'two_factor_input.html', form=form,
        inst="Enter Auth Code", navbar_links=nl
    )


@totps.route('/disable-totp', methods=['GET', 'POST'])
def disable_totp():
    if current_user.is_anonymous or not current_user.use_totp:
        return(redirect(url_for('cats.index')))
    nl = (('cancel', url_for('prof.edit_profile')), )
    contributor = Contributor.query.get(current_user.id)
    form = DisableTotp()
    if form.validate_on_submit():
        if disable_2fa(contributor, app.config):
            flash('2FA Now Disabled')
            return(redirect(url_for('prof.edit_profile')))
        else:
            flash('2FA Not Disabled')
            return(redirect(url_for('prof.edit_profile')))
    return render_template(
        'disable_2fa.html', form=form,
        title="Disable 2FA", navbar_links=nl
    )


@totps.route('/enable-totp', methods=['GET', 'POST'])
def enable_totp():
    if current_user.is_anonymous or current_user.use_totp:
        return(redirect(url_for('cats.index')))
    nl = (('cancel', url_for('prof.edit_profile')), )
    contributor = Contributor.query.get(current_user.id)
    form = ConfirmTotp()
    qr = get_totp_qr(contributor, app.config)
    if form.validate_on_submit():
        if contributor.use_totp:
            flash('2FA Already Enabled')
            return(redirect(url_for('prof.edit_profile')))
        if validate_totp(contributor, form.totp_code.data, app.config):
            flash('2FA Now Enabled')
            return(redirect(url_for('prof.edit_profile')))
        else:
            flash("TOTP Code didn't validate, rescan and try again")
            return(redirect(url_for('prof.edit_profile')))
    return render_template(
        'qr.html', qr=qr, form=form,
        title="Aunthentication Code",
        navbar_links=nl
    )
