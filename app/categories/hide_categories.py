#!/usr/bin/env python3

from flask import Blueprint, redirect, url_for, render_template, flash
from flask_login import current_user
from app.models import Category, Task
from .. import db

hidecats = Blueprint(
    "hidecats", __name__, template_folder="templates"
)


@hidecats.route("/category-toggle-hidden/<int:catid>")
def category_toggle_hidden(catid):
    category = Category.query.get(catid)
    if category is None:
        return(redirect(url_for('cats.index')))
    if current_user.is_anonymous or current_user.id != category.contributor_id:
        return(redirect(url_for('cats.index')))
    category.hidden = not category.hidden
    db.session.commit()
    if category.hidden:
        flash("category {} is now hidden".format(category.name))
        return(redirect(url_for('hidecats.hide_categories')))
    else:
        flash("category {} is now unhidden".format(category.name))
        return(redirect(url_for('hidecats.unhide_categories')))


@hidecats.route("/unhide-categories")
def unhide_categories():
    if current_user.is_anonymous:
        return(redirect(url_for('cats.index')))
    if Category.query.filter_by(contributor_id=current_user.id, hidden=True).count() == 0:
        return(redirect(url_for('hidecats.hide_categories')))
    nl = (
        ('cancel', url_for('cats.index')),
        ('hide', url_for('hidecats.hide_categories')),
        ('delete', url_for('delcat.delete_categories'))
    )
    categories = Category.query.filter_by(contributor_id=current_user.id, hidden=True).all()
    for cat in categories:
        cat.href = url_for('hidecats.category_toggle_hidden', catid=cat.id)
        cat.open = Task.query.filter_by(catid=cat.id, contributor_id=cat.contributor_id, done=False).count()
        cat.done = Task.query.filter_by(catid=cat.id, contributor_id=cat.contributor_id, done=True).count()

    return render_template(
        'categories.html',
        title="Category To unHide",
        navbar_links=nl,
        heading='category to unhide?',
        categories=categories
    )


@hidecats.route("/hide-categories")
def hide_categories():
    if current_user.is_anonymous:
        return(redirect(url_for('cats.index')))
    num_hidden_cats = Category.query.filter_by(contributor_id=current_user.id, hidden=True).count()
    nl = [('cancel', url_for('cats.index')), ]
    if num_hidden_cats > 0:
        nl.append(('unhide', url_for('hidecats.unhide_categories')), )
    nl.append(('logout', url_for('auths.logout')))

    categories = Category.query.filter_by(contributor_id=current_user.id, hidden=False).all()
    for cat in categories:
        cat.href = url_for('hidecats.category_toggle_hidden', catid=cat.id)
        cat.open = Task.query.filter_by(catid=cat.id, contributor_id=cat.contributor_id, done=False).count()
        cat.done = Task.query.filter_by(catid=cat.id, contributor_id=cat.contributor_id, done=True).count()

    return render_template(
        'categories.html',
        title="Category To Hide",
        navbar_links=nl,
        heading='category to hide?',
        categories=categories
    )
