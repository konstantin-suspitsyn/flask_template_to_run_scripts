from hq import app, db
from flask import render_template, flash, request, session, redirect, url_for
from hq.user_management.models_user_management import User, UserRoles, Role
from hq.user_management.forms_user_management import RegisterForm
from passlib.hash import sha256_crypt
from hq.helpers import is_not_logged_in, is_logged_in


@app.route('/login', methods=['POST', 'GET'])
@is_not_logged_in
def login():
    """
    Login form
    :return:
    """
    error_message = "Логин не существует или пароль некорректный"

    if request.method == 'POST':
        # Getting data from form
        username = request.form['username']
        password_candidate = request.form['password_candidate']

        system_user = User.query.filter_by(username=username).first()

        if system_user is not None:
            # User was found
            if sha256_crypt.verify(password_candidate, system_user.password):
                # Password matched
                role_user = UserRoles.query.filter_by(user_id=system_user.id).first()
                role_name = Role.query.filter_by(id=role_user.role_id).first()

                session['logged_in'] = True
                session['username'] = username
                session['role'] = role_name.name

                # If successful login, redirect to home page
                return redirect(url_for('index'))

            else:
                # Password is wrong
                flash(error_message, 'danger')

        else:
            # No user by this name
            flash(error_message, 'danger')

    return render_template('user_management/login.html')

@app.route('/register', methods=['POST', 'GET'])
@is_not_logged_in
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        # Base role of logged in user
        base_role = Role.query.filter_by(id=1).first()
        new_user = User(email=form.email.data,
                        username=form.username.data,
                        password=sha256_crypt.hash(form.password.data),
                        active=True,
                        first_name=form.first_name.data,
                        last_name=form.last_name.data,
                        )
        new_user.roles.append(base_role)
        db.session.add(new_user)
        db.session.commit()

        del new_user
        del base_role

        flash("""{}, привет! С регистрацией!""".format(form.username.data), 'success')

        return redirect(url_for('index'))

    return render_template('user_management/register.html', form=form)


@app.route('/logout', methods=['POST', 'GET'])
@is_logged_in
def logout():
    session.clear()
    flash('До новых встреч!', 'success')
    return redirect(url_for('index'))
