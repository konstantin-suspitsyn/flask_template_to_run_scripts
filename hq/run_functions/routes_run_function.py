from hq import app, db
import pandas as pd
from hq.helpers import check_role, check_filetype
from flask import render_template, request, flash, redirect, url_for, send_file, after_this_request
from sqlalchemy import create_engine
from werkzeug.utils import secure_filename
import os
import datetime as dt


@app.route('/data', methods=['POST', 'GET'])
@check_role(['administrator'])
def data_menu():
    return render_template('data_management/data_menu.html')


@app.route('/data/add_data_from_excel', methods=['POST', 'GET'])
@check_role(['administrator'])
def add_data_from_excel():
    data = None

    sql_text = """
        SELECT title, `year`, bond_actor, director, actual_box_office, actual_budget
        FROM orchestrator_01.data_example_bond_movies
        order by `year` asc
        limit 10;
        """

    if request.method == 'POST':
        # check if the post request has the file part
        if not check_filetype(request.files['excel_to_upload'].filename):
            flash('Файл должет быть в нужном формате', 'danger')
            return redirect(url_for('add_data_from_excel'))

        file = request.files['excel_to_upload']

        # Path to save file
        filename = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file.filename))

        file.save(filename)
        df_to_upload = pd.read_excel(file)
        engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
        df_to_upload.to_sql('data_example_bond_movies', con=engine, if_exists='replace', index=False)

        os.remove(filename)

        flash('Данные загружены', 'success')

    try:
        data = db.engine.execute(sql_text)
    except Exception:
        flash('Пока данных нет', 'warning')

    return render_template('data_management/add_data_from_excel.html', data=data)


@app.route('/data/get_data_from_table', methods=['POST', 'GET'])
@check_role(['administrator'])
def get_data_from_table():
    """
    Retrive data from sql table
    You can show data of download excel file
    :return:
    """

    # Standard years for between in SQL
    year_start = 0
    year_end = 9999

    data = None

    sql_text = """
        select title, `year`, bond_actor, director, actual_box_office, actual_budget
        from orchestrator_01.data_example_bond_movies
        where `year` between {} and {}
        order by `year` asc;
        """
    if request.method == 'POST':
        try:
            if request.form['year_start'] != '':
                year_start = int(request.form['year_start'])
            if request.form['year_end'] != '':
                year_end = int(request.form['year_end'])
        except:
            flash('Годы должны бьть в числовом формате', 'danger')
            return redirect(url_for('get_data_from_table'))

        sql_text = sql_text.format(year_start, year_end)

        if request.form['submit_button'] == 'show':
            data = db.engine.execute(sql_text)

        if request.form['submit_button'] == 'download':
            engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
            df_to_download = pd.read_sql(sql_text, con=engine)

            filename = dt.datetime.now()

            # You need to add some random number to file to make sure that you would not rewrite somebody else's file
            filename = filename.strftime('%Y%m%d_%H%M') + '_bond_data.xlsx'

            save_path = os.path.abspath(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            df_to_download.to_excel(save_path, index=False)

            return send_file(save_path, attachment_filename='bond.xlsx')

    return render_template('data_management/get_data_from_table.html', data=data)


@app.route('/data/little_math', methods=['POST', 'GET'])
@check_role(['administrator'])
def little_math():

    if request.method == 'POST':
        # check if the post request has the file part
        if not check_filetype(request.files['excel_to_upload'].filename):
            flash('Файл должет быть в нужном формате', 'danger')
            return redirect(url_for('add_data_from_excel'))

        file = request.files['excel_to_upload']

        # Path to save file
        # You need to change name and add pseudo random something to name
        filename = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file.filename))

        file.save(filename)
        df_little_math = pd.read_excel(file)

        df_little_math['profit'] = df_little_math['actual_box_office'] - df_little_math['actual_budget']

        filename = dt.datetime.now()

        # You need to add some random number to file to make sure that you would not rewrite somebody else's file
        filename = filename.strftime('%Y%m%d_%H%M') + '_profit_data.xlsx'
        save_path = os.path.abspath(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        df_little_math.to_excel(save_path, index=False)

        return send_file(save_path, attachment_filename='bond_profit.xlsx')

    return render_template('data_management/little_math.html')
