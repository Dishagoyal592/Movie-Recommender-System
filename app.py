import streamlit as st
import pickle
import pandas as pd
import requests
import time
import urllib3
from difflib import SequenceMatcher

# =====================================================
# PAGE CONFIGURATION
# =====================================================

st.set_page_config(
    page_title="CineMatch",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =====================================================
# SSL WARNING
# =====================================================

urllib3.disable_warnings(
    urllib3.exceptions.InsecureRequestWarning
)

# =====================================================
# CUSTOM CSS
# =====================================================

st.markdown(
    """
    <style>

    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    header {
        visibility: hidden;
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1400px;
    }

    [data-testid="stSidebar"] {
        background-color: #111827;
    }

    [data-testid="stSidebar"] * {
        color: #e5e7eb;
    }

    .hero {
        padding: 35px;
        border-radius: 20px;
        background: linear-gradient(
            135deg,
            #171d32,
            #0f172a
        );
        border: 1px solid #26324b;
        margin-bottom: 30px;
    }

    .hero h1 {
        color: white;
        font-size: 42px;
        margin-bottom: 8px;
    }

    .hero p {
        color: #aeb8cc;
        font-size: 17px;
    }

    .movie-card {
        background: #111827;
        border: 1px solid #26324b;
        border-radius: 15px;
        padding: 14px;
        height: 100%;
    }

    .movie-title {
        color: white;
        font-size: 18px;
        font-weight: 700;
        margin-top: 12px;
        min-height: 48px;
    }

    .movie-info {
        color: #cbd5e1;
        font-size: 14px;
        line-height: 1.8;
    }

    .similarity {
        color: #c084fc;
        font-weight: 700;
        font-size: 14px;
    }

    .section-title {
        font-size: 26px;
        font-weight: 700;
        color: white;
        margin-top: 30px;
    }

    </style>
    """,
    unsafe_allow_html=True
)

# =====================================================
# TMDB API KEY
# =====================================================

API_KEY = "a2b9b34ddbf3049e282dba0cb9500ca0"

# =====================================================
# SIDEBAR
# =====================================================

with st.sidebar:

    st.markdown(
        """
        <h2>🎬 CineMatch</h2>
        <p style="color:#94a3b8;">
        AI Movie Recommendation System
        </p>
        """,
        unsafe_allow_html=True
    )

    st.divider()

    st.markdown("### 📌 Project Overview")
    st.caption("Content-Based Recommendation")

    st.divider()

    st.markdown("### 📁 Dataset")
    st.caption("TMDB Movie Dataset")

    st.divider()

    st.markdown("### 🧠 Features Used")
    st.caption("• Genres")
    st.caption("• Keywords")
    st.caption("• Cast")
    st.caption("• Director")
    st.caption("• Movie Overview")

    st.divider()

    st.markdown("### 🎯 Similarity Measure")
    st.caption("Cosine Similarity")

    st.divider()

    st.markdown("### ⚙️ Technology Stack")
    st.caption("Python")
    st.caption("Pandas")
    st.caption("Scikit-Learn")
    st.caption("Streamlit")
    st.caption("TMDB API")

# =====================================================
# LOAD DATA
# =====================================================

@st.cache_resource
def load_data():

    with open("movies.pkl", "rb") as file:
        movies = pickle.load(file)

    with open("similarity.pkl", "rb") as file:
        similarity = pickle.load(file)

    return movies, similarity


movies, similarity = load_data()

# =====================================================
# TMDB REQUEST
# =====================================================

@st.cache_data(ttl=3600)
def tmdb_request(movie_title):

    url = "https://api.themoviedb.org/3/search/movie"

    params = {
        "api_key": API_KEY,
        "query": movie_title,
        "language": "en-US",
        "include_adult": False
    }

    for attempt in range(5):

        try:

            response = requests.get(
                url,
                params=params,
                timeout=30,
                verify=False
            )

            if response.status_code == 200:

                data = response.json()

                return data.get(
                    "results",
                    []
                )

            if response.status_code == 401:

                return "INVALID_KEY"

            time.sleep(1)

        except requests.exceptions.RequestException:

            time.sleep(2)

        except Exception:

            time.sleep(2)

    return []

# =====================================================
# FIND BEST MOVIE MATCH
# =====================================================

def find_best_match(
    movie_title,
    results
):

    if not results:

        return None

    target = movie_title.lower().strip()

    # EXACT MATCH
    for movie in results:

        title = movie.get(
            "title",
            ""
        ).lower().strip()

        if title == target:

            return movie

    # BEST SIMILAR MATCH
    best_movie = None
    best_score = 0

    for movie in results:

        title = movie.get(
            "title",
            ""
        ).lower().strip()

        score = SequenceMatcher(
            None,
            target,
            title
        ).ratio()

        if score > best_score:

            best_score = score
            best_movie = movie

    if best_score >= 0.55:

        return best_movie

    return results[0]

# =====================================================
# FETCH MOVIE DETAILS
# =====================================================

@st.cache_data(ttl=3600)
def fetch_movie_details(movie_title):

    results = tmdb_request(
        movie_title
    )

    if results == "INVALID_KEY":

        return {
            "title": movie_title,
            "poster": "",
            "rating": None,
            "release": "N/A",
            "overview": "TMDB API key is invalid.",
            "language": "N/A",
            "popularity": None
        }

    if not results:

        return {
            "title": movie_title,
            "poster": "",
            "rating": None,
            "release": "N/A",
            "overview": (
                "Movie details are currently unavailable."
            ),
            "language": "N/A",
            "popularity": None
        }

    selected_movie = find_best_match(
        movie_title,
        results
    )

    if selected_movie is None:

        return {
            "title": movie_title,
            "poster": "",
            "rating": None,
            "release": "N/A",
            "overview": "No movie details available.",
            "language": "N/A",
            "popularity": None
        }

    poster = ""

    if selected_movie.get("poster_path"):

        poster = (
            "https://image.tmdb.org/t/p/w500"
            + selected_movie["poster_path"]
        )

    rating = selected_movie.get(
        "vote_average"
    )

    if rating is not None:

        rating = round(
            rating,
            1
        )

    popularity = selected_movie.get(
        "popularity"
    )

    if popularity is not None:

        popularity = round(
            popularity,
            2
        )

    overview = selected_movie.get(
        "overview"
    )

    if not overview:

        overview = "No synopsis available."

    return {

        "title": selected_movie.get(
            "title",
            movie_title
        ),

        "poster": poster,

        "rating": rating,

        "release": selected_movie.get(
            "release_date",
            "N/A"
        ),

        "overview": overview,

        "language": selected_movie.get(
            "original_language",
            "N/A"
        ).upper(),

        "popularity": popularity
    }

# =====================================================
# RECOMMENDATION FUNCTION
# =====================================================

def recommend(movie):

    movie_index = movies[
        movies["title"] == movie
    ].index[0]

    distances = similarity[movie_index]

    movie_list = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:6]

    recommendations = []

    for index, score in movie_list:

        movie_title = movies.iloc[
            index
        ]["title"]

        movie_details = fetch_movie_details(
            movie_title
        )

        movie_details["similarity"] = round(
            score * 100,
            1
        )

        recommendations.append(
            movie_details
        )

    return recommendations

