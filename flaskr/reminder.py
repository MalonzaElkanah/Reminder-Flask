from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('notes', __name__)


# - index
@bp.route('/')
@login_required
def index():
	pass

# - create category

# - create reminder
# - update reminder
# - snooze reminder
# - delete reminder
# - repeat reminder (Daily, Weekly, Monthly, Yearly)

# - view all reminder
# - view calender and reminder
# - view category reminder
# - view specific reminder
# - reminder notification