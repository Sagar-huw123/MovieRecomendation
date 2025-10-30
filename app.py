# app.py - MODIFIED VERSION (no secrets required)
import streamlit as st
import pickle
import pandas as pd
import requests
from PIL import Image
import io
import base64
from typing import List, Dict, Any
import os

# Configuration - SIMPLIFIED
OMDB_API_KEY = "2ee4fbe9"  # Direct assignment
MOVIES_PICKLE_PATH = "movies.pkl"
SIMILARITY_PICKLE_PATH = "similarity.pkl"

# Page configuration
st.set_page_config(
    page_title="Movie Recommender",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)


class MovieRecommender:
    def __init__(self):
        self.movies_df = None
        self.similarity_matrix = None
        self.load_data()

    def load_data(self):
        """Load movie data and similarity matrix from pickle files"""
        try:
            with open(MOVIES_PICKLE_PATH, 'rb') as f:
                self.movies_df = pickle.load(f)

            with open(SIMILARITY_PICKLE_PATH, 'rb') as f:
                self.similarity_matrix = pickle.load(f)

            st.success(f"✅ Loaded {len(self.movies_df)} movies and similarity matrix")

        except Exception as e:
            st.error(f"❌ Error loading data: {e}")
            # Create a dummy dataframe for testing if files don't exist
            self.movies_df = pd.DataFrame({
                'title': ['The Matrix', 'Inception', 'Avatar', 'The Dark Knight'],
                'movie_id': [1, 2, 3, 4],
                'overview': ['A computer hacker learns about the true nature of reality.',
                           'A thief who steals corporate secrets through dream-sharing technology.',
                           'A paraplegic marine dispatched to the moon Pandora.',
                           'Batman faces the Joker, a criminal mastermind.'],
                'release_date': ['1999-03-31', '2010-07-16', '2009-12-18', '2008-07-18'],
                'genres': [['Action', 'Sci-Fi'], ['Action', 'Thriller'], ['Action', 'Adventure'], ['Action', 'Crime']],
                'vote_average': [8.7, 8.8, 7.8, 9.0],
                'vote_count': [1800000, 2200000, 1200000, 2500000]
            })
            st.info("Using sample data for demonstration")

    def get_all_movies(self) -> List[Dict[str, Any]]:
        """Get all movies with basic information"""
        movies_list = []
        for _, row in self.movies_df.iterrows():
            movie = {
                'id': str(row.get('movie_id', row.get('id', ''))),
                'title': row.get('title', 'Unknown'),
                'year': self._extract_year(row),
                'genres': self._parse_genres(row),
                'overview': row.get('overview', 'No overview available.'),
                'vote_average': row.get('vote_average', 0),
                'vote_count': row.get('vote_count', 0)
            }
            movies_list.append(movie)
        return movies_list

    def get_recommendations(self, movie_title: str, k: int = 8) -> List[Dict[str, Any]]:
        """Get movie recommendations based on similarity"""
        try:
            # Find movie index
            movie_idx = self.movies_df[self.movies_df['title'] == movie_title].index
            if len(movie_idx) == 0:
                # Try partial match
                matching_movies = self.movies_df[
                    self.movies_df['title'].str.contains(movie_title, case=False, na=False)
                ]
                if len(matching_movies) == 0:
                    return []
                movie_idx = matching_movies.index[0:1]

            movie_idx = movie_idx[0]

            # Get similarity scores
            sim_scores = list(enumerate(self.similarity_matrix[movie_idx]))
            sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

            # Get top k similar movies (excluding itself)
            sim_scores = sim_scores[1:k + 1]

            recommendations = []
            for idx, score in sim_scores:
                movie_row = self.movies_df.iloc[idx]
                rec_movie = {
                    'id': str(movie_row.get('movie_id', movie_row.get('id', ''))),
                    'title': movie_row.get('title', 'Unknown'),
                    'year': self._extract_year(movie_row),
                    'genres': self._parse_genres(movie_row),
                    'score': float(score),
                    'overview': movie_row.get('overview', 'No overview available.'),
                    'vote_average': movie_row.get('vote_average', 0),
                    'vote_count': movie_row.get('vote_count', 0)
                }
                recommendations.append(rec_movie)

            return recommendations

        except Exception as e:
            st.error(f"Error getting recommendations: {e}")
            # Return dummy recommendations for testing
            return [
                {
                    'id': '1',
                    'title': 'The Matrix Reloaded',
                    'year': 2003,
                    'genres': ['Action', 'Sci-Fi'],
                    'score': 0.95,
                    'overview': 'Neo and the rebels continue their fight against the machines.',
                    'vote_average': 7.2,
                    'vote_count': 500000
                },
                {
                    'id': '2',
                    'title': 'Inception',
                    'year': 2010,
                    'genres': ['Action', 'Thriller'],
                    'score': 0.92,
                    'overview': 'A thief who steals corporate secrets through dream-sharing technology.',
                    'vote_average': 8.8,
                    'vote_count': 2200000
                }
            ]

    def search_movies(self, query: str, limit: int = 50) -> List[Dict[str, Any]]:
        """Search movies by title"""
        if not query:
            return self.get_all_movies()[:limit]

        query_lower = query.lower()
        matching_movies = []

        for movie in self.get_all_movies():
            if query_lower in movie['title'].lower():
                matching_movies.append(movie)

        return matching_movies[:limit]

    def _extract_year(self, row) -> int:
        """Extract year from release date or other fields"""
        try:
            # Try to get year from release_date
            release_date = row.get('release_date')
            if pd.notna(release_date) and release_date:
                if isinstance(release_date, str) and len(release_date) >= 4:
                    return int(release_date[:4])

            # Try from title (e.g., "Movie Title (2021)")
            title = row.get('title', '')
            if '(' in title and ')' in title:
                import re
                year_match = re.search(r'\((\d{4})\)', title)
                if year_match:
                    return int(year_match.group(1))

            return 2000  # Default year
        except:
            return 2000

    def _parse_genres(self, row) -> List[str]:
        """Parse genres from row data"""
        try:
            genres = row.get('genres', [])
            if isinstance(genres, str):
                # Handle string representation of list
                import ast
                try:
                    genres = ast.literal_eval(genres)
                except:
                    genres = [genres]

            if isinstance(genres, list):
                # Extract genre names from dict format
                genre_names = []
                for genre in genres:
                    if isinstance(genre, dict) and 'name' in genre:
                        genre_names.append(genre['name'])
                    elif isinstance(genre, str):
                        genre_names.append(genre)
                return genre_names[:3]  # Limit to 3 genres

            return ['Action', 'Drama']  # Default genres
        except:
            return ['Action', 'Drama']


