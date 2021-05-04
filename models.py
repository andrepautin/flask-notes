from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    """creates a user instance"""

    __tablename__ = "users"

    username = db.Column(db.String(20), primary_key=True)

    password = db.Column(db.Text, nullable=False)

    email = db.Column(db.String(50), nullable=False, unique=True)

    first_name = db.Column(db.String(30), nullable=False)
    
    last_name = db.Column(db.String(30), nullable=False)


def connect_db(app):
    db.app = app
    db.init_app(app)