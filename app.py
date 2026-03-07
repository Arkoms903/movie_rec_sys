import streamlit as st
import pickle
import requests
import pandas as pd

# Page Config
st.set_page_config(
    page_title="Movie Recommender",
    page_icon="🎬",
    layout="wide"
)

# Netflix Style CSS
st.markdown("""
<style>

/* App background */
.stApp {
    background: linear-gradient(to bottom, #0f0f0f, #141414);
    color: white;
}

/* Title */
h1 {
    text-align: center;
    color: #E50914;
    font-size: 60px;
    font-weight: bold;
}

/* Subtitle */
.subtitle {
    text-align: center;
    color: #bbbbbb;
    font-size: 20px;
}

/* Button styling */
.stButton>button {
    background-color: #E50914;
    color: white;
    border-radius: 10px;
    height: 3.2em;
    width: 220px;
    font-size: 18px;
    border: none;
    transition: 0.3s;
}

.stButton>button:hover {
    background-color: #b20710;
    transform: scale(1.05);
}

/* Movie cards */
.movie-card {
    text-align: center;
    padding: 10px;
    border-radius: 12px;
    transition: transform 0.3s;
}

.movie-card:hover {
    transform: scale(1.08);
}

</style>
""", unsafe_allow_html=True)

# Title Section
st.markdown("<h1>🎬 Movie Recommender</h1>", unsafe_allow_html=True)

st.markdown(
    "<p class='subtitle'>Find movies similar to your favorites instantly 🍿</p>",
    unsafe_allow_html=True
)

# Load data
movies_dict = pickle.load(open("movie_dict.pkl", "rb"))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open("similarity.pkl", "rb"))

# Poster Fetch Function
@st.cache_data
def fetch_poster(movie_title):

    url = f"https://www.omdbapi.com/?t={movie_title}&apikey=eb6c2602"

    try:
        data = requests.get(url).json()
        poster = data.get("Poster")
    except:
        return "https://via.placeholder.com/342x500?text=Error"

    if poster and poster != "N/A":
        return poster
    else:
        return "https://via.placeholder.com/342x500?text=No+Image"

# Recommendation Function
@st.cache_data
def recommend(movie):

    movie_index = movies[movies['title'] == movie].index[0]

    similar_movies = similarity[movie_index][:5]

    recommended_movies = []
    recommended_posters = []

    for i in similar_movies:
        title = movies.iloc[i]['title']
        recommended_movies.append(title)
        recommended_posters.append(fetch_poster(title))

    return recommended_movies, recommended_posters


# Movie Selection
selected_movie_name = st.selectbox(
    "🎥 Select a Movie",
    movies['title'].values
)

# Recommendation Button
if st.button("🍿 Recommend Movies"):

    names, posters = recommend(selected_movie_name)

    st.markdown("## 🔥 Top Picks For You")

    cols = st.columns(5)

    for i in range(5):
        with cols[i]:
            st.markdown("<div class='movie-card'>", unsafe_allow_html=True)
            st.image(posters[i])
            st.markdown(f"**{names[i]}**")
            st.markdown("</div>", unsafe_allow_html=True)

# Footer
st.markdown("---")

st.markdown(
    "<center>Built with ❤️ using Streamlit | Posters via OMDb API</center>",
    unsafe_allow_html=True
)