import requests
import logging
from flask import current_app

class TMDbAPI:
    def __init__(self):
        self.api_key = current_app.config['TMDB_API_KEY']
        self.base_url = current_app.config['TMDB_BASE_URL']
        self.image_base_url = current_app.config['TMDB_IMAGE_BASE_URL']
    
    def _make_request(self, endpoint, params=None):
        """Make a request to the TMDb API"""
        if params is None:
            params = {}
        
        params['api_key'] = self.api_key
        
        try:
            response = requests.get(f"{self.base_url}/{endpoint}", params=params)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logging.error(f"TMDb API request failed: {e}")
            return None
    
    def search_movies(self, query, page=1):
        """Search for movies by title"""
        endpoint = "search/movie"
        params = {
            'query': query,
            'page': page,
            'include_adult': 'false'
        }
        return self._make_request(endpoint, params)
    
    def get_movie_details(self, movie_id):
        """Get detailed information about a movie"""
        endpoint = f"movie/{movie_id}"
        params = {
            'append_to_response': 'credits,reviews,similar'
        }
        return self._make_request(endpoint, params)
    
    def get_movie_credits(self, movie_id):
        """Get cast and crew information for a movie"""
        endpoint = f"movie/{movie_id}/credits"
        return self._make_request(endpoint)
    
    def get_popular_movies(self, page=1):
        """Get popular movies"""
        endpoint = "movie/popular"
        params = {'page': page}
        return self._make_request(endpoint, params)
    
    def get_trending_movies(self, time_window='week', page=1):
        """Get trending movies"""
        endpoint = f"trending/movie/{time_window}"
        params = {'page': page}
        return self._make_request(endpoint, params)
    
    def get_movie_recommendations(self, movie_id, page=1):
        """Get movie recommendations based on a movie"""
        endpoint = f"movie/{movie_id}/recommendations"
        params = {'page': page}
        return self._make_request(endpoint, params)
    
    def get_genres(self):
        """Get list of movie genres"""
        endpoint = "genre/movie/list"
        return self._make_request(endpoint)
    
    def get_poster_url(self, poster_path, size='w500'):
        """Get full URL for movie poster"""
        if not poster_path:
            return None
        return f"{self.image_base_url}/{size}{poster_path}"
    
    def get_backdrop_url(self, backdrop_path, size='w1280'):
        """Get full URL for movie backdrop"""
        if not backdrop_path:
            return None
        return f"{self.image_base_url}/{size}{backdrop_path}"
    
    def get_top_rated_movies(self, page=1):
        """Get top-rated movies"""
        endpoint = "movie/top_rated"
        params = {'page': page}
        return self._make_request(endpoint, params)
    
    def get_upcoming_movies(self, page=1):
        """Get upcoming movies"""
        endpoint = "movie/upcoming"
        params = {'page': page}
        return self._make_request(endpoint, params)
    
    def get_now_playing_movies(self, page=1):
        """Get now playing movies"""
        endpoint = "movie/now_playing"
        params = {'page': page}
        return self._make_request(endpoint, params)
    
    def discover_movies_by_genre(self, genre_id, page=1):
        """Discover movies by genre"""
        endpoint = "discover/movie"
        params = {
            'with_genres': genre_id,
            'page': page,
            'sort_by': 'popularity.desc'
        }
        return self._make_request(endpoint, params)
    
    def get_movie_videos(self, movie_id):
        """Get movie trailers and videos"""
        endpoint = f"movie/{movie_id}/videos"
        return self._make_request(endpoint)
