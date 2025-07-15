# Movie Database Web Application

## Overview

This is a Flask-based movie database web application that allows users to search for movies, view detailed information, and manage a personal watchlist. The application integrates with The Movie Database (TMDb) API to fetch movie data and provides user authentication for personalized features.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Backend Architecture
- **Framework**: Flask (Python web framework)
- **Database**: SQLAlchemy ORM with SQLite for development (configurable for PostgreSQL in production)
- **Authentication**: Flask-Login for session management
- **Form Handling**: Flask-WTF for form validation and CSRF protection
- **API Integration**: Custom TMDb API client for movie data

### Frontend Architecture
- **Template Engine**: Jinja2 (Flask's default)
- **CSS Framework**: Bootstrap 5 with dark theme
- **JavaScript**: Vanilla JavaScript for interactive features
- **Icons**: Font Awesome for UI icons

### Database Schema
- **User Model**: Stores user credentials, profile information, and timestamps
- **Watchlist Model**: Links users to movies with cached movie metadata
- **Review Model**: Stores user reviews and ratings for movies
- **MovieGenre Model**: Referenced but not fully implemented in current codebase

## Key Components

### Authentication System
- User registration and login functionality
- Password hashing using Werkzeug security utilities
- Session-based authentication with Flask-Login
- CSRF protection on all forms

### Movie Search and Discovery
- Integration with TMDb API for movie search
- Popular and trending movies display on homepage
- Detailed movie information pages with cast, reviews, and similar movies
- Movie recommendation system based on user watchlist

### Personal Features
- User watchlist management (add/remove movies)
- User profile page with statistics
- Movie reviews and ratings system
- Social sharing capabilities for movies

### API Integration
- TMDb API client (`tmdb_api.py`) handles all external API calls
- Caching of movie metadata in local database
- Error handling for API failures
- Image URL generation for movie posters

## Data Flow

1. **User Registration/Login**: Users create accounts or authenticate through forms
2. **Movie Search**: Search queries sent to TMDb API, results cached locally
3. **Watchlist Management**: Movies added to user's personal watchlist with metadata stored
4. **Recommendations**: Generated based on user's watchlist and similar movie preferences
5. **Reviews**: User ratings and reviews stored locally and associated with movies

## External Dependencies

### Third-Party Services
- **TMDb API**: Primary source for movie data, images, and metadata
- **Bootstrap CDN**: UI framework and styling
- **Font Awesome CDN**: Icon library

### Python Packages
- Flask ecosystem (Flask, Flask-SQLAlchemy, Flask-Login, Flask-WTF)
- Requests library for HTTP API calls
- Werkzeug for security utilities
- WTForms for form validation

### Environment Variables
- `SESSION_SECRET`: Flask session encryption key
- `DATABASE_URL`: Database connection string
- `TMDB_API_KEY`: API key for TMDb service

## Deployment Strategy

### Configuration
- Environment-based configuration using os.environ
- Database connection pooling for production
- Proxy fix middleware for deployment behind reverse proxies
- Debug mode configurable via environment

### Production Considerations
- SQLite for development, PostgreSQL recommended for production
- Static file serving via CDN or reverse proxy
- Session security with proper secret key management
- Database migration support through Flask-SQLAlchemy

## Recent Changes (July 2025)

### Enhanced Interactive Features
- **Browse Movies**: Added `/browse` route with tabbed interface for Popular, Trending, Top Rated, and Upcoming movies
- **Discover by Genre**: Added `/discover` route allowing users to explore movies by genre with visual genre cards
- **Navigation Updates**: Updated main navigation to prioritize Browse and Discover features
- **No Login Required**: All movie browsing and discovery features are accessible without authentication
- **Interactive Elements**: Added hover effects, smooth transitions, and keyboard shortcuts (S for search, B for browse, D for discover)

### API Enhancements
- **Extended TMDb Integration**: Added methods for top-rated, upcoming, now-playing movies, and genre-based discovery
- **Movie Videos**: Added support for fetching movie trailers and videos
- **Genre Discovery**: Implemented genre-based movie filtering with popularity sorting

### UI/UX Improvements
- **Quick Navigation**: Added large interactive buttons on homepage for easy access to main features
- **Enhanced Styling**: Improved animations, hover effects, and visual feedback
- **Responsive Design**: Better mobile experience with adjusted button sizes and navigation
- **Interactive Rating System**: Enhanced star rating with animations and feedback
- **Toast Notifications**: Improved notification system with icons and animations

### Technical Improvements
- **Database**: Successfully connected to PostgreSQL database
- **TMDb API**: Configured with authentic API key for real movie data
- **Enhanced JavaScript**: Added debounced search, tab switching, ripple effects, and keyboard navigation
- **Performance**: Optimized API calls and added loading states

### Architecture Updates
- **Route Organization**: Better separation of concerns with dedicated browse and discover routes
- **Template Structure**: Added reusable components and consistent styling
- **API Client**: Extended TMDbAPI class with comprehensive movie data methods
- **Static Assets**: Enhanced CSS and JavaScript for better interactivity

### Current Limitations
- Infinite scroll implementation needs backend pagination support
- Advanced search filters not yet implemented
- Movie trailer integration needs video player component
- Social features could be expanded with user interactions

The application now provides a fully interactive movie browsing experience accessible to all users, with authentication optional for personal features like watchlists and reviews.