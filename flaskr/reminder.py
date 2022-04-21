from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('reminder', __name__)

import datetime
import json

@bp.route('/')
@login_required
def index():
    db = get_db()
    # upcoming Reminders
    reminders = db.execute(
        'SELECT id, name, description, reminder_date'
        ' FROM reminder'
        ' WHERE user_id = ?'
        ' ORDER BY reminder_date DESC',
        (g.user['id'],)
    ).fetchall()
    return render_template('reminder/index.html', reminders=reminders)


@bp.route('/reminder/add', methods=['GET', 'POST'])
@login_required
def create_reminder():
    if request.method == 'POST':
        error = None
        # Get name, category_id, location, reminder_date, repeat, description
        name = request.form.get('name', None)
        repeat = request.form.get('repeat', 'ONCE')
        description = request.form.get('description', '[None]') 
        reminder_date = request.form.get('reminder_date', None)

        if name is None:
            error = 'Name is required.'

        if reminder_date is None:
            error = 'Reminder Date is required.'
        else:
            reminder_date = clean_datetime(reminder_date)
            if reminder_date is None:
                error = "Enter the Correct Date and Time format YYYY-MM-DD HH:MI"


        if error is not None:
            flash("ERROR: {}".format(error))
        else:
            db = get_db()
            db.execute(
                'INSERT INTO reminder (name, repeat, description, reminder_date, user_id)'
                ' VALUES (?, ?, ?, ?, ?)',
                (name, repeat, description, reminder_date, g.user['id'])
            )
            db.commit()
            return redirect(url_for('reminder.index'))

    return render_template('reminder/create_reminder.html', page="Create Reminder", reminder={})


@bp.route('/reminder/<int:id>/update', methods=['POST', 'GET'])
@login_required
def update_reminder(id):
    reminder = get_reminder(id)
    if request.method == 'POST':
        # Get name, category_id, location, reminder_date, repeat, description
        name = request.form.get('name', None)
        repeat = request.form.get('repeat', 'ONCE')
        description = request.form.get('description', '[None]') 
        reminder_date = request.form.get('reminder_date', None)

        error = None
        if name is None:
            error = 'Name is required.'

        if reminder_date is None:
            error = 'Reminder Date is required.'
        else:
            reminder_date = clean_datetime(reminder_date)
            if reminder_date is None:
                error = "Enter the Correct Date and Time format YYYY-MM-DD HH:MI"


        if error is not None:
            flash("ERROR: {}".format(error))
        else:
            db = get_db()
            db.execute(
                'UPDATE reminder'
                ' SET name = ?, repeat = ?, description = ?, reminder_date = ?'
                ' WHERE id = ?',
                (name, repeat, description, reminder_date, id)
            )
            db.commit()
            flash("{} Reminder updated".format(name))

            return redirect(url_for('reminder.reminder', id=id))

    return render_template('reminder/create_reminder.html', reminder=reminder, 
        page="Update Reminder: {}".format(reminder['name']))


