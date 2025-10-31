import streamlit as st
import pickle
import pandas as pd
import requests
from streamlit_option_menu import option_menu
import base64
import random
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="MovieFlix",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)


# Custom CSS for royal green styling
def local_css():
    st.markdown("""
    <style>
    /* Main background */
    .stApp {
        background-color: #141414;
        color: white;
    }

    /* Sidebar styling */
    .css-1d391kg, .css-12oz5g7 {
        background-color: #141414;
    }

    /* Text color */
    .css-10trblm, .css-16idsys p, .css-1cpxqw2 {
        color: white !important;
    }

    /* Button styling */
    .stButton button {
        background-color: #1e7b1e;
        color: white;
        border: none;
        border-radius: 4px;
        padding: 10px 20px;
        font-weight: bold;
        transition: all 0.3s ease;
    }

    .stButton button:hover {
        background-color: #2a9a2a;
        transform: scale(1.05);
    }

    /* Selectbox styling */
    .stSelectbox div[data-baseweb="select"] {
        background-color: #333;
        color: white;
        border-radius: 4px;
    }

    /* Header styling */
    .main-header {
        font-size: 3.5rem;
        font-weight: bold;
        background: linear-gradient(90deg, #1e7b1e, #4CAF50);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 2rem;
    }

    /* Movie card styling */
    .movie-card {
        background-color: #2f2f2f;
        border-radius: 8px;
        padding: 15px;
        margin: 10px;
        transition: transform 0.3s ease;
        height: 100%;
        display: flex;
        flex-direction: column;
    }

    .movie-card:hover {
        transform: translateY(-10px);
        box-shadow: 0 10px 20px rgba(30, 123, 30, 0.3);
    }

    .movie-title {
        font-weight: bold;
        font-size: 1.1rem;
        margin-top: 10px;
        color: white;
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
        flex-grow: 0;
    }

    .movie-year {
        color: #888;
        font-size: 0.9rem;
        margin-bottom: 10px;
    }

    .movie-overview {
        color: #d2d2d2;
        font-size: 0.9rem;
        overflow: hidden;
        display: -webkit-box;
        -webkit-line-clamp: 3;
        -webkit-box-orient: vertical;
        flex-grow: 1;
    }

    /* Recommendation section */
    .recommendation-section {
        margin: 30px 0;
    }

    .section-title {
        font-size: 1.8rem;
        font-weight: bold;
        margin-bottom: 20px;
        color: white;
        border-left: 5px solid #1e7b1e;
        padding-left: 15px;
    }

    /* Loading animation */
    .loading {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 200px;
    }

    /* Footer */
    .footer {
        text-align: center;
        margin-top: 50px;
        padding: 30px;
        color: #b0b0b0;
        border-top: 1px solid #333;
        background: linear-gradient(180deg, #141414 0%, #1a1a1a 100%);
    }

    .footer-title {
        font-size: 1.2rem;
        font-weight: bold;
        color: #1e7b1e;
        margin-bottom: 10px;
    }

    .footer-text {
        font-size: 0.9rem;
        line-height: 1.5;
    }

    /* Movie info in cards */
    .movie-info {
        flex-grow: 1;
        display: flex;
        flex-direction: column;
    }

    /* Developer credit */
    .developer-credit {
        text-align: center;
        margin-top: 20px;
        padding: 15px;
        background: linear-gradient(90deg, #1e7b1e, #4CAF50);
        border-radius: 8px;
        color: white;
        font-weight: bold;
    }

    /* Hide deprecated warning */
    .stDecoration {
        display: none;
    }

    /* Trailer button styling */
    .trailer-button {
        background: linear-gradient(45deg, #FF0000, #CC0000) !important;
        color: white !important;
        border: none !important;
        border-radius: 4px !important;
        padding: 8px 16px !important;
        font-weight: bold !important;
        margin-top: 10px !important;
        width: 100% !important;
    }

    .trailer-button:hover {
        background: linear-gradient(45deg, #CC0000, #990000) !important;
        transform: scale(1.02) !important;
    }

    /* YouTube embed styling */
    .youtube-container {
        position: relative;
        width: 100%;
        height: 0;
        padding-bottom: 56.25%;
        margin: 20px 0;
    }

    .youtube-iframe {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        border-radius: 8px;
    }

    /* Chat message styling */
    .user-message {
        background: linear-gradient(135deg, #1e7b1e, #2a9a2a);
        color: white;
        padding: 12px 16px;
        border-radius: 18px 18px 4px 18px;
        margin: 8px 0;
        max-width: 80%;
        margin-left: auto;
    }

    .bot-message {
        background: #2f2f2f;
        color: white;
        padding: 12px 16px;
        border-radius: 18px 18px 18px 4px;
        margin: 8px 0;
        max-width: 80%;
        margin-right: auto;
        border: 1px solid #444;
    }

    /* Comparison styling */
    .comparison-card {
        background: linear-gradient(135deg, #2f2f2f, #3a3a3a);
        border-radius: 12px;
        padding: 20px;
        margin: 15px 0;
        border: 1px solid #444;
    }

    /* Statistics styling */
    .stat-card {
        background: linear-gradient(135deg, #1e7b1e, #2a9a2a);
        border-radius: 12px;
        padding: 20px;
        margin: 10px;
        text-align: center;
        color: white;
    }

    .stat-number {
        font-size: 2.5rem;
        font-weight: bold;
        margin-bottom: 5px;
    }

    .stat-label {
        font-size: 0.9rem;
        opacity: 0.9;
    }
    </style>
    """, unsafe_allow_html=True)


