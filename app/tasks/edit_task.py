#!/usr/bin/env python3

from flask import Blueprint, redirect, url_for, flash, render_template, request
from flask_login import current_user
from app.models import Task
from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField
from wtforms.validators import DataRequired
from .. import db

edittask = Blueprint(
    "edittask", __name__, template_folder="templates"
)


@edittask.route("/edit-task/<int:taskid>", methods=["GET", "POST"])
def edit_task(taskid):
    if current_user.is_anonymous:
        return(redirect(url_for('cats.index')))
    task = Task.query.get(taskid)
    form = EditTask()
    if task.done:
        cancel_nav_link = ('cancel', url_for('tsks.hidden_tasks', category_id=task.catid))
    else:
        cancel_nav_link = ('cancel', url_for('tsks.tasks', category_id=task.catid))
    nl = (cancel_nav_link, )
    if request.method == 'GET':
        form.content.data = task.content
    if form.validate_on_submit():
        task.content = form.content.data
        db.session.commit()
        flash("Thanks for the task edit!")
        if task.done:
            return(redirect(url_for('tsks.hidden_tasks', category_id=task.catid)))
        else:
            return(redirect(url_for('tsks.tasks', category_id=task.catid)))
    return render_template('edit_task.html', title='Edit Task', form=form, navbar_links=nl, task=task)


class EditTask(FlaskForm):
    content = TextAreaField(
        'Edit Task - Markdown Supported',
        validators=[DataRequired(), ],
        render_kw={'autofocus': True}
    )
    submit = SubmitField('Save')
