import streamlit  as st
import pickle
import pandas as pd
import requests


def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=<YOUR API KEY>&language=en-US".format(
        movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path


def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_lists = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    recommend_movies = []
    recommended_movies_poster = []
    for i in movies_lists:
        movie_id = movies.iloc[i[0]].movie_id
        # fetch poster

        recommend_movies.append(movies.iloc[i[0]].title)
        recommended_movies_poster.append(fetch_poster(movie_id))
    return recommend_movies, recommended_movies_poster


movies_list = pickle.load(open('movies.pkl', 'rb'))
movies = pd.DataFrame(movies_list)
movies_list = movies_list['title'].values
st.title('Movie Recommender System')
option = st.selectbox('How would you like to be connected ?',
                      movies_list
                      )
similarity = pickle.load(open('similarity.pkl', 'rb'))
st.write('You selected :', option)

if st.button('Recommend'):
    recommendations, posters = recommend(option)
    img1, img2, img3, img4, img5 = st.columns(5)
    style = "<style>h6 {text-align: center;}</style>"

    with img1:
        st.markdown(f'<div style="font-size: 15px">{recommendations[0]}</div>', unsafe_allow_html=True)
        st.image(posters[0])

    with img2:
        st.markdown(f'<div style="font-size: 15px">{recommendations[1]}</div>', unsafe_allow_html=True)
        st.image(posters[1])

    with img3:
        st.markdown(f'<div style="font-size: 15px">{recommendations[2]}</div>', unsafe_allow_html=True)
        st.image(posters[2])

    with img4:
        st.markdown(f'<div style="font-size: 15px ">{recommendations[3]}</div>', unsafe_allow_html=True)
        st.image(posters[3])

    with img5:
        st.markdown(f'<div style="font-size: 15px">{recommendations[4]}</div>', unsafe_allow_html=True)
        st.image(posters[4])
