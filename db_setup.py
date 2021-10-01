# Creates tables if not exists
from hq import db
from hq.models import User

db.create_all()
db.session.commit()
