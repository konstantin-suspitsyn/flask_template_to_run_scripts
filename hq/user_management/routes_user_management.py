from hq import app, db
from flask import render_template, flash, request, session, redirect, url_for
from hq.user_management.models_user_management import User, UserRoles, Role
from hq.user_management.forms_user_management import RegisterForm, UserDataChangeForm, PasswordChangeForm, RoleForm,\
    PasswordResetForm
from passlib.hash import sha256_crypt
from hq.helpers import is_not_logged_in, is_logged_in, check_role


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


@app.route('/personal_settings', methods=['POST', 'GET'])
@is_logged_in
def personal_settings():
    data_change = UserDataChangeForm(request.form)

    user = User.query.filter_by(username=session['username']).first()

    if request.method == 'GET':
        # If we only view info
        data_change.email.data = user.email
        data_change.first_name.data = user.first_name
        data_change.last_name.data = user.last_name

    if (request.method == 'POST') and data_change.validate():
        # Changing User data NOT PASSWORD
        # Checking if data_change form was activated
        email_check = User.query.filter_by(email=data_change.email.data).first()
        if email_check is None or data_change.email.data == user.email:
            # No email duplicate was found or it's the same email we've got
            user.email = data_change.email.data
            user.first_name = data_change.first_name.data
            user.last_name = data_change.last_name.data
            db.session.commit()

            flash('Вы обновили данные пользователя', 'success')

        else:
            # Email duplicate was found
            flash('Пользователь с такой электронной почтой существует', 'danger')

    return render_template('user_management/personal_settings.html', data_change=data_change)


@app.route('/personal_settings/change_password', methods=['POST', 'GET'])
@is_logged_in
def change_password():
    password_change = PasswordChangeForm(request.form)

    user = User.query.filter_by(username=session['username']).first()

    if (request.method == 'POST') and password_change.validate():
        # Changing PASSWORD not user data
        # Checking if password_change form was activated
        if sha256_crypt.verify(password_change.old_password.data, user.password):
            # Checking if password matched
            user.password = sha256_crypt.hash(password_change.password.data)
            db.session.commit()

            flash('Пароль успешно изменен', 'success')

        else:
            flash('Текущий пароль неправильный', 'danger')

    return render_template('user_management/change_password.html', password_change=password_change)


@app.route('/dashboard')
@check_role(['administrator'])
def dashboard():
    return render_template('user_management/dashboard.html')


@app.route('/dashboard/roles', methods=['POST', 'GET'])
@check_role(['administrator'])
def roles():
    roles_list = Role.query.all()
    role_form = RoleForm(request.form)

    if request.method == 'POST' and role_form.validate():

        new_role_name = role_form.role.data

        check_existing_role = Role.query.filter_by(name=new_role_name).first()
        if check_existing_role is None:
            # Check if role is new
            new_role = Role(name=new_role_name)
            db.session.add(new_role)
            db.session.commit()

            flash('Роль создана', 'success')

            return redirect(url_for('roles'))

        else:
            flash('Такая роль уже есть', 'danger')

    return render_template('user_management/roles_list.html', role_form=role_form, roles_list=roles_list)


@app.route('/dashboard/roles/change/<string:id_no>', methods=['POST', 'GET'])
@check_role(['administrator'])
def role_edit(id_no):
    """
    Edit role
    :param id_no: Role id
    """
    role_form = RoleForm(request.form)
    current_role = Role.query.filter_by(id=id_no).first()

    if request.method == 'POST' and role_form.validate():

        if Role.query.filter_by(name=role_form.role.data).first() is None:
            current_role.name = role_form.role.data
            db.session.commit()

            flash('Название изменено', 'success')

            return redirect(url_for('roles'))

        else:
            # Duplicate name was found
            flash('Такая роль уже существует', 'danger')

    role_form.role.data = current_role.name

    return render_template('user_management/update_role.html', role_form=role_form)


@app.route('/dashboard/roles/delete/<string:id_no>', methods=['POST', 'GET'])
@check_role(['administrator'])
def role_delete(id_no):
    """
    Delete a role
    :param id_no: Role id
    """
    current_role = Role.query.filter_by(id=id_no).first()
    db.session.delete(current_role)
    db.session.commit()
    return redirect(url_for('roles'))


@app.route('/dashboard/users', methods=['GET', 'POST'])
@check_role(['administrator'])
def list_users():
    # List all users with pagination and search
    if request.method == 'POST':
        # Getting data from form
        # Crazy select with multiple tables
        user_name = request.form['username']
        # .first() returns tuple, so I need to convert it to list of tuples
        user_list = [db.session.query(User).select_from(User)\
                         .join(UserRoles, UserRoles.user_id == User.id)\
                         .join(Role, Role.id == UserRoles.role_id)\
                         .add_columns(User.id, User.username, User.email, User.first_name, User.last_name, User.active,
                                      Role.name)\
                         .filter(User.username == user_name)\
                         .filter(User.username != session['username']).first()]

        if user_list is None:
            flash('Пользователь с таким именем не найден', 'danger')

    if request.method == 'GET':
        # Crazy select with multiple tables
        # Do not allow change self user from this form
        user_list = db.session.query(User).select_from(User) \
            .join(UserRoles, UserRoles.user_id == User.id) \
            .join(Role, Role.id == UserRoles.role_id) \
            .add_columns(User.id, User.username, User.email, User.first_name, User.last_name, User.active, Role.name) \
            .filter(User.username != session['username']).all()

    return render_template('user_management/user_list.html', user_list=user_list)


@app.route('/dashboard/users/delete/<string:id_no>', methods=['GET', 'POST'])
@check_role(['administrator'])
def user_delete(id_no):
    """
    Delete an user
    :param id_no: Role id
    """
    current_role = User.query.filter_by(id=id_no).first()
    # Row from table user_roles will be deleted automatically
    db.session.delete(current_role)
    db.session.commit()
    return redirect(url_for('list_users'))


@app.route('/dashboard/users/password_reset/<string:id_no>', methods=['GET', 'POST'])
@check_role(['administrator'])
def password_reset(id_no):
    """

    :param id_no:
    """
    pass_form = PasswordResetForm(request.form)
    current_user = User.query.filter_by(id=id_no).first()

    if request.method == 'POST' and pass_form.validate():
        current_user.password = sha256_crypt.hash(pass_form.password.data)
        db.session.commit()

        flash('Пароль успешно изменен', 'success')

    return render_template('user_management/password_reset.html', pass_form=pass_form, user=current_user)