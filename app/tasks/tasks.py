#!/usr/bin/env python3

from flask import Blueprint, redirect, url_for, render_template
from flask_login import current_user
from app.models import Category, Task
from markdown import markdown
from time import timezone
from datetime import timedelta

tsks = Blueprint(
    "tsks", __name__, template_folder="templates"
)


@tsks.route("/hidden-tasks/<int:category_id>")
def hidden_tasks(category_id):
    category = Category.query.get(category_id)
    if current_user.is_anonymous or current_user.id != category.contributor_id:
        return(redirect(url_for('cats.index')))

    tasks = Task.query.filter_by(
        catid=category_id,
        contributor_id=current_user.id,
        done=True
    ).order_by(Task.priority.desc()).all()

    for task in tasks:
        task.markup = markdown(task.content)
        task.href = url_for('taskaction.task_action', taskid=task.id)
        local_time = task.timestamp - timedelta(seconds=timezone)
        task.time = local_time.strftime("%Y-%m-%d %H:%M")

    nl = (
        ('new', url_for('newtask.new_task', category_id=category_id)),
        ('categories', url_for('cats.index')),
        ('open', url_for('tsks.tasks', category_id=category_id))
    )
    return render_template(
        'tasks.html',
        title="Completed Tasks",
        navbar_links=nl,
        tasks=tasks,
        heading="{}:completed tasks".format(category.name)
    )


@tsks.route("/tasks/<int:category_id>")
def tasks(category_id):
    category = Category.query.get(category_id)
    if current_user.is_anonymous or current_user.id != category.contributor_id:
        return(redirect(url_for('cats.index')))

    tasks = Task.query.filter_by(
        catid=category_id,
        contributor_id=current_user.id,
        done=False
    ).order_by(Task.priority.desc()).all()

    for task in tasks:
        task.markup = markdown(task.content)
        task.href = url_for('taskaction.task_action', taskid=task.id)
        local_time = task.timestamp - timedelta(seconds=timezone)
        task.time = local_time.strftime("%Y-%m-%d %H:%M")

    nl = (
        ('new', url_for('newtask.new_task', category_id=category_id)),
        ('categories', url_for('cats.index')),
        ('done', url_for('tsks.hidden_tasks', category_id=category_id))
    )
    return render_template(
        'tasks.html',
        title="Tasks",
        navbar_links=nl,
        tasks=tasks,
        heading="{}:tasks".format(category.name)
    )
