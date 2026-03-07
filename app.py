import streamlit as st
import pickle
import requests
import pandas as pd

st.title('Movie Recommendation System')
session = requests.Session()

@st.cache_data
@st.cache_data
def fetch_poster(movie_title):
    url = f"https://www.omdbapi.com/?t={movie_title}&apikey=eb6c2602"
    
    try:
        response = requests.get(url)
        data = response.json()
        poster = data.get("Poster")
    except:
        return "https://via.placeholder.com/342x500?text=Error"

    if poster and poster != "N/A":
        return poster
    else:
        return "https://via.placeholder.com/342x500?text=No+Image"

@st.cache_data
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_posters = []

    for i in movies_list:
        title = movies.iloc[i[0]].title
        recommended_movies.append(title)
        recommended_posters.append(fetch_poster(title))
    
    return recommended_movies, recommended_posters

movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))

selected_movie_name = st.selectbox("Select a movie", movies['title'].values)

if st.button("Recommend"):
    names, posters = recommend(selected_movie_name)

    cols = st.columns(5)
    for i, col in enumerate(cols):
        with col:
            st.text(names[i])
            st.image(posters[i])