@bp.route('/reminder/<int:id>/delete')
@login_required
def delete_reminder(id):
    get_reminder(id)
    db = get_db()
    db.execute('DELETE FROM reminder WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('reminder.index')) 


@bp.route('/reminder/<int:id>/repeat')
@login_required
def repeat_reminder(id):
    # - repeat reminder (Daily, Weekly, Monthly, Yearly)
    return render_template('reminder/index.html')  


@bp.route('/reminder/all')
@login_required
def all_reminder():
    db = get_db()
    # all Reminders
    reminders = db.execute(
        'SELECT id, name, description, event_date, reminder_date'
        ' FROM reminder'
        ' WHERE user_id = ?'
        ' ORDER BY event_date DESC',
        (g.user['id'],)
    ).fetchall()
    return render_template('reminder/index.html', reminders=reminders, page="All Reminders")


@bp.route('/reminder/calendar', methods = ['GET'])
@login_required
def calendar():
    db = get_db()
    # all Reminders
    reminders = db.execute(
        'SELECT *'
        ' FROM reminder'
        ' WHERE user_id = ?'
        ' ORDER BY reminder_date DESC',
        (g.user['id'],)
    ).fetchall()
    return render_template('reminder/calendar.html', reminders=reminders)


@bp.route('/<int:id>/category/reminder')
@login_required
def category_reminder(id):
    db = get_db()
    category = get_db().execute(
        'SELECT name, user_id FROM category WHERE id = ?',
        (id,)
    ).fetchone()

    # check if category exists and belong to user
    if category is None:
        abort(404, f"Category doesn't exist.")
    elif category['user_id'] != g.user['id']:
        abort(403)    
    else:
        # all Reminders
        reminders = db.execute(
            'SELECT id, name, description, event_date, reminder_date'
            ' FROM reminder'
            ' WHERE user_id = ? AND category_id = ?'
            ' ORDER BY event_date DESC',
            (g.user['id'], id)
        ).fetchall()

    status = "Category: {} Notes".format(category['name'])

    return render_template('reminder/index.html', reminders=reminders, page=status)


@bp.route('/reminder/<int:id>/view')
@login_required
def reminder(id):
    reminder = get_reminder(id)
    return render_template('reminder/reminder.html', reminder=reminder)


@bp.route('/reminder/<int:id>/notification')
@login_required
def notify_reminder(id):
    '''
    TODO
    send SMS
    send Email
    send 
    '''
    pass 


def get_reminder(id, check_user=True):
    reminder = get_db().execute(
        'SELECT *'
        ' FROM reminder'
        ' WHERE id = ?',
        (id,)
    ).fetchone()

    # Check if List Exist and belongs to request Owner
    if reminder is None:
        abort(404, f"Post id {id} doesn't exist.")
    elif check_user and reminder['user_id'] != g.user['id']:
        abort(403)

    print(type(reminder['reminder_date']))

    return reminder


@bp.route('/reminder/json')
@login_required
def get_event():
    db = get_db()
    # all Reminders
    reminders = db.execute(
        'SELECT *'
        ' FROM reminder'
        ' WHERE user_id = ?'
        ' ORDER BY reminder_date DESC',
        (g.user['id'],)
    ).fetchall()

    json_event = []

    for reminder in reminders:
        repeat = str(reminder['repeat']).strip() # ONCE, Daily, Weekly, Monthly, Yearly
        date = reminder['reminder_date']
        name = reminder['name']
        id = int(reminder['id'])

        duration = None

        if repeat == 'DAILY':
            duration = datetime.timedelta(days=1)
        elif repeat == 'WEEKLY':
            duration = datetime.timedelta(weeks=1)
        elif repeat == 'MONTHLY':
            duration = datetime.timedelta(months=1)
        elif repeat == 'YEARLY':
            duration = datetime.timedelta(days=365)

        json_event.append({
            'title': name, 'start': f"{date:%Y-%m-%dT%H:%M:%S}", 'url': url_for('reminder.reminder', id=id)
        })

        if duration is not None:
            # Next 55 Events
            for x in range(0, 56):
                date = date + duration
                json_event.append({
                    'title': name, 'start': f"{date:%Y-%m-%dT%H:%M:%S}", 
                    'url': url_for('reminder.reminder', id=id)
                })

    print(json_event)
    return json.dumps(json_event)





def clean_datetime(val):
    try:
        val = val.strip()
        datepart, timepart = val.split(" ")
        print(datepart)
        print(timepart)
        year, month, day = map(int, datepart.split("-"))
        # hours, minutes, seconds = map(int, timepart.split(":"))
        timelist = timepart.split(":")

        hours, minutes, seconds, microseconds = 0, 0, 0, 0 
        if len(timelist) == 3:
            hours, minutes, seconds = map(int, timepart.split(":"))
        elif len(timelist) == 2:
            hours, minutes = map(int, timepart.split(":"))
        elif len(timelist) == 1:
            hours = map(int, timepart.split(":"))

        val = datetime.datetime(year, month, day, hours, minutes, seconds, microseconds)
        return f"{val:%Y-%m-%d %H:%M:%S}"

    except Exception as e:
        return None
