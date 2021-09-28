from flask import flash, url_for, redirect, session
from functools import wraps


def is_logged_in(f):
    """
    Проверяет, если пользователь залогинился
    """

    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Вы не авторизированы. Пожалуйста, войдите', 'danger')
            return redirect(url_for('login_page'))

    return wrap


def is_not_logged_in(f):
    """
    Не позволяет залогиниться еще раз
    """

    @wraps(f)
    def wrap_no(*args, **kwargs):
        if 'logged_in' not in session:
            return f(*args, **kwargs)
        else:
            flash('Вы уже залогинены. Прекратите баловаться', 'danger')
            return redirect(url_for('index'))

    return wrap_no
