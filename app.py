import streamlit as st
import pickle
import pandas as pd

import os
from dotenv import load_dotenv
import requests

load_dotenv()  # loads .env in development
API_KEY = os.getenv("API_KEY")


movies = pickle.load(open('movies_dict.pkl','rb'))
movies_list = pd.DataFrame(movies)
print(movies_list.head())
similarity = pickle.load(open('similarity.pkl', 'rb'))

# Poster fetch
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&language=en-US"
    response = requests.get(url)

    if response.status_code != 200:
        print(f"Error: {response.status_code}, could not fetch movie {movie_id}")
        return None

    data = response.json()
    poster_path = data.get("poster_path")
    
    if poster_path:
        full_path = f"https://image.tmdb.org/t/p/w500{poster_path}"
        return full_path
    else:
        return None

# Recommend function
def recommend(movie):
    movie_index = movies_list[movies_list['title'] == movie].index[0]
    distances = similarity[movie_index]
    top_movies = sorted(list(enumerate(distances)), reverse=True, key=lambda x:x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []
    for movie in top_movies:
        #movie_id = 
        recommended_movies.append(movies_list.iloc[movie[0]]['title']) # extracting movie name
        recommended_movies_posters.append(fetch_poster(movies_list.iloc[movie[0]]['id'])) # fetch movie image from api
    return recommended_movies, recommended_movies_posters

st.title("Movie Recommender System.")

selected_movie = st.selectbox(
    "Select Movie:", movies_list['title'].values
)

if st.button("Recommend"):
    recommendations, posters = recommend(selected_movie)

    cols = st.columns(5)
    for i in range(5):
        with cols[i]:
            st.text(recommendations[i])
            if posters[i]:  
                st.image(posters[i])
            else:
                st.warning("Poster not available")


    #st.write("Recommended Movies:")
    # for movie in recommendations:
    #     st.write(movie)
    #st.write(selected_movie)
