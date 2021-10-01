# from hq import app, mysql
# from flask import render_template, request, flash, url_for, redirect, session
# from hq.forms import RegisterForm
# from passlib.hash import sha256_crypt
# from hq.helpers import is_not_logged_in, is_logged_in
#
#
# @app.route('/')
# @app.route('/home')
# def index():
#     return render_template('home.html')
#
#
# @app.route('/about')
# def about_page():
#     return render_template('about.html')
#
#
# @app.route('/register', methods=['POST', 'GET'])
# @is_not_logged_in
# def register():
#     sql_user_check = """
#     SELECT * FROM users
#     WHERE
#         username = %s
#         OR email = %s
#     """
#
#     form = RegisterForm(request.form)
#     if request.method == 'POST' and form.validate():
#
#         username = form.username.data
#         email = form.email.data
#         password = sha256_crypt.encrypt(str(form.password.data))
#
#         cursor = mysql.connection.cursor()
#
#         cursor.execute(sql_user_check, (username, email))
#         mysql.connection.commit()
#
#         if cursor.rowcount >= 1:
#             flash("Пользователь с таким именем или email уже существует", 'danger')
#         else:
#             cursor.execute("""
#             INSERT INTO users (username, email, password)
#             VALUES(%s, %s, %s);
#             """, (username, email, password))
#
#             mysql.connection.commit()
#             cursor.close()
#
#             flash("""{}, привет! С регистрацией!""".format(username), 'success')
#
#             return redirect(url_for('index'))
#
#     return render_template('register.html', form=form)
#
#
# @app.route('/login', methods=['POST', 'GET'])
# @is_not_logged_in
# def login_page():
#     error_message = "Логин не существует или пароль некорректный"
#
#     if request.method == 'POST':
#         # Получаем имя и пароль из формы
#         username = request.form['username']
#         password_candidate = request.form['password_candidate']
#
#         # Пытаемся получить наличие user по username
#         cursor = mysql.connection.cursor()
#         result = cursor.execute("SELECT * FROM users WHERE username = %s", [username])
#
#         if result > 0:
#             # Если user есть, сравниваем пароли
#             data = cursor.fetchone()
#             password = data['password']
#
#             cursor.close()
#
#             # Важен порядок внутри sha256_crypt.verify()
#             if sha256_crypt.verify(password_candidate, password):
#                 # Юзер существует, пароль корректный
#
#                 session['logged_in'] = True
#                 session['username'] = username
#
#                 flash("{}, добро пожаловать!".format(username), 'success')
#                 return redirect(url_for('index'))
#
#             else:
#                 return render_template('login.html', error_message=error_message)
#         else:
#             return render_template('login.html', error_message=error_message)
#
#     return render_template('login.html')
#
#
# @app.route('/logout')
# @is_logged_in
# def logout():
#     session.clear()
#     flash('До новых встреч!', 'success')
#     return redirect(url_for('index'))
#
#
# @app.route('/dashboard')
# @is_logged_in
# def dashboard():
#     return render_template('dashboard.html')