class OMDBApi:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "http://www.omdbapi.com/"

    def get_movie_poster(self, title: str, year: int = None):
        """Get movie poster URL from OMDB API"""
        try:
            params = {
                'apikey': self.api_key,
                't': title,
                'type': 'movie'
            }
            if year:
                params['y'] = year

            response = requests.get(self.base_url, params=params, timeout=10)
            data = response.json()

            if data.get('Response') == 'True' and data.get('Poster') != 'N/A':
                return data['Poster']
            else:
                return None

        except Exception as e:
            st.warning(f"Could not fetch poster for {title}: {e}")
            return None


def load_css():
    """Load custom CSS for styling"""
    st.markdown("""
    <style>
    .movie-card {
        border: 1px solid #ddd;
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
        background: white;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        transition: transform 0.2s;
    }
    .movie-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.15);
    }
    .recommendation-card {
        border-left: 4px solid #ff4b4b;
    }
    .similarity-score {
        background: #ff4b4b;
        color: white;
        padding: 2px 8px;
        border-radius: 12px;
        font-size: 0.8em;
        font-weight: bold;
    }
    .genre-tag {
        background: #e0e0e0;
        padding: 2px 8px;
        border-radius: 10px;
        font-size: 0.8em;
        margin-right: 5px;
    }
    </style>
    """, unsafe_allow_html=True)


