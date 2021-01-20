#!/usr/bin/env python3

from flask import Blueprint, redirect, url_for, render_template
from flask_login import current_user
from app.models import Task

taskaction = Blueprint(
    "taskaction", __name__, template_folder="templates"
)


@taskaction.route('/task-action/<int:taskid>')
def task_action(taskid):
    if current_user.is_anonymous:
        return(redirect(url_for('cats.index')))
    task = Task.query.get(taskid)
    if task.done:
        cancel_nav_link = ('cancel', url_for('tsks.hidden_tasks', category_id=task.catid))
    else:
        cancel_nav_link = ('cancel', url_for('tsks.tasks', category_id=task.catid))
    nl = (
        cancel_nav_link,
        ('categories', url_for('cats.index')),
        ('logout', url_for('auths.logout'))
    )
    make_move_up_down_bools(task)
    return(render_template(
        'task_action.html',
        title="Task Actions",
        navbar_links=nl,
        task=task
    ))


def make_move_up_down_bools(task):
    num_higher = Task.query.filter(
        Task.catid == task.catid,
        Task.contributor_id == task.contributor_id,
        Task.done == task.done,
        Task.priority > task.priority).count()
    num_lower = Task.query.filter(
        Task.catid == task.catid,
        Task.contributor_id == task.contributor_id,
        Task.done == task.done,
        Task.priority < task.priority).count()
    print(num_higher, num_lower)
    if num_higher > 1:
        task.can_move_top = True
        task.can_move_up = True
    elif num_higher == 1:
        task.can_move_top = False
        task.can_move_up = True
    else:
        task.can_move_top = False
        task.can_move_up = False
    if num_lower > 1:
        task.can_move_end = True
        task.can_move_down = True
    elif num_lower == 1:
        task.can_move_end = False
        task.can_move_down = True
    else:
        task.can_move_end = False
        task.can_move_down = False
