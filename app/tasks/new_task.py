#!/usr/bin/env python3

import psycopg2
from datetime import datetime
from flask import Blueprint, redirect, url_for, flash, render_template
from flask import current_app as app
from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField
from wtforms.validators import DataRequired
from app.models import Task, Category

newtask = Blueprint(
    "newtask", __name__, template_folder="templates"
)


def insert_task(task):
    conn = psycopg2.connect(
        dbname=app.config['DATABASE_NAME'],
        user=app.config['DATABASE_USER'],
        host=app.config['DATABASE_HOST'],
        password=app.config['DATABASE_PASSWORD']
    )
    cur = conn.cursor()
    cur.execute("SELECT setval('task_id_seq', (SELECT MAX(id) FROM task))")
    conn.commit()
    cur.execute(
        "SELECT MAX(priority) FROM task WHERE catid=%s AND contributor_id=%s AND done=%s",
        (task.catid, task.contributor_id, False)
    )
    max_priority = cur.fetchone()[0]
    task.priority = 1 if max_priority is None else max_priority + 1
    cur.execute(
        "SELECT count(id) FROM task WHERE content=%s AND contributor_id=%s",
        (task.content, task.contributor_id)
    )
    if cur.fetchone()[0] == 0:
        cur.execute(
            "INSERT INTO task(content, contributor_id, catid, priority, timestamp) VALUES(%s,%s,%s,%s,%s)",
            (task.content, task.contributor_id, task.catid, task.priority, task.timestamp)
        )
        conn.commit()
    conn.close


@newtask.route("/new-task/<int:category_id>", methods=["GET", "POST"])
def new_task(category_id):
    if current_user.is_anonymous:
        return(redirect(url_for('cats.index')))
    form = NewTask()
    category = Category.query.get(category_id)
    nl = (('cancel', url_for('tsks.tasks', category_id=category_id)), )
    if form.validate_on_submit():
        task = Task(
            content=form.content.data,
            contributor_id=current_user.id,
            catid=category_id,
            timestamp=str(datetime.utcnow()),
        )
        insert_task(task)
        flash("Thanks for the new task!")
        return(redirect(url_for('tsks.tasks', category_id=category_id)))
    return render_template('new_task.html', title='New Task', form=form, navbar_links=nl, category=category)


class NewTask(FlaskForm):
    content = TextAreaField(
        'New Task - Markdown Supported',
        validators=[DataRequired(), ],
        render_kw={'autofocus': True}
    )
    submit = SubmitField('Save')
