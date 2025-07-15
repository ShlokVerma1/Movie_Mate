from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import login_user, logout_user, login_required, current_user 
from sqlalchemy.exc import IntegrityError 
from app import db
from models import User, Watchlist, Review, MovieGenre
from forms import LoginForm, RegisterForm, SearchForm, ReviewForm
from tmdb_api import TMDbAPI
import logging
from extensions import cache  # Import cache from extension


# Create blueprints
main_bp = Blueprint('main', __name__)
auth_bp = Blueprint('auth', __name__)
movie_bp = Blueprint('movie', __name__)

# Main routes
@main_bp.route('/')
@cache.cached(timeout=60)  # Cache homepage for 1 hour
def index():
    """Home page with popular and trending movies"""
    tmdb = TMDbAPI(current_app.config['TMDB_API_KEY'])  # Get key from config
    
    try:
        # Get popular movies with error handling
        popular_movies = tmdb.get_popular_movies()
        trending_movies = tmdb.get_trending_movies()
        
        if not popular_movies or not trending_movies:
            flash('Error loading movie data', 'warning')
            popular_movies = trending_movies = []
            
    except Exception as e:
        logging.error(f"TMDb API error: {str(e)}")
        flash('Error connecting to movie database', 'danger')
        popular_movies = trending_movies = []
    
    search_form = SearchForm()
    
    return render_template('index.html', 
                        popular_movies=popular_movies,
                        trending_movies=trending_movies,
                        search_form=search_form,
                        tmdb=tmdb)

"""
# Old index route without caching or error handling
@main_bp.route('/')
def index():
    tmdb = TMDbAPI()
    popular_movies = tmdb.get_popular_movies()
    trending_movies = tmdb.get_trending_movies()
    search_form = SearchForm()
    return render_template('index.html', 
                         popular_movies=popular_movies,
                         trending_movies=trending_movies,
                         search_form=search_form,
                         tmdb=tmdb)
"""

@main_bp.route('/search', methods=['GET', 'POST'])
def search():
    """Search for movies"""
    form = SearchForm()
    results = None
    tmdb = TMDbAPI(current_app.config['TMDB_API_KEY'])
    
    if form.validate_on_submit():
        try:
            query = form.query.data
            page = request.args.get('page', 1, type=int)
            results = tmdb.search_movies(query, page)
            if not results:
                flash('No results found', 'info')
        except Exception as e:
            logging.error(f"Search error: {str(e)}")
            flash('Search service unavailable', 'danger')
    
    return render_template('search.html', form=form, results=results, tmdb=tmdb)

@main_bp.route('/watchlist')
@login_required
def watchlist():
    """User's personal watchlist"""
    # Pagination implementation
    page = request.args.get('page', 1, type=int)
    watchlist_pagination = Watchlist.query.filter_by(
        user_id=current_user.id
    ).order_by(
        Watchlist.added_at.desc()
    ).paginate(page=page, per_page=10)
    
    tmdb = TMDbAPI(current_app.config['TMDB_API_KEY'])
    return render_template('watchlist.html', 
                         watchlist=watchlist_pagination,
                         tmdb=tmdb)

"""
# Old watchlist route without pagination
@main_bp.route('/watchlist')
@login_required
def watchlist():
    user_watchlist = Watchlist.query.filter_by(user_id=current_user.id).order_by(Watchlist.added_at.desc()).all()
    tmdb = TMDbAPI()
    return render_template('watchlist.html', watchlist=user_watchlist, tmdb=tmdb)
"""

# Authentication routes
@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """User registration with enhanced security"""
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = RegisterForm()
    if form.validate_on_submit():
        try:
            # Password complexity checked in RegisterForm
            user = User(
                username=form.username.data,
                email=form.email.data
            )
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('auth.login'))
        except IntegrityError:
            db.session.rollback()
            flash('Username or email already exists', 'danger')
        except Exception as e:
            db.session.rollback()
            logging.error(f"Registration error: {str(e)}")
            flash('Registration failed', 'danger')
    
    return render_template('auth/register.html', form=form)

