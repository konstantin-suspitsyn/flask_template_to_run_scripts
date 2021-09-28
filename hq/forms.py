from wtforms import Form, StringField, PasswordField, validators


class RegisterForm(Form):
    """
    Форма регистрации
    """
    username = StringField('Имя пользователя', [validators.Length(min=6, max=50)])
    email = StringField('Email пользователя', [validators.Length(min=6, max=50)])
    password = PasswordField('Пароль', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Пароли не совпадают')
    ])
    confirm = PasswordField('Повторите пароль')