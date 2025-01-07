from flask_sqlalchemy import SQLAlchemy
db = None


def db_init(app):
    db = SQLAlchemy(app)
