from hq import app
from flask import render_template, session, redirect, url_for
from hq.helpers import check_role

@app.route('/')
@app.route('/home')
def index():
    if 'logged_in' in session:
        return render_template('home.html')
    else:
        return redirect(url_for('login'))


@app.route('/about')
@check_role(['base'])
def about():
    return render_template('about.html')