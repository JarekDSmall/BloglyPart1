"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    """User model."""
    
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    bio = db.Column(db.Text)
    
    def __repr__(self):
        return f'<User id={self.id} username={self.username}>'

def connect_db(app):
    """Connect the database to the Flask app."""
    db.app = app
    db.init_app(app)
