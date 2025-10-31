import streamlit as st
import pickle
import pandas as pd


movies = pickle.load(open('movies_dict.pkl','rb'))
movies_list = pd.DataFrame(movies)
#print(movies_list.head())
similarity = pickle.load(open('similarity.pkl', 'rb'))

# Recommend function
def recommend(movie):
    movie_index = movies_list[movies_list['title'] == movie].index[0]
    distances = similarity[movie_index]
    top_movies = sorted(list(enumerate(distances)), reverse=True, key=lambda x:x[1])[1:6]

    recommended_movies = []
    for movie in top_movies:
        recommended_movies.append(movies_list.iloc[movie[0]]['title'])
    return recommended_movies

st.title("Movie Recommender System.")

selected_movie = st.selectbox(
    "Select Movie:", movies_list['title'].values
)

if st.button("Recommend"):
    recommendations = recommend(selected_movie)
    #st.write("Recommended Movies:")
    for movie in recommendations:
        st.write(movie)
    #st.write(selected_movie)
