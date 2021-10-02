from flask import flash, url_for, redirect, session
from functools import wraps


def is_logged_in(f):
    """
    Checks if user is logged in
    """

    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Вы не авторизированы. Пожалуйста, войдите', 'danger')
            return redirect(url_for('login'))

    return wrap


def is_not_logged_in(f):
    """
    Checks if user is NOT logged in
    """

    @wraps(f)
    def wrap_no(*args, **kwargs):
        if 'logged_in' not in session:
            return f(*args, **kwargs)
        else:
            flash('Вы уже залогинены. Прекратите баловаться', 'danger')
            return redirect(url_for('index'))

    return wrap_no


def check_role(roles: list):
    """
    At least one role should be passed
    :param roles: list of roles that would be accepted to view data
    :return:
    """

    def wrapper(f):
        @wraps(f)
        def decorator(*args, **kwargs):
            if ('logged_in' in session) and (session['role'] in roles):
                return f(*args, **kwargs)
            else:
                flash('Вам закрыт доступ к этой информации. Обратитесь к администратору', 'danger')
                return redirect(url_for('index'))

        return decorator

    return wrapper