# Initialize session state
def initialize_session_state():
    if 'user_profile' not in st.session_state:
        st.session_state.user_profile = {
            'liked_movies': [],
            'watched_movies': [],
            'watchlist': [],
            'ratings': {},
            'joined_date': datetime.now().strftime("%Y-%m-%d")
        }

    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []

    if 'compared_movies' not in st.session_state:
        st.session_state.compared_movies = []


# Load data and similarity matrix
@st.cache_data
def load_data():
    movies = pickle.load(open('movies.pkl', 'rb'))
    similarity = pickle.load(open('similarity.pkl', 'rb'))
    return movies, similarity


# Fetch movie poster and details from OMDB API
def fetch_movie_details(movie_title):
    try:
        OMDB_API_KEY = "7dc44734"

        # Search for the movie by title
        url = f"http://www.omdbapi.com/?t={movie_title}&apikey={OMDB_API_KEY}"
        response = requests.get(url)
        data = response.json()

        if data['Response'] == 'True':
            return {
                'poster': data.get('Poster', 'https://via.placeholder.com/500x750/2f2f2f/ffffff?text=No+Image'),
                'year': data.get('Year', 'N/A'),
                'plot': data.get('Plot', 'No description available.'),
                'genre': data.get('Genre', 'N/A'),
                'rating': data.get('imdbRating', 'N/A'),
                'imdb_id': data.get('imdbID', ''),
                'director': data.get('Director', 'N/A'),
                'actors': data.get('Actors', 'N/A'),
                'runtime': data.get('Runtime', 'N/A')
            }
        else:
            return {
                'poster': 'https://via.placeholder.com/500x750/2f2f2f/ffffff?text=No+Image',
                'year': 'N/A',
                'plot': 'No description available.',
                'genre': 'N/A',
                'rating': 'N/A',
                'imdb_id': '',
                'director': 'N/A',
                'actors': 'N/A',
                'runtime': 'N/A'
            }
    except Exception as e:
        return {
            'poster': 'https://via.placeholder.com/500x750/2f2f2f/ffffff?text=No+Image',
            'year': 'N/A',
            'plot': 'No description available.',
            'genre': 'N/A',
            'rating': 'N/A',
            'imdb_id': '',
            'director': 'N/A',
            'actors': 'N/A',
            'runtime': 'N/A'
        }


# Fetch YouTube trailer using YouTube Data API
def fetch_youtube_trailer(movie_title, year=""):
    try:
        YOUTUBE_API_KEY = "AIzaSyAfgiry5l1sjctL4qSaX4WoHrleYlvbYs0"

        # Search for trailer
        search_query = f"{movie_title} {year} official trailer"
        url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&q={search_query}&type=video&key={YOUTUBE_API_KEY}&maxResults=1"

        response = requests.get(url)
        data = response.json()

        if 'items' in data and len(data['items']) > 0:
            video_id = data['items'][0]['id']['videoId']
            return f"https://www.youtube.com/embed/{video_id}"
        else:
            return None
    except Exception as e:
        return None


