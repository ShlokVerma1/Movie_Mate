from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    watchlist = db.relationship('Watchlist', backref='user', lazy=True, cascade='all, delete-orphan')
    reviews = db.relationship('Review', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.username}>'

class Watchlist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    movie_id = db.Column(db.Integer, nullable=False)  # TMDb movie ID
    movie_title = db.Column(db.String(200), nullable=False)
    movie_poster = db.Column(db.String(500))
    movie_overview = db.Column(db.Text)
    movie_release_date = db.Column(db.String(20))
    movie_rating = db.Column(db.Float)
    added_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Ensure unique movie per user
    __table_args__ = (db.UniqueConstraint('user_id', 'movie_id', name='unique_user_movie'),)
    
    def __repr__(self):
        return f'<Watchlist {self.movie_title}>'

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    movie_id = db.Column(db.Integer, nullable=False)  # TMDb movie ID
    movie_title = db.Column(db.String(200), nullable=False)
    rating = db.Column(db.Integer, nullable=False)  # 1-5 stars
    review_text = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Ensure unique review per user per movie
    __table_args__ = (db.UniqueConstraint('user_id', 'movie_id', name='unique_user_movie_review'),)
    
    def __repr__(self):
        return f'<Review {self.movie_title} by {self.user.username}>'

class MovieGenre(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    genre_id = db.Column(db.Integer, nullable=False)
    genre_name = db.Column(db.String(100), nullable=False)
    
    def __repr__(self):
        return f'<Genre {self.genre_name}>'