# =====================================================
# HERO SECTION
# =====================================================



st.title("🎬 CineMatch")

st.write(
    "Discover movies you'll love using "
    "content-based machine learning recommendations."
)

# =====================================================
# PROJECT STATS
# =====================================================

col1, col2, col3 = st.columns(3)

with col1:

    st.metric(
        "🎞️ Total Movies",
        f"{len(movies):,}"
    )

with col2:

    st.metric(
        "🧠 Recommendation",
        "Content-Based"
    )

with col3:

    st.metric(
        "🎯 Similarity",
        "Cosine Similarity"
    )

st.divider()

# =====================================================
# MOVIE SELECTOR
# =====================================================

st.markdown(
    '<div class="section-title">🔍 Find Your Next Movie</div>',
    unsafe_allow_html=True
)

st.caption(
    "Select a movie and discover similar movies using machine learning."
)

movie_list = movies["title"].values

selected_movie = st.selectbox(
    "Select a Movie",
    movie_list
)

recommend_button = st.button(
    "✨ Recommend Similar Movies",
    use_container_width=True
)

# =====================================================
# RECOMMENDATIONS
# =====================================================

if recommend_button:

    with st.spinner(
        "Finding the best movie recommendations..."
    ):

        recommendations = recommend(
            selected_movie
        )

    st.divider()

    st.markdown(
        f"""
        <div class="section-title">
        🎬 Movies Similar to {selected_movie}
        </div>
        """,
        unsafe_allow_html=True
    )

    cols = st.columns(5)

    for col, movie in zip(
        cols,
        recommendations
    ):

        with col:

            st.markdown(
                '<div class="movie-card">',
                unsafe_allow_html=True
            )

            # POSTER
            if movie["poster"]:

                st.image(
                    movie["poster"],
                    use_container_width=True
                )

            else:

                st.markdown(
                    """
                    <div style="
                    height:420px;
                    background:#1e293b;
                    border-radius:10px;
                    display:flex;
                    align-items:center;
                    justify-content:center;
                    color:#94a3b8;
                    ">
                    🎬 Poster unavailable
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            # TITLE
            st.markdown(
                f"""
                <div class="movie-title">
                {movie['title']}
                </div>
                """,
                unsafe_allow_html=True
            )

            # RATING
            rating = movie["rating"]

            if rating is None:

                rating_text = "N/A"

            else:

                rating_text = f"{rating} / 10"

            # RELEASE
            release = movie["release"]

            if release != "N/A":

                release = release[:4]

            # POPULARITY
            popularity = movie["popularity"]

            if popularity is None:

                popularity_text = "N/A"

            else:

                popularity_text = popularity

            # INFO
            st.markdown(
                f"""
                <div class="movie-info">

                ⭐ Rating: {rating_text}

                <br>

                📅 Release: {release}

                <br>

                🌐 Language: {movie['language']}

                <br>

                🔥 Popularity: {popularity_text}

                </div>

                <div class="similarity">

                🎯 Similarity: {movie['similarity']}%

                </div>
                """,
                unsafe_allow_html=True
            )

            # SYNOPSIS
            with st.expander(
                "📖 Movie Synopsis"
            ):

                st.write(
                    movie["overview"]
                )

            st.markdown(
                "</div>",
                unsafe_allow_html=True
            )

# =====================================================
# PROJECT DETAILS
# =====================================================

st.divider()

st.markdown(
    '<div class="section-title">📌 Project Details</div>',
    unsafe_allow_html=True
)

st.write(
    "CineMatch is a machine learning based movie recommendation system."
)

st.write(
    "The system uses a **Content-Based Filtering** approach "
    "to recommend movies based on content similarity."
)

st.markdown(
    '<div class="section-title">🚀 How It Works</div>',
    unsafe_allow_html=True
)

st.markdown(
    """
    1. Movie data is processed using Python and Pandas.
    2. Movie features are converted into numerical vectors.
    3. Cosine Similarity is used to find similar movies.
    4. TMDB API provides movie posters and information.
    5. Streamlit creates the interactive user interface.
    """
)

st.divider()

st.caption(
    "CineMatch | AI Movie Recommendation System | Developed by Disha Goyal"
)