# Recommendation function
def recommend(movie, movies, similarity):
    try:
        movie_index = movies[movies['title'] == movie].index[0]
        distances = similarity[movie_index]
        movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:11]

        recommended_movies = []
        recommended_details = []

        for i in movies_list:
            movie_title = movies.iloc[i[0]].title
            recommended_movies.append(movie_title)
            # Fetch movie details including poster
            movie_details = fetch_movie_details(movie_title)
            recommended_details.append(movie_details)

        return recommended_movies, recommended_details
    except Exception as e:
        st.error(f"Error generating recommendations: {e}")
        return [], []


# Function to display trailer in a modal
def show_trailer(movie_title, movie_details):
    trailer_url = fetch_youtube_trailer(movie_title, movie_details.get('year', ''))

    if trailer_url:
        st.markdown(f"""
        <div class="youtube-container">
            <iframe class="youtube-iframe" src="{trailer_url}" 
                    frameborder="0" allow="accelerometer; autoplay; clipboard-write; 
                    encrypted-media; gyroscope; picture-in-picture" allowfullscreen>
            </iframe>
        </div>
        """, unsafe_allow_html=True)
        st.success(f"🎬 Watching trailer for: **{movie_title}**")
    else:
        st.warning(f"🚫 Trailer not available for **{movie_title}**")


# User Statistics Functions
def display_user_statistics():
    st.markdown('<div class="section-title">📊 Your Movie Statistics</div>', unsafe_allow_html=True)

    profile = st.session_state.user_profile
    total_watched = len(profile['watched_movies'])
    total_watchlist = len(profile['watchlist'])
    total_liked = len(profile['liked_movies'])

    # Calculate average rating
    ratings = list(profile['ratings'].values())
    avg_rating = sum(ratings) / len(ratings) if ratings else 0

    # Display stats in cards
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-number">{total_watched}</div>
            <div class="stat-label">Movies Watched</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-number">{total_watchlist}</div>
            <div class="stat-label">In Watchlist</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-number">{total_liked}</div>
            <div class="stat-label">Liked Movies</div>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-number">{avg_rating:.1f} ⭐</div>
            <div class="stat-label">Avg Rating</div>
        </div>
        """, unsafe_allow_html=True)

    # Recent activity
    st.subheader("Recent Activity")
    if profile['watched_movies']:
        st.write("**Recently Watched:**")
        recent_movies = profile['watched_movies'][-5:]
        for movie in reversed(recent_movies):
            st.write(f"• {movie}")
    else:
        st.info("No movies watched yet. Start exploring!")


# Movie Comparison Functions
def compare_movies(movie1, movie2):
    st.markdown('<div class="section-title">🎭 Movie Comparison</div>', unsafe_allow_html=True)

    details1 = fetch_movie_details(movie1)
    details2 = fetch_movie_details(movie2)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(f"""
        <div class="comparison-card">
            <div style="text-align: center;">
                <img src="{details1['poster']}" style="width: 200px; border-radius: 8px; margin-bottom: 15px;">
                <h3>{movie1}</h3>
                <p><strong>⭐ {details1['rating']}</strong> | {details1['year']}</p>
            </div>
            <div style="margin-top: 15px;">
                <p><strong>Genre:</strong> {details1['genre']}</p>
                <p><strong>Director:</strong> {details1['director']}</p>
                <p><strong>Runtime:</strong> {details1['runtime']}</p>
                <p><strong>Cast:</strong> {details1['actors']}</p>
            </div>
            <div style="margin-top: 15px;">
                <p><strong>Plot:</strong> {details1['plot']}</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="comparison-card">
            <div style="text-align: center;">
                <img src="{details2['poster']}" style="width: 200px; border-radius: 8px; margin-bottom: 15px;">
                <h3>{movie2}</h3>
                <p><strong>⭐ {details2['rating']}</strong> | {details2['year']}</p>
            </div>
            <div style="margin-top: 15px;">
                <p><strong>Genre:</strong> {details2['genre']}</p>
                <p><strong>Director:</strong> {details2['director']}</p>
                <p><strong>Runtime:</strong> {details2['runtime']}</p>
                <p><strong>Cast:</strong> {details2['actors']}</p>
            </div>
            <div style="margin-top: 15px;">
                <p><strong>Plot:</strong> {details2['plot']}</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Comparison metrics
    st.subheader("📈 Quick Comparison")
    comp_col1, comp_col2, comp_col3 = st.columns(3)

    with comp_col1:
        rating1 = float(details1['rating']) if details1['rating'] != 'N/A' else 0
        rating2 = float(details2['rating']) if details2['rating'] != 'N/A' else 0
        if rating1 > rating2:
            st.success(f"🏆 **{movie1}** has higher rating")
        elif rating2 > rating1:
            st.success(f"🏆 **{movie2}** has higher rating")
        else:
            st.info("⭐ Both have similar ratings")

    with comp_col2:
        year1 = int(details1['year']) if details1['year'].isdigit() else 0
        year2 = int(details2['year']) if details2['year'].isdigit() else 0
        if year1 > year2:
            st.info(f"🆕 **{movie1}** is newer")
        elif year2 > year1:
            st.info(f"🆕 **{movie2}** is newer")
        else:
            st.info("📅 Released in same year")

    with comp_col3:
        # Simple genre comparison
        genres1 = set(details1['genre'].split(', '))
        genres2 = set(details2['genre'].split(', '))
        common_genres = genres1.intersection(genres2)
        if common_genres:
            st.info(f"🎭 Common genres: {', '.join(common_genres)}")


