
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

import functools
from sqlite3 import IntegrityError
from werkzeug.security import check_password_hash, generate_password_hash

from website.db import get_db


bp = Blueprint('auth', __name__)


@bp.route("/create_account", methods=['POST', 'GET'])
def create_account():
    if request.method == 'POST':
 
        username = request.form['username']
        password = request.form['password']
        confirm = request.form['confirm']
        email = request.form['email']

        error = False

        if not username:
            error = True
            flash('A username is required')
        if not password:
            error = True
            flash('A password is required')
        if not email:
            error = True
            flash('An email is required')
        if not confirm:
            error = True
            flash('You must enter your password twice!')
        
        if password != confirm:
            flash('Your entered passwords do not match!')
            error = True

        if error is False:
            try:
                db = get_db()
                db.execute(
                    "INSERT INTO user (username, password, email, role) VALUES(?, ?, ?, ?)",
                    (username, generate_password_hash(password), email, "user")
                )
                db.commit()
            except db.IntegrityError:
                error = "Some part of the user is already registered!"
            else:
                return redirect(url_for("auth.login"))
   
    return render_template("auth/create_account.html", hide_error="hidden")


@bp.route("/login", methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        # check to see if you have a username and a password
        username = request.form['username']
        password = request.form['password']

        db = get_db()
        error = False
        user = db.execute(
        'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()

        if user is None:
            error = True
            flash('Incorrect username.')
        elif not check_password_hash(user['password'], password):
            error = True
            flash('Incorrect password.')

        if error is False:
            session.clear()
            session['user_id'] = user['username']
            return redirect(url_for('index'))

    return render_template("auth/login.html")


@bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for('index'))


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if (user_id) is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE username = ?', (user_id,)
        ).fetchone()


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for("auth.login"))

        return view(**kwargs)

    return wrapped_view