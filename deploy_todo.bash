#!/bin/bash
# deploy_todo.bash

[ ! -d "/var/lib/todo" ] && mkdir /var/lib/todo
cp -v /home/trent/flaskapps/todo_app_flask/config.py        /var/lib/todo/
cp -v /home/trent/flaskapps/todo_app_flask/todo.py          /var/lib/todo/

[ ! -d "/var/lib/todo/app" ] && mkdir /var/lib/todo/app
cp -v /home/trent/flaskapps/todo_app_flask/app/__init__.py        /var/lib/todo/app
cp -v /home/trent/flaskapps/todo_app_flask/app/sendxmpp_handler.py        /var/lib/todo/app
cp -v /home/trent/flaskapps/todo_app_flask/app/models.py        /var/lib/todo/app
cp -v /home/trent/flaskapps/todo_app_flask/app/forms.py        /var/lib/todo/app
cp -v /home/trent/flaskapps/todo_app_flask/app/email.py        /var/lib/todo/app

[ ! -d "/var/lib/todo/app/categories" ] && mkdir /var/lib/todo/app/categories
cp -v /home/trent/flaskapps/todo_app_flask/app/categories/categories.py        /var/lib/todo/app/categories
cp -v /home/trent/flaskapps/todo_app_flask/app/categories/new_category.py        /var/lib/todo/app/categories
cp -v /home/trent/flaskapps/todo_app_flask/app/categories/hide_categories.py        /var/lib/todo/app/categories
cp -v /home/trent/flaskapps/todo_app_flask/app/categories/delete_category.py        /var/lib/todo/app/categories

[ ! -d "/var/lib/todo/app/categories/templates" ] && mkdir /var/lib/todo/app/categories/templates
cp -v /home/trent/flaskapps/todo_app_flask/app/categories/templates/categories.html        /var/lib/todo/app/categories/templates
cp -v /home/trent/flaskapps/todo_app_flask/app/categories/templates/new_category.html        /var/lib/todo/app/categories/templates

[ ! -d "/var/lib/todo/app/tasks" ] && mkdir /var/lib/todo/app/tasks
cp -v /home/trent/flaskapps/todo_app_flask/app/tasks/tasks.py        /var/lib/todo/app/tasks
cp -v /home/trent/flaskapps/todo_app_flask/app/tasks/new_task.py        /var/lib/todo/app/tasks
cp -v /home/trent/flaskapps/todo_app_flask/app/tasks/edit_task.py        /var/lib/todo/app/tasks
cp -v /home/trent/flaskapps/todo_app_flask/app/tasks/task_action.py        /var/lib/todo/app/tasks
cp -v /home/trent/flaskapps/todo_app_flask/app/tasks/delete_move_toggle_task.py        /var/lib/todo/app/tasks
cp -v /home/trent/flaskapps/todo_app_flask/app/tasks/reorder_priorities.py        /var/lib/todo/app/tasks

[ ! -d "/var/lib/todo/app/tasks/templates" ] && mkdir /var/lib/todo/app/tasks/templates
cp -v /home/trent/flaskapps/todo_app_flask/app/tasks/templates/tasks.html        /var/lib/todo/app/tasks/templates
cp -v /home/trent/flaskapps/todo_app_flask/app/tasks/templates/new_task.html        /var/lib/todo/app/tasks/templates
cp -v /home/trent/flaskapps/todo_app_flask/app/tasks/templates/task_action.html        /var/lib/todo/app/tasks/templates
cp -v /home/trent/flaskapps/todo_app_flask/app/tasks/templates/edit_task.html        /var/lib/todo/app/tasks/templates

[ ! -d "/var/lib/todo/app/auth" ] && mkdir /var/lib/todo/app/auth
cp -v /home/trent/flaskapps/todo_app_flask/app/auth/auth.py        /var/lib/todo/app/auth
cp -v /home/trent/flaskapps/todo_app_flask/app/auth/profile.py        /var/lib/todo/app/auth
cp -v /home/trent/flaskapps/todo_app_flask/app/auth/reset_password.py        /var/lib/todo/app/auth
cp -v /home/trent/flaskapps/todo_app_flask/app/auth/email.py        /var/lib/todo/app/auth
cp -v /home/trent/flaskapps/todo_app_flask/app/auth/register.py        /var/lib/todo/app/auth
cp -v /home/trent/flaskapps/todo_app_flask/app/auth/totp.py        /var/lib/todo/app/auth
cp -v /home/trent/flaskapps/todo_app_flask/app/auth/totp_utils.py        /var/lib/todo/app/auth

[ ! -d "/var/lib/todo/app/auth/templates" ] && mkdir /var/lib/todo/app/auth/templates
cp -v /home/trent/flaskapps/todo_app_flask/app/auth/templates/disable_2fa.html        /var/lib/todo/app/auth/templates
cp -v /home/trent/flaskapps/todo_app_flask/app/auth/templates/two_factor_input.html        /var/lib/todo/app/auth/templates
cp -v /home/trent/flaskapps/todo_app_flask/app/auth/templates/qr.html        /var/lib/todo/app/auth/templates
cp -v /home/trent/flaskapps/todo_app_flask/app/auth/templates/reset_password.html        /var/lib/todo/app/auth/templates
cp -v /home/trent/flaskapps/todo_app_flask/app/auth/templates/reset_password_request.html        /var/lib/todo/app/auth/templates
cp -v /home/trent/flaskapps/todo_app_flask/app/auth/templates/change_password.html        /var/lib/todo/app/auth/templates
cp -v /home/trent/flaskapps/todo_app_flask/app/auth/templates/edit_profile.html        /var/lib/todo/app/auth/templates
cp -v /home/trent/flaskapps/todo_app_flask/app/auth/templates/register.html        /var/lib/todo/app/auth/templates
cp -v /home/trent/flaskapps/todo_app_flask/app/auth/templates/login.html        /var/lib/todo/app/auth/templates

[ ! -d "/var/lib/todo/app/templates" ] && mkdir /var/lib/todo/app/templates
cp -v /home/trent/flaskapps/todo_app_flask/app/templates/base.html        /var/lib/todo/app/templates

[ ! -d "/var/lib/todo/app/templates/email" ] && mkdir /var/lib/todo/app/templates/email
cp -v /home/trent/flaskapps/todo_app_flask/app/templates/email/reset_password_email_html.html        /var/lib/todo/app/templates/email
cp -v /home/trent/flaskapps/todo_app_flask/app/templates/email/reset_password_email_text.txt        /var/lib/todo/app/templates/email

[ ! -d "/var/lib/todo/app/static" ] && mkdir /var/lib/todo/app/static
[ ! -d "/var/lib/todo/app/static/css" ] && mkdir /var/lib/todo/app/static/css
cp -v /home/trent/flaskapps/todo_app_flask/app/static/css/todo.css        /var/lib/todo/app/static/css

chown -R todo:todo /var/lib/todo
chown root:root /etc/systemd/system/todo.service

chmod 600 /var/lib/todo/.env