# AI Chatbot Functions
def movie_chatbot():
    st.markdown('<div class="section-title">🤖 Movie Assistant</div>', unsafe_allow_html=True)
    st.write("Ask me about movies, get recommendations, or discuss your favorites!")

    # Chat container
    chat_container = st.container()

    # Display chat history
    with chat_container:
        for message in st.session_state.chat_history:
            if message['role'] == 'user':
                st.markdown(f'<div class="user-message">{message["content"]}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="bot-message">{message["content"]}</div>', unsafe_allow_html=True)

    # Chat input
    col1, col2 = st.columns([4, 1])
    with col1:
        user_input = st.text_input("Type your message...", key="chat_input", placeholder="Ask about movies...")
    with col2:
        send_button = st.button("Send", use_container_width=True)

    if send_button and user_input:
        # Add user message to chat
        st.session_state.chat_history.append({'role': 'user', 'content': user_input})

        # Generate bot response
        bot_response = generate_chat_response(user_input)
        st.session_state.chat_history.append({'role': 'bot', 'content': bot_response})

        # Rerun to update chat
        st.rerun()


def generate_chat_response(user_input):
    """Generate AI response based on user input"""
    user_input_lower = user_input.lower()

    # Greeting responses
    if any(word in user_input_lower for word in ['hello', 'hi', 'hey', 'hola']):
        responses = [
            "Hello! I'm your movie assistant. How can I help you today?",
            "Hi there! Ready to explore some amazing movies?",
            "Hey! What movies are you interested in today?"
        ]
        return random.choice(responses)

    # Recommendation requests
    elif any(word in user_input_lower for word in ['recommend', 'suggest', 'what should i watch', 'movie suggestion']):
        if 'action' in user_input_lower:
            return "For action movies, I'd recommend: Mad Max: Fury Road, John Wick, The Dark Knight, or Mission: Impossible!"
        elif 'comedy' in user_input_lower:
            return "Great choice! For comedy, check out: Superbad, The Hangover, Step Brothers, or Bridesmaids!"
        elif 'romance' in user_input_lower:
            return "For romantic movies, try: The Notebook, La La Land, Crazy Rich Asians, or Pride and Prejudice!"
        elif 'horror' in user_input_lower:
            return "If you like horror: Get Out, The Conjuring, A Quiet Place, or Hereditary are excellent choices!"
        else:
            return "I'd love to recommend some movies! Could you tell me what genre you're in the mood for? Or maybe a movie you recently enjoyed?"

    # Movie information requests
    elif any(word in user_input_lower for word in ['about', 'tell me about', 'info', 'information']):
        movie_mentions = [word for word in user_input_lower.split() if len(word) > 3]
        if movie_mentions:
            return f"I can look up information about {movie_mentions[0].title()}. Try using the 'Browse Movies' section for detailed info!"
        else:
            return "Which movie would you like to know more about? I can help you find information about any movie!"

    # Rating questions
    elif any(word in user_input_lower for word in ['rating', 'score', 'imdb', 'rotten tomatoes']):
        return "I can check movie ratings from various sources. Which movie's rating are you curious about?"

    # General movie discussion
    elif any(word in user_input_lower for word in ['movie', 'film', 'cinema']):
        responses = [
            "Movies are amazing! What's your all-time favorite film?",
            "I love discussing movies! Have you seen any good ones recently?",
            "The world of cinema is so diverse! Are you into classics or prefer modern films?",
            "What genre excites you the most? Action, drama, comedy, or something else?"
        ]
        return random.choice(responses)

    # Fallback responses
    else:
        fallback_responses = [
            "I'm here to help with movies! You can ask me for recommendations, movie info, or just chat about films.",
            "That's interesting! As a movie assistant, I can help you find great films to watch.",
            "I'd love to talk about movies with you! What kind of films do you enjoy?",
            "Let's focus on movies! I can recommend films, compare movies, or discuss your favorites."
        ]
        return random.choice(fallback_responses)


