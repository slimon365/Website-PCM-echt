from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def db_init(app):
    db.init_app(app)

    with app.app_context():
        db.create_all()


db2 = SQLAlchemy()

def db2_init(app):
    db2.init_app(app)

    with app.app_context():
        db2.create_all()