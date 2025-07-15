import os
import logging
import random
from dotenv import load_dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from sqlalchemy.orm import DeclarativeBase
from werkzeug.middleware.proxy_fix import ProxyFix
from extensions import cache  # Import cache from extensions

# Load environment variables from .env file
load_dotenv()
# Configure logging
logging.basicConfig(level=logging.DEBUG)

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)
login_manager = LoginManager()
csrf = CSRFProtect()

def create_app():
    app = Flask(__name__)
    
     # Configure cache
    app.config['CACHE_TYPE'] = 'SimpleCache'  # Or 'RedisCache', 'FileSystemCache', etc.
    cache.init_app(app)
    
    # Configuration
    app.secret_key = os.getenv("SECRET_KEY")
    app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)
    
    # Database configuration
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
    app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
        "pool_recycle": 300,
        "pool_pre_ping": True,
    }
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    
    # TMDb API configuration
    app.config["TMDB_API_KEY"] = [os.getenv("TMDB_API_KEY"),os.getenv("TMDB_API_KEY_1"),
                                   os.getenv("TMDB_API_KEY_2"), os.getenv("TMDB_API_KEY_3"),
                                   os.getenv("TMDB_API_KEY_4"), os.getenv("TMDB_API_KEY_5"),
                                   os.getenv("TMDB_API_KEY_6"), os.getenv("TMDB_API_KEY_7")]
    app.config["TMDB_BASE_URL"] = "https://api.themoviedb.org/3"
    app.config["TMDB_IMAGE_BASE_URL"] = "https://image.tmdb.org/t/p"
    
    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)
    
    # Login manager configuration
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this page.'
    login_manager.login_message_category = 'info'
    
    @login_manager.user_loader
    def load_user(user_id):
        from models import User
        return User.query.get(int(user_id))
    
    # Create database tables
    with app.app_context():
        import models  # noqa: F401
        db.create_all()
        logging.info("Database tables created")
    
    # Register blueprints
    from routes import main_bp, auth_bp, movie_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(movie_bp, url_prefix='/movie')
    
    return app

app = create_app()
