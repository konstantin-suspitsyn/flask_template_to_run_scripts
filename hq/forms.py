from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt


class RegisterForm(Form):
    username = StringField('Имя пользователя', [validators.Length(min=6, max=50)])
    email = StringField('Email пользователя', [validators.Length(min=6, max=50)])
    password = PasswordField('Пароль', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Пароли не совпадают')
    ])
    confirm = PasswordField('Повторите пароль')
