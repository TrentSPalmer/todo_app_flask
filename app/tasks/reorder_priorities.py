#!/usr/bin/env python3

import psycopg2
from flask import Blueprint, redirect, url_for, request, flash
from flask import current_app
from app.models import Task
from flask_login import current_user
from .task_action import make_move_up_down_bools
from .. import db

reorderp = Blueprint(
    "reorderp", __name__, template_folder="templates"
)


@reorderp.route('/move-task/<int:taskid>')
def move_task(taskid):
    task = Task.query.get(taskid)
    if task is None or current_user.is_anonymous or task.contributor_id != current_user.id:
        return(redirect(url_for('cats.index')))
    make_move_up_down_bools(task)
    priority = task.priority
    if request.args['move'] == 'up' and task.can_move_up:
        other_task = Task.query.filter(
            Task.catid == task.catid,
            Task.contributor_id == task.contributor_id,
            Task.done == task.done, Task.priority > task.priority).order_by(Task.priority).first()
        other_priority = other_task.priority
        other_task.priority = task.priority
        task.priority = other_priority
    if request.args['move'] == 'down' and task.can_move_down:
        other_task = Task.query.filter(
            Task.catid == task.catid,
            Task.contributor_id == task.contributor_id,
            Task.done == task.done, Task.priority < task.priority).order_by(Task.priority.desc()).first()
        other_priority = other_task.priority
        other_task.priority = task.priority
        task.priority = other_priority
    if request.args['move'] == 'top' and task.can_move_top:
        other_task = Task.query.filter(
            Task.catid == task.catid,
            Task.contributor_id == task.contributor_id,
            Task.done == task.done).order_by(Task.priority.desc()).first()
        task.priority = other_task.priority + 1
    if request.args['move'] == 'end' and task.can_move_end:
        task.priority = 0
    db.session.commit()
    if request.args['move'] == 'end' or request.args['move'] == 'top':
        reorder_priorities(task.catid, task.contributor_id, task.done, current_app.config)
    flash("task {} is moved {}".format(priority, request.args['move']))
    ru = 'tsks.{}tasks'.format('hidden_' if task.done else '')
    return(redirect(url_for(ru, category_id=task.catid)))


def reorder_priorities(catid, conid, done, app_config):
    conn = psycopg2.connect(
        dbname=app_config['DATABASE_NAME'],
        user=app_config['DATABASE_USER'],
        host=app_config['DATABASE_HOST'],
        password=app_config['DATABASE_PASSWORD']
    )
    cur = conn.cursor()
    cur.execute(
        "SELECT COUNT(id) FROM task WHERE catid=%s AND contributor_id=%s AND done=%s",
        (catid, conid, done))
    if cur.fetchone()[0] > 1:
        cur.execute(
            "SELECT id FROM task WHERE catid=%s AND contributor_id=%s AND done=%s ORDER BY priority",
            (catid, conid, done))
        ids = [x[0] for x in cur.fetchall()]
        for i, task in enumerate(ids, 1):
            cur.execute("UPDATE task SET priority=%s WHERE id=%s", (i, task))
            conn.commit()
    conn.close()
