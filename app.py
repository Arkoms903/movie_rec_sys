import streamlit as st
import pickle
import requests
import pandas as pd

# ---------------- PAGE TITLE ----------------
st.set_page_config(page_title="Movie Recommendation System", page_icon="🎬")
st.title("🎬 Movie Recommendation System")

# ---------------- LOAD FILES ----------------
movies_dict = pickle.load(open("movie_dict.pkl", "rb"))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open("similarity.pkl", "rb"))

# ---------------- FETCH POSTER ----------------
@st.cache_data(ttl=3600)
def fetch_poster(movie_title):
    url = f"https://www.omdbapi.com/?t={movie_title}&apikey=eb6c2602"

    try:
        response = requests.get(url, timeout=3)
        data = response.json()
        poster = data.get("Poster")
        
        if poster and poster != "N/A":
            return poster
    except:
        pass
    
    return "https://via.placeholder.com/300x450?text=No+Image"

# ---------------- RECOMMEND FUNCTION ----------------
@st.cache_data
def recommend(movie):
    movie_index = movies[movies["title"] == movie].index[0]

    # similarity scores of selected movie
    distances = similarity[movie_index]

    # sort by highest similarity
    movies_list = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:6]   # skip itself, take top 5

    recommended_movies = []
    recommended_posters = []

    for i in movies_list:
        movie_id = i[0]
        title = movies.iloc[movie_id]["title"]
        recommended_movies.append(title)
        recommended_posters.append(fetch_poster(title))

    return recommended_movies, recommended_posters

# ---------------- UI ----------------
selected_movie_name = st.selectbox(
    "Select a movie",
    movies["title"].values
)

if st.button("Recommend", use_container_width=True):
    # Show loading message
    with st.spinner("Finding recommendations..."):
        names, posters = recommend(selected_movie_name)

    cols = st.columns(5, gap="medium")

    for i in range(5):
        with cols[i]:
            st.image(posters[i], use_container_width=True)
            st.markdown(f"<p style='text-align: center; font-weight: bold; font-size: 14px;'>{names[i]}</p>", unsafe_allow_html=True)

# Optional debug
# st.write(similarity[0][:10])