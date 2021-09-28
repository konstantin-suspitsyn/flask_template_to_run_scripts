from hq import app, mysql
from flask import render_template, request, session, flash, redirect, url_for
from hq.helpers import is_logged_in
from hq.data_change.data_change_forms import BaseDataChangeForm
import datetime as dt


@app.route('/db-change')
@is_logged_in
def db_change():
    """
    Список доступных форм для изменения
    На данный момент просто хардкод в html
    TODO переделать на автомат
    """
    return render_template(r'db_changes/data_change.html')


@app.route('/db-change/master_data_template')
@is_logged_in
def master_data_template():
    # Получим все записи таблицы
    cursor = mysql.connection.cursor()

    data = cursor.execute("""
    SELECT mde.id, some_data, property, u.username, creation_datetime, update_datetime
    FROM orchestrator.master_data_example mde
    left join users u on
        u.id = last_user_id """)

    all_data = cursor.fetchall()

    if data > 0:
        # Если что-то выгрузилось
        return render_template(r'db_changes/master_data_template.html', all_data=all_data)
    else:
        msg = 'Записей нет'
        return render_template(r'db_changes/master_data_template.html', msg=msg)

    cursor.close()


@app.route('/db-change/master_data_template/add_data', methods=['GET', 'POST'])
@is_logged_in
def add_data_to_md():
    form = BaseDataChangeForm(request.form)
    if request.method == 'POST' and form.validate():
        title_of_md = form.some_data.data
        property_of_md = form.some_property.data

        cursor = mysql.connection.cursor()
        # Получаем id текущего юзера
        cursor.execute("SELECT id FROM users WHERE username = %s", [session['username']])
        data = cursor.fetchone()
        user_id = data['id']
        cursor.execute("""
        INSERT INTO master_data_example(some_data, property, last_user_id, creation_datetime)
        VALUES (%s, %s, %s, %s)""", (title_of_md, property_of_md, user_id, dt.datetime.now()))
        mysql.connection.commit()
        cursor.close()

        flash('Запись создана', 'success')

        return redirect(url_for('master_data_template'))

    return render_template(r'db_changes/add_data.html', form=form)