def display_movie_card(movie: Dict[str, Any], omdb_api: OMDBApi, show_score: bool = False):
    """Display a movie card with poster and details"""
    col1, col2 = st.columns([1, 3])

    with col1:
        # Try to get poster from OMDB
        poster_url = omdb_api.get_movie_poster(movie['title'], movie['year'])
        if poster_url and poster_url != 'N/A':
            st.image(poster_url, width=120)
        else:
            st.image("https://via.placeholder.com/120x180/cccccc/666666?text=No+Poster", width=120)

    with col2:
        st.subheader(movie['title'])

        # Year and rating
        col2a, col2b, col2c = st.columns([1, 1, 1])
        with col2a:
            st.write(f"**Year:** {movie['year']}")
        with col2b:
            st.write(f"**Rating:** ⭐ {movie['vote_average']}/10")
        with col2c:
            if show_score:
                st.markdown(f'<span class="similarity-score">{movie["score"] * 100:.1f}%</span>',
                            unsafe_allow_html=True)

        # Genres
        if movie['genres']:
            genre_tags = " ".join([f'<span class="genre-tag">{genre}</span>' for genre in movie['genres']])
            st.markdown(f"**Genres:** {genre_tags}", unsafe_allow_html=True)

        # Overview
        with st.expander("Overview"):
            st.write(movie['overview'][:300] + "..." if len(movie['overview']) > 300 else movie['overview'])

        # Action buttons
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            if st.button("🎬 Get Recommendations", key=f"rec_{movie['id']}_{movie['title']}"):
                st.session_state.selected_movie = movie['title']
                st.session_state.show_recommendations = True
                st.rerun()
        with col_btn2:
            if st.button("❤️ Add to Favorites", key=f"fav_{movie['id']}_{movie['title']}"):
                if 'favorites' not in st.session_state:
                    st.session_state.favorites = []
                if movie['title'] not in st.session_state.favorites:
                    st.session_state.favorites.append(movie['title'])
                    st.success(f"Added {movie['title']} to favorites!")

    st.markdown("---")


def main():
    # Initialize session state
    if 'selected_movie' not in st.session_state:
        st.session_state.selected_movie = None
    if 'show_recommendations' not in st.session_state:
        st.session_state.show_recommendations = False
    if 'favorites' not in st.session_state:
        st.session_state.favorites = []

    # Load CSS
    load_css()

    # Header
    st.title("🎬 Movie Recommender System")
    st.markdown("Discover your next favorite movie based on your preferences!")

    # Initialize recommender and OMDB API
    try:
        recommender = MovieRecommender()
        omdb_api = OMDBApi(OMDB_API_KEY)
    except Exception as e:
        st.error(f"Failed to initialize the recommender system: {e}")
        return

    # Sidebar
    with st.sidebar:
        st.header("🔍 Search & Filter")

        # Search
        search_query = st.text_input("Search movies", placeholder="Enter movie title...")

        # Genre filter (if available)
        all_movies = recommender.get_all_movies()
        all_genres = set()
        for movie in all_movies:
            all_genres.update(movie['genres'])
        selected_genres = st.multiselect("Filter by genres", sorted(all_genres))

        # Number of recommendations
        k_recommendations = st.slider("Number of recommendations", 4, 20, 8)

        # Favorites section
        if st.session_state.favorites:
            st.header("❤️ Your Favorites")
            for fav in st.session_state.favorites:
                if st.button(f"🎬 {fav}", key=f"fav_btn_{fav}"):
                    st.session_state.selected_movie = fav
                    st.session_state.show_recommendations = True
                    st.rerun()

        st.markdown("---")
        st.info("💡 **Tip:** Click 'Get Recommendations' on any movie to find similar films!")

    # Main content area
    if st.session_state.show_recommendations and st.session_state.selected_movie:
        # Show recommendations
        st.header(f"🎯 Recommendations similar to: **{st.session_state.selected_movie}**")

        if st.button("← Back to all movies"):
            st.session_state.show_recommendations = False
            st.session_state.selected_movie = None
            st.rerun()

        recommendations = recommender.get_recommendations(
            st.session_state.selected_movie,
            k=k_recommendations
        )

        if recommendations:
            st.success(f"Found {len(recommendations)} recommendations!")
            for movie in recommendations:
                display_movie_card(movie, omdb_api, show_score=True)
        else:
            st.warning("No recommendations found. Try a different movie.")

    else:
        # Show all/search results
        if search_query:
            st.header(f"🔍 Search Results for: '{search_query}'")
            movies = recommender.search_movies(search_query, limit=50)
        else:
            st.header("🎬 All Movies")
            movies = all_movies[:100]  # Limit to first 100 for performance

        # Apply genre filter
        if selected_genres:
            movies = [m for m in movies if any(genre in m['genres'] for genre in selected_genres)]

        if not movies:
            st.warning("No movies found matching your criteria.")
        else:
            st.info(f"Showing {len(movies)} movies")

            # Display movies in a grid
            for i, movie in enumerate(movies):
                display_movie_card(movie, omdb_api)

    # Footer
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center; color: #666;'>
            <p>Built with ❤️ using Streamlit | Movie data from TMDB | Posters from OMDB</p>
        </div>
        """,
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()