# User interaction functions
def add_to_watchlist(movie_title):
    if movie_title not in st.session_state.user_profile['watchlist']:
        st.session_state.user_profile['watchlist'].append(movie_title)
        return True
    return False


def mark_as_watched(movie_title):
    if movie_title not in st.session_state.user_profile['watched_movies']:
        st.session_state.user_profile['watched_movies'].append(movie_title)
        return True
    return False


def rate_movie(movie_title, rating):
    st.session_state.user_profile['ratings'][movie_title] = rating


# Main app
def main():
    # Initialize session state
    initialize_session_state()

    # Apply custom CSS
    local_css()

    # Load data
    movies, similarity = load_data()
    movie_list = movies['title'].values

    # Sidebar navigation
    with st.sidebar:
        # Developer logo/name instead of Netflix
        st.markdown("""
        <div style='text-align: center; padding: 20px 0;'>
            <h2 style='color: #1e7b1e; font-size: 1.8rem; font-weight: bold;'>MovieFlix</h2>
            <p style='color: #888; font-size: 0.9rem;'>Developed by SAGAR</p>
        </div>
        """, unsafe_allow_html=True)

        selected = option_menu(
            menu_title="Navigation",
            options=["Home", "Recommendations", "Browse Movies", "Movie Comparison", "User Statistics", "AI Assistant"],
            icons=["house", "film", "search", "balance", "graph-up", "robot"],
            menu_icon="cast",
            default_index=0,
            styles={
                "container": {"padding": "5px", "background-color": "#141414"},
                "icon": {"color": "#1e7b1e", "font-size": "20px"},
                "nav-link": {"font-size": "16px", "text-align": "left", "margin": "0px", "--hover-color": "#2f2f2f"},
                "nav-link-selected": {"background-color": "#1e7b1e"},
            }
        )

    # Home page
    if selected == "Home":
        st.markdown('<h1 class="main-header">MovieFlix</h1>', unsafe_allow_html=True)

        col1, col2 = st.columns([2, 1])

        with col1:
            st.markdown("""
            <h2 style='color: white;'>Discover Your Next Favorite Movie</h2>
            <p style='font-size: 1.2rem; color: #d2d2d2;'>
            Welcome to MovieFlix, your personal movie recommendation engine. 
            Find movies similar to your favorites with our advanced AI-powered system.
            </p>
            <ul style='color: #d2d2d2; font-size: 1.1rem;'>
                <li>Personalized recommendations based on your movie preferences</li>
                <li>Thousands of movies in our database</li>
                <li>Watch trailers directly in the app</li>
                <li>Get recommendations in seconds</li>
                <li>Compare movies side-by-side</li>
                <li>Track your movie statistics</li>
                <li>Chat with AI movie assistant</li>
                <li>Detailed movie information with posters and ratings</li>
            </ul>
            """, unsafe_allow_html=True)

            if st.button("Get Started →", key="home_button"):
                st.session_state.page = "Recommendations"

        with col2:
            st.image("https://cdn.pixabay.com/photo/2019/04/24/21/55/cinema-4153289_1280.jpg", use_container_width=True)

    # Recommendations page
    elif selected == "Recommendations":
        st.markdown('<h1 class="main-header">Movie Recommendations</h1>', unsafe_allow_html=True)

        col1, col2 = st.columns([1, 1])

        with col1:
            selected_movie = st.selectbox(
                "Select a movie you like:",
                movie_list,
                index=0,
                help="Choose a movie to get similar recommendations"
            )

        with col2:
            st.write("")
            st.write("")
            if st.button("Find Similar Movies", key="recommend_button"):
                with st.spinner('Finding the best recommendations for you...'):
                    recommended_movies, recommended_details = recommend(selected_movie, movies, similarity)

                    if recommended_movies:
                        st.session_state.recommended_movies = recommended_movies
                        st.session_state.recommended_details = recommended_details
                        st.session_state.selected_movie = selected_movie
                    else:
                        st.error("Sorry, we couldn't find recommendations for this movie.")

        # Display recommendations if available
        if hasattr(st.session_state, 'recommended_movies') and st.session_state.recommended_movies:
            st.markdown(f'<div class="section-title">Movies Similar to "{st.session_state.selected_movie}"</div>',
                        unsafe_allow_html=True)

            # Display movies in a grid with trailer buttons
            cols = st.columns(5)
            for idx, (movie, details) in enumerate(
                    zip(st.session_state.recommended_movies, st.session_state.recommended_details)):
                with cols[idx % 5]:
                    with st.container():
                        st.markdown('<div class="movie-card">', unsafe_allow_html=True)
                        st.image(details['poster'], use_container_width=True)
                        st.markdown('<div class="movie-info">', unsafe_allow_html=True)
                        st.markdown(f'<div class="movie-title">{movie}</div>', unsafe_allow_html=True)
                        st.markdown(f'<div class="movie-year">{details["year"]} • ⭐ {details["rating"]}</div>',
                                    unsafe_allow_html=True)
                        st.markdown(f'<div class="movie-overview">{details["plot"]}</div>', unsafe_allow_html=True)
                        st.markdown('</div>', unsafe_allow_html=True)

                        # Action buttons
                        col_btn1, col_btn2, col_btn3 = st.columns(3)
                        with col_btn1:
                            if st.button("🎬", key=f"trailer_{idx}", help="Watch Trailer"):
                                st.session_state.current_trailer_movie = movie
                                st.session_state.current_trailer_details = details
                        with col_btn2:
                            if st.button("➕", key=f"watchlist_{idx}", help="Add to Watchlist"):
                                if add_to_watchlist(movie):
                                    st.success(f"Added {movie} to watchlist!")
                        with col_btn3:
                            if st.button("👁️", key=f"watched_{idx}", help="Mark as Watched"):
                                if mark_as_watched(movie):
                                    st.success(f"Marked {movie} as watched!")

                        st.markdown('</div>', unsafe_allow_html=True)

            # Display trailer if a movie is selected
            if hasattr(st.session_state, 'current_trailer_movie'):
                st.markdown("---")
                st.markdown(f'<div class="section-title">Trailer: {st.session_state.current_trailer_movie}</div>',
                            unsafe_allow_html=True)
                show_trailer(st.session_state.current_trailer_movie, st.session_state.current_trailer_details)

    # Browse Movies page
    elif selected == "Browse Movies":
        st.markdown('<h1 class="main-header">Browse Movies</h1>', unsafe_allow_html=True)

        # Search and filter options
        col1, col2, col3 = st.columns([2, 1, 1])

        with col1:
            search_query = st.text_input("Search movies:", placeholder="Type to search...")

        with col2:
            sort_option = st.selectbox("Sort by:", ["Title", "Popularity"])

        with col3:
            items_per_page = st.selectbox("Movies per page:", [10, 20, 50])

        # Filter movies based on search
        if search_query:
            filtered_movies = movies[movies['title'].str.contains(search_query, case=False)]
        else:
            filtered_movies = movies

        # Sort movies
        if sort_option == "Title":
            filtered_movies = filtered_movies.sort_values('title')

        # Pagination
        total_movies = len(filtered_movies)
        if total_movies > 0:
            total_pages = (total_movies - 1) // items_per_page + 1

            page = st.number_input("Page", min_value=1, max_value=total_pages, value=1)
            start_idx = (page - 1) * items_per_page
            end_idx = min(start_idx + items_per_page, total_movies)

            st.write(f"Showing {start_idx + 1}-{end_idx} of {total_movies} movies")

            # Display movies in grid
            movie_chunk = filtered_movies.iloc[start_idx:end_idx]
            rows = (len(movie_chunk) - 1) // 5 + 1

            for row in range(rows):
                cols = st.columns(5)
                for col_idx in range(5):
                    movie_idx = row * 5 + col_idx
                    if movie_idx < len(movie_chunk):
                        movie = movie_chunk.iloc[movie_idx]
                        with cols[col_idx]:
                            with st.container():
                                st.markdown('<div class="movie-card">', unsafe_allow_html=True)
                                # Fetch movie details for browse view
                                movie_details = fetch_movie_details(movie["title"])
                                st.image(movie_details['poster'], use_container_width=True)
                                st.markdown('<div class="movie-info">', unsafe_allow_html=True)
                                st.markdown(f'<div class="movie-title">{movie["title"]}</div>', unsafe_allow_html=True)
                                st.markdown(
                                    f'<div class="movie-year">{movie_details["year"]} • ⭐ {movie_details["rating"]}</div>',
                                    unsafe_allow_html=True)
                                st.markdown('</div>', unsafe_allow_html=True)

                                col1, col2, col3 = st.columns(3)
                                with col1:
                                    if st.button("🎬", key=f"browse_trailer_{movie_idx}", help="Trailer"):
                                        st.session_state.current_trailer_movie = movie["title"]
                                        st.session_state.current_trailer_details = movie_details
                                with col2:
                                    if st.button("➕", key=f"browse_watchlist_{movie_idx}", help="Watchlist"):
                                        if add_to_watchlist(movie["title"]):
                                            st.success(f"Added to watchlist!")
                                with col3:
                                    if st.button("👁️", key=f"browse_watched_{movie_idx}", help="Watched"):
                                        if mark_as_watched(movie["title"]):
                                            st.success(f"Marked as watched!")

                                st.markdown('</div>', unsafe_allow_html=True)

            # Display trailer if selected in browse view
            if hasattr(st.session_state, 'current_trailer_movie'):
                st.markdown("---")
                st.markdown(f'<div class="section-title">Trailer: {st.session_state.current_trailer_movie}</div>',
                            unsafe_allow_html=True)
                show_trailer(st.session_state.current_trailer_movie, st.session_state.current_trailer_details)
        else:
            st.info("No movies found matching your search criteria.")

    # Movie Comparison page
    elif selected == "Movie Comparison":
        st.markdown('<h1 class="main-header">Movie Comparison</h1>', unsafe_allow_html=True)

        col1, col2 = st.columns(2)

        with col1:
            movie1 = st.selectbox("Select first movie:", movie_list, key="compare_movie1")
        with col2:
            # Filter out the first movie from second selection
            movie2_options = [m for m in movie_list if m != movie1]
            movie2 = st.selectbox("Select second movie:", movie2_options, key="compare_movie2")

        if st.button("Compare Movies", use_container_width=True):
            if movie1 and movie2:
                compare_movies(movie1, movie2)
            else:
                st.warning("Please select two different movies to compare.")

    # User Statistics page
    elif selected == "User Statistics":
        st.markdown('<h1 class="main-header">User Statistics</h1>', unsafe_allow_html=True)
        display_user_statistics()

        # Watchlist section
        if st.session_state.user_profile['watchlist']:
            st.subheader("📋 Your Watchlist")
            for movie in st.session_state.user_profile['watchlist']:
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.write(f"• {movie}")
                with col2:
                    if st.button("Mark Watched", key=f"watch_{movie}"):
                        if mark_as_watched(movie):
                            st.session_state.user_profile['watchlist'].remove(movie)
                            st.rerun()

        # Recently Watched section
        if st.session_state.user_profile['watched_movies']:
            st.subheader("🎬 Recently Watched")
            recent_movies = st.session_state.user_profile['watched_movies'][-10:]
            for movie in reversed(recent_movies):
                rating = st.session_state.user_profile['ratings'].get(movie, "Not rated")
                st.write(f"• {movie} - ⭐ {rating}")

    # AI Assistant page
    elif selected == "AI Assistant":
        st.markdown('<h1 class="main-header">AI Movie Assistant</h1>', unsafe_allow_html=True)
        movie_chatbot()

    # Developer credit
    st.markdown("""
    <div class="developer-credit">
        <p>Developed by SAGAR | Advanced Movie Recommendation System</p>
    </div>
    """, unsafe_allow_html=True)

    # Professional Footer
    st.markdown("""
    <div class="footer">
        <div class="footer-title">MovieFlix</div>
        <div class="footer-text">
            <p>© 2025 MovieFlix. All Rights Reserved.</p>
            <p>Powered by OMDB API & YouTube Integration | Advanced Movie Recommendation Engine</p>
            <p style="margin-top: 10px; font-size: 0.8rem; color: #888;">
                Movie Comparisons • User Statistics • AI Assistant • Personalized Recommendations
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()