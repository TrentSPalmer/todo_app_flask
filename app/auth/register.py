#!/usr/bin/env python3

import psycopg2
from flask import Blueprint, redirect, url_for, flash, render_template
from flask_login import current_user
from app.forms import RegistrationForm
from app.models import Contributor
from flask import current_app as app
from .. import db

reg = Blueprint(
    "reg", __name__, template_folder="templates"
)


@reg.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('cats.index'))
    form = RegistrationForm()
    nl = (('cancel', url_for('auths.login')), )
    if form.validate_on_submit():
        set_contributor_id_seq()
        contributor = Contributor(name=form.username.data, email=form.email.data)
        contributor.set_password(form.password.data)
        db.session.add(contributor)
        db.session.commit()
        flash("Congratulations, you are now a registered user!")
        return redirect(url_for('auths.login'))
    return render_template('register.html', title='Register', form=form, navbar_links=nl)


def set_contributor_id_seq():
    conn = psycopg2.connect(
        dbname=app.config['DATABASE_NAME'],
        user=app.config['DATABASE_USER'],
        host=app.config['DATABASE_HOST'],
        password=app.config['DATABASE_PASSWORD']
    )

    cur = conn.cursor()
    cur.execute("SELECT setval('contributor_id_seq', (SELECT MAX(id) FROM contributor))")
    conn.commit()
    conn.close()