@movie_bp.route('/<int:movie_id>')
def detail(movie_id):
    """Movie detail page with optimized queries"""
    tmdb = TMDbAPI(current_app.config['TMDB_API_KEY'])
    
    try:
        movie = tmdb.get_movie_details(movie_id)
        if not movie:
            flash('Movie not found', 'danger')
            return redirect(url_for('main.index'))
    except Exception as e:
        logging.error(f"Movie detail error: {str(e)}")
        flash('Error loading movie details', 'danger')
        return redirect(url_for('main.index'))
    
    # Optimized queries
    in_watchlist = False
    user_review = None
    
    if current_user.is_authenticated:
        # Single query to check both watchlist and review
        watchlist_item, user_review = db.session.query(
            Watchlist, Review
        ).outerjoin(
            Review, 
            (Review.user_id == current_user.id) & 
            (Review.movie_id == movie_id)
        ).filter(
            Watchlist.user_id == current_user.id,
            Watchlist.movie_id == movie_id
        ).first() or (None, None)
        
        in_watchlist = watchlist_item is not None
    
    # Optimized reviews query with usernames
    reviews = db.session.query(
        Review, 
        User.username
    ).join(
        User
    ).filter(
        Review.movie_id == movie_id
    ).order_by(
        Review.created_at.desc()
    ).all()
    
    # Get recommendations with error handling
    recommendations = []
    try:
        recs = tmdb.get_movie_recommendations(movie_id)
        recommendations = recs.get('results', [])[:6]  # Limit to 6 recommendations
    except Exception as e:
        logging.error(f"Recommendations error: {str(e)}")
    
    form = ReviewForm()
    if user_review:
        form.rating.data = str(user_review.rating)
        form.review_text.data = user_review.review_text
    
    return render_template('movie_detail.html', 
                        movie=movie, 
                        tmdb=tmdb,
                        in_watchlist=in_watchlist,
                        reviews=reviews,
                        user_review=user_review,
                        recommendations=recommendations,
                        form=form)

"""
# Old detail route with separate queries
@movie_bp.route('/<int:movie_id>')
def detail(movie_id):
    tmdb = TMDbAPI()
    movie = tmdb.get_movie_details(movie_id)
    
    if not movie:
        flash('Movie not found', 'danger')
        return redirect(url_for('main.index'))
    
    in_watchlist = False
    user_review = None
    
    if current_user.is_authenticated:
        watchlist_item = Watchlist.query.filter_by(user_id=current_user.id, movie_id=movie_id).first()
        in_watchlist = watchlist_item is not None
        user_review = Review.query.filter_by(user_id=current_user.id, movie_id=movie_id).first()
    
    reviews = Review.query.filter_by(movie_id=movie_id).order_by(Review.created_at.desc()).all()
    recommendations = tmdb.get_movie_recommendations(movie_id)
    
    form = ReviewForm()
    if user_review:
        form.rating.data = str(user_review.rating)
        form.review_text.data = user_review.review_text
    
    return render_template('movie_detail.html', 
                         movie=movie, 
                         tmdb=tmdb,
                         in_watchlist=in_watchlist,
                         reviews=reviews,
                         user_review=user_review,
                         recommendations=recommendations,
                         form=form)
"""

@main_bp.route('/recommendations')
@login_required
@cache.memoize(timeout=86400)  # Cache recommendations for 24 hours
def recommendations():
    """Get optimized movie recommendations"""
    tmdb = TMDbAPI(current_app.config['TMDB_API_KEY'])
    
    # Get user's watchlist movie IDs
    watchlist_movie_ids = [w.movie_id for w in 
                          Watchlist.query.filter_by(
                              user_id=current_user.id
                          ).limit(5).all()]
    
    if not watchlist_movie_ids:
        flash('Add some movies to your watchlist to get recommendations', 'info')
        return redirect(url_for('main.watchlist'))
    
    # Get unique recommendations
    unique_recommendations = []
    seen_ids = set()
    
    for movie_id in watchlist_movie_ids:
        try:
            recs = tmdb.get_movie_recommendations(movie_id)
            if recs and recs.get('results'):
                for rec in recs['results']:
                    if rec['id'] not in seen_ids:
                        seen_ids.add(rec['id'])
                        unique_recommendations.append(rec)
                        if len(unique_recommendations) >= 20:
                            break
        except Exception as e:
            logging.error(f"Recommendation error for movie {movie_id}: {str(e)}")
            continue
    
    return render_template('recommendations.html', 
                         recommendations=unique_recommendations,
                         tmdb=tmdb)

"""
# Old recommendations route
@main_bp.route('/recommendations')
@login_required
def recommendations():
    tmdb = TMDbAPI()
    user_watchlist = Watchlist.query.filter_by(user_id=current_user.id).all()
    
    if not user_watchlist:
        flash('Add some movies to your watchlist to get recommendations', 'info')
        return redirect(url_for('main.watchlist'))
    
    recommendations = []
    for watchlist_item in user_watchlist[:5]:
        movie_recommendations = tmdb.get_movie_recommendations(watchlist_item.movie_id)
        if movie_recommendations and movie_recommendations.get('results'):
            recommendations.extend(movie_recommendations['results'])
    
    seen_ids = set()
    unique_recommendations = []
    for rec in recommendations:
        if rec['id'] not in seen_ids:
            seen_ids.add(rec['id'])
            unique_recommendations.append(rec)
            if len(unique_recommendations) >= 20:
                break
    
    return render_template('recommendations.html', 
                         recommendations=unique_recommendations,
                         tmdb=tmdb)
"""