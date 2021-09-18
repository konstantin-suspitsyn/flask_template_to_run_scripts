from flask import Flask
from flask_mysqldb import MySQL

app = Flask(__name__)
app.secret_key = 'ddb3bac6ad73503d1ef4920a'

# Config MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'orchestrator'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

# init MySQL
mysql = MySQL(app)

from hq import routes
