#!/usr/bin/env python3

from flask import Blueprint, redirect, url_for, flash
from flask_login import current_user
from flask import current_app
from app.models import Task, Category
from .. import db
from .reorder_priorities import reorder_priorities

movecat = Blueprint(
    "movecat", __name__, template_folder="templates"
)

toggletaskdone = Blueprint(
    "toggletaskdone", __name__, template_folder="templates"
)

deletetask = Blueprint(
    "deletetask", __name__, template_folder="templates"
)


@movecat.route("/move-cat/<int:taskid>/<int:catid>")
def move_cat(taskid, catid):
    task = Task.query.get(taskid)
    if current_user.is_anonymous or current_user.id != task.contributor_id:
        return(redirect(url_for('cats.index')))
    if bool(Category.query.get(catid)):
        category = Category.query.get(catid)
        if category.contributor_id == task.contributor_id:
            previous_catid = task.catid
            task.catid = catid
            db.session.commit()
            flash("Task {} moved!".format(taskid))
            reorder_priorities(catid, task.contributor_id, task.done, current_app.config)
            reorder_priorities(previous_catid, task.contributor_id, task.done, current_app.config)
    if task.done:
        return(redirect(url_for('tsks.hidden_tasks', category_id=task.catid)))
    else:
        return(redirect(url_for('tsks.tasks', category_id=task.catid)))


@deletetask.route("/delete-task/<int:taskid>")
def delete_task(taskid):
    task = Task.query.get(taskid)
    if current_user.is_anonymous or current_user.id != task.contributor_id:
        return(redirect(url_for('cats.index')))
    db.session.delete(task)
    db.session.commit()
    flash("Task {} deleted!".format(taskid))
    reorder_priorities(task.catid, task.contributor_id, task.done, current_app.config)
    if task.done:
        return(redirect(url_for('tsks.hidden_tasks', category_id=task.catid)))
    else:
        return(redirect(url_for('tsks.tasks', category_id=task.catid)))


@toggletaskdone.route("/toggle-task-done/<int:taskid>")
def toggle_task_done(taskid):
    task = Task.query.get(taskid)
    if current_user.is_anonymous or current_user.id != task.contributor_id:
        return(redirect(url_for('cats.index')))
    task.done = not task.done
    db.session.commit()
    reorder_priorities(task.catid, task.contributor_id, True, current_app.config)
    reorder_priorities(task.catid, task.contributor_id, False, current_app.config)
    if task.done:
        flash("Task {} unmarked done!".format(taskid))
        return(redirect(url_for('tsks.tasks', category_id=task.catid)))
    else:
        flash("Task {} marked done!".format(taskid))
        return(redirect(url_for('tsks.hidden_tasks', category_id=task.catid)))
