from dotenv import load_dotenv
import os
import pickle
import streamlit as st
import requests

# Load API Key
load_dotenv()

api_key = os.getenv("TMDB_API_KEY")


# Fetch poster from TMDB
def fetch_poster(movie_id):
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=en-US"

        response = requests.get(url, timeout=10)
        response.raise_for_status()

        data = response.json()

        poster_path = data.get('poster_path')

        if poster_path:
            full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
            return full_path
        else:
            return "https://via.placeholder.com/300x450?text=No+Poster"

    except:
        return "https://via.placeholder.com/300x450?text=Error"


# Recommendation Function
def recommend(movie):

    index = movies[movies['title'] == movie].index[0]

    distances = sorted(
        list(enumerate(similarity[index])),
        reverse=True,
        key=lambda x: x[1]
    )

    recommended_movie_names = []
    recommended_movie_posters = []

    for i in distances[1:6]:

        movie_id = movies.iloc[i[0]].movie_id

        recommended_movie_names.append(
            movies.iloc[i[0]].title
        )

        recommended_movie_posters.append(
            fetch_poster(movie_id)
        )

    return recommended_movie_names, recommended_movie_posters


# Streamlit UI
st.title("Movie Recommender System")

movies = pickle.load(open('movie_list.pkl', 'rb'))

 import zipfile
import os

if not os.path.exists("similarity.pkl"):
    with zipfile.ZipFile("similarity.zip", "r") as zip_ref:
        zip_ref.extractall()

similarity = pickle.load(open('similarity.pkl', 'rb'))   

movie_list = movies['title'].values

selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list
)


if st.button('Show Recommendation'):

    recommended_movie_names, recommended_movie_posters = recommend(selected_movie)

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.write(recommended_movie_names[0])
        st.image(recommended_movie_posters[0], width=150)

    with col2:
        st.write(recommended_movie_names[1])
        st.image(recommended_movie_posters[1], width=150)

    with col3:
        st.write(recommended_movie_names[2])
        st.image(recommended_movie_posters[2], width=150)

    with col4:
        st.write(recommended_movie_names[3])
        st.image(recommended_movie_posters[3], width=150)

    with col5:
        st.write(recommended_movie_names[4])
        st.image(recommended_movie_posters[4], width=150)