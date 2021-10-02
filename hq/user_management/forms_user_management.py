from wtforms import Form, StringField, PasswordField, validators


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



