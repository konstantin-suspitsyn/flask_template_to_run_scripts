from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'ddb3bac6ad73503d1ef4920a'

# Config MySQL
MYSQL_HOST = 'localhost'
MYSQL_USER = 'root'
MYSQL_PASSWORD = 'root'
MYSQL_DB = 'orchestrator_01'

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://{}:{}@{}/{}'.format(MYSQL_USER, MYSQL_PASSWORD, MYSQL_HOST, MYSQL_DB)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Items per page for pagination
app.config['ALLOWED_EXTENSIONS'] = ('xlsx',)
app.config['UPLOAD_FOLDER'] = r'hq\static\tmp_files'

# init SQLAlchemy
db = SQLAlchemy(app)

from hq import routes
from hq.user_management import routes_user_management
from hq.run_functions import routes_run_function
