#!/usr/bin/env python3

import psycopg2
from flask import Blueprint, redirect, url_for, flash, render_template
from flask import current_app as app
from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Regexp
from app.models import Category

new_cat = Blueprint(
    "new_cat", __name__, template_folder="templates"
)


def insert_category(category):
    conn = psycopg2.connect(
        dbname=app.config['DATABASE_NAME'],
        user=app.config['DATABASE_USER'],
        host=app.config['DATABASE_HOST'],
        password=app.config['DATABASE_PASSWORD']
    )
    cur = conn.cursor()
    cur.execute("SELECT setval('category_id_seq', (SELECT MAX(id) FROM category))")
    conn.commit()
    cur.execute("SELECT count(id) FROM category WHERE name=%s AND contributor_id=%s", (category.name, category.contributor_id))
    if cur.fetchone()[0] == 0:
        cur.execute("INSERT INTO category(name, contributor_id) VALUES(%s, %s)", (category.name, category.contributor_id))
        conn.commit()
    conn.close


@new_cat.route("/new-category", methods=["GET", "POST"])
def new_category():
    if current_user.is_anonymous:
        return(redirect(url_for('cats.index')))
    form = NewCategory()
    nl = (('cancel', url_for('cats.index')), )
    if form.validate_on_submit():
        category = Category(name=form.name.data, contributor_id=current_user.id)
        insert_category(category)
        flash("Thanks for the new category!")
        return(redirect(url_for('cats.index')))
    return render_template('new_category.html', title='New Category', form=form, navbar_links=nl)


class NewCategory(FlaskForm):
    name = StringField(
        'New Task Category',
        validators=[
            DataRequired(),
            Regexp('^[a-zA-Z0-9\\s-]+$', message='dashes, digits, and spaces are ok')
        ],
        render_kw={'autofocus': True}
    )
    submit = SubmitField('Save')
