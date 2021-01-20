#!/usr/bin/env python3

from flask import Blueprint, url_for, render_template, redirect
from flask_login import current_user
from app.models import Category, Task

cats = Blueprint(
    "cats", __name__, template_folder="templates"
)


@cats.route("/move-categories/<int:taskid>")
def move_categories(taskid):
    task = Task.query.get(taskid)
    if task is None:
        return(redirect(url_for('cats.index')))
    if current_user.is_anonymous or current_user.id != task.contributor_id:
        return(redirect(url_for('cats.index')))
    cu = 'tsks.{}tasks'.format('hidden_' if task.done else '')
    cancel_nav_link = ('cancel', url_for(cu, category_id=task.catid))
    nl = (cancel_nav_link, )
    categories = Category.query.filter(Category.contributor_id == current_user.id, Category.id != task.catid).all()
    for cat in categories:
        cat.href = url_for('movecat.move_cat', taskid=taskid, catid=cat.id)
        cat.open = Task.query.filter_by(catid=cat.id, contributor_id=cat.contributor_id, done=False).count()
        cat.done = Task.query.filter_by(catid=cat.id, contributor_id=cat.contributor_id, done=True).count()

    return render_template(
        'categories.html',
        title="Move to",
        navbar_links=nl,
        heading='move to?',
        categories=categories
    )


@cats.route("/index")
@cats.route("/")
def index():
    if current_user.is_anonymous:
        navbar_links = (('login', url_for('auths.login')), )
        return render_template('categories.html', title="Todo", navbar_links=navbar_links)
    nl = (
        ('prof', url_for('prof.edit_profile')),
        ('new', url_for('new_cat.new_category')),
        ('hide', url_for('hidecats.hide_categories')),
        ('logout', url_for('auths.logout'))
    )
    categories = Category.query.filter_by(contributor_id=current_user.id, hidden=False).all()
    for cat in categories:
        cat.href = url_for('tsks.tasks', category_id=cat.id)
        cat.open = Task.query.filter_by(catid=cat.id, contributor_id=cat.contributor_id, done=False).count()
        cat.done = Task.query.filter_by(catid=cat.id, contributor_id=cat.contributor_id, done=True).count()

    return render_template(
        'categories.html',
        title="Categories",
        navbar_links=nl,
        heading='categories',
        categories=categories
    )
