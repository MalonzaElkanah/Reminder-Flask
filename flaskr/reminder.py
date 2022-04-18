from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('reminder', __name__)


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

        if not name:
            error = 'Name is required.'

        if not reminder_date:
            error = 'Reminder Date is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO reminder (name, repeat, description, reminder_date, user_id)'
                ' VALUES (?, ?, ?, ?, ?)',
                (name, repeat, description, reminder_date, g.user['id'])
            )
            db.commit()
            return redirect(url_for('reminder.index'))

    return render_template('reminder/create_reminder.html', page="Create Note", reminder={})


@bp.route('/reminder/<int:id>/update', methods=['POST', 'GET'])
@login_required
def update_reminder(id):
    reminder = get_reminder()
    if request.method == 'POST':
        # Get name, category_id, location, reminder_date, repeat, description
        name = request.form.get('name', None)
        repeat = request.form.get('repeat', 'ONCE')
        description = request.form.get('description', '[None]') 
        reminder_date = request.form.get('reminder_date', None)

        error = None
        if not name:
            error = 'Name is required.'

        if not reminder_date:
            error = 'Reminder Date is required.'


        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE journal'
                ' SET name = ?, repeat = ?, description = ?, reminder_date = ?'
                ' WHERE id = ?',
                (name, repeat, description, reminder_date, id)
            )
            db.commit()
            flash("{} Reminder updated".format(name))

            return redirect(url_for('reminder.reminder', id=id))

    return render_template('reminder/create_note.html', reminder=reminder, 
        page="Update Reminder: {}".format(reminder['name']))


@bp.route('/reminder/<int:id>/snooze')
@login_required
def snooze_reminder(id):
    return render_template('reminder/index.html')



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
        'SELECT id, name, description, event_date, reminder_date'
        ' FROM reminder'
        ' WHERE user_id = ?'
        ' ORDER BY event_date DESC',
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

    return reminder

