from wtforms import Form, StringField, validators


class BaseDataChangeForm(Form):
    """
    Базовая форма изменения Мастер данных в БД
    """
    some_data = StringField('Показатель', validators=[validators.Length(min=1, max=100)])
    some_property = StringField('Свойство показателя', validators=[validators.Length(min=1, max=100)])
