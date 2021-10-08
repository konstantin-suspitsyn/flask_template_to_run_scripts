from wtforms import Form, StringField, PasswordField, validators, SubmitField


class RegisterForm(Form):
    """
    Registration Form
    """
    username = StringField('Username пользователя', [validators.Length(min=3, max=50)])
    email = StringField('Email пользователя', [validators.Length(min=3, max=255)])
    password = PasswordField('Пароль', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Пароли не совпадают')
    ])
    confirm = PasswordField('Повторите пароль')
    first_name = StringField('Имя пользователя', [validators.Length(min=3, max=50)])
    last_name = StringField('Фамилия пользователя', [validators.Length(min=3, max=50)])


class PasswordChangeForm(Form):
    """
    Password Change Form
    """
    old_password = PasswordField('Старый пароль', [validators.DataRequired()])

    password = PasswordField('Пароль', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Пароли не совпадают')
    ])
    confirm = PasswordField('Повторите пароль')

    # PasswordChangeForm and UserDataChangeForm will be on the same page
    # Submit button will allow to catch what form was submitted
    submit = SubmitField('Изменить пароль')


class UserDataChangeForm(Form):
    """
    UserDataChange Form
    """
    email = StringField('Email пользователя', [validators.Length(min=3, max=255)])
    first_name = StringField('Имя пользователя', [validators.Length(min=3, max=50)])
    last_name = StringField('Фамилия пользователя', [validators.Length(min=3, max=50)])

    # PasswordChangeForm and UserDataChangeForm will be on the same page
    # Submit button will allow to catch what form was submitted
    submit = SubmitField('Изменить данные пользователя')

class RoleForm(Form):
    """
    Role form
    """
    role = StringField('Роль', [validators.Length(min=1, max=50)])


class PasswordResetForm(Form):
    """
    Reset Password form
    """
    password = PasswordField('Пароль', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Пароли не совпадают')
    ])
    confirm = PasswordField('Повторите пароль')