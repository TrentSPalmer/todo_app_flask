#!/usr/bin/env python3

from flask import Blueprint, url_for, redirect, render_template, flash
from flask_login import current_user
from app.models import Category, Task
from .. import db

delcat = Blueprint(
    "delcat", __name__, template_folder="templates"
)


@delcat.route("/delete_category/<int:catid>")
def delete_category(catid):
    category = Category.query.get(catid)
    if category is None:
        return(redirect(url_for('cats.index')))
    if current_user.is_anonymous or current_user.id != category.contributor_id:
        return(redirect(url_for('cats.index')))
    db.session.delete(category)
    db.session.commit()
    flash("category {} is deleted".format(category.name))
    return(redirect(url_for('hidecats.unhide_categories')))


@delcat.route("/delete-categories")
def delete_categories():
    if current_user.is_anonymous:
        return(redirect(url_for('cats.index')))
    nl = (
        ('cancel', url_for('hidecats.unhide_categories')),
        ('logout', url_for('auths.logout'))
    )
    categories = Category.query.filter_by(contributor_id=current_user.id, hidden=True).all()
    for cat in categories:
        cat.href = url_for('delcat.delete_category', catid=cat.id)
        cat.open = Task.query.filter_by(catid=cat.id, contributor_id=cat.contributor_id, done=False).count()
        cat.done = Task.query.filter_by(catid=cat.id, contributor_id=cat.contributor_id, done=True).count()

    return render_template(
        'categories.html',
        title="Category To Delete",
        navbar_links=nl,
        heading='category to delete?',
        categories=categories
    )
