pip install scikit-learn
import streamlit as st
import pickle
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

# Load the merged dataset
with open('merged_df.pkl', 'rb') as file:
    merged_df = pickle.load(file)

# Extract unique genres, movie titles, and user IDs
unique_genres = sorted(merged_df['genres'].dropna().unique())
unique_movies = sorted(merged_df['title'].dropna().unique())
unique_users = sorted(merged_df['userId'].dropna().unique())

# -----------------------------------------
# Recommendation Functions
# -----------------------------------------

def popularity_based_recommendation(genres, reviews, top):
    """Recommend top-rated movies based on popularity within a selected genre."""
    genre_movies = merged_df[merged_df['genres'] == genres]
    movie_ratings = genre_movies.groupby('movieId').agg(
        avg_rating=('rating', 'mean'),
        num_reviews=('rating', 'count')
    ).reset_index()

    # Filter movies with minimum required reviews
    movie_ratings = movie_ratings[movie_ratings['num_reviews'] >= reviews]

    # Sort movies by average rating
    top_movies = movie_ratings.sort_values(by='avg_rating', ascending=False).head(top)

    # Merge to get movie titles
    top_movies = top_movies.merge(merged_df[['movieId', 'title']].drop_duplicates(), on='movieId', how='left')

    return top_movies[['title', 'avg_rating', 'num_reviews']]

def content_based_recommendation(movie_title, top_n):
    """Recommend movies based on content similarity (shared genres)."""
    
    # Get the movie genre
    movie_genres = merged_df[merged_df['title'] == movie_title]['genres'].values[0]

    # Find similar movies in the same genre
    similar_movies = merged_df[merged_df['genres'] == movie_genres]

    # Compute average ratings and number of reviews
    movie_ratings = similar_movies.groupby('movieId').agg(
        avg_rating=('rating', 'mean'),
        num_reviews=('rating', 'count')
    ).reset_index()

    # Get top recommended movies
    top_movies = movie_ratings.sort_values(by='avg_rating', ascending=False).head(top_n)

    # Merge with movie titles
    top_movies = top_movies.merge(merged_df[['movieId', 'title']].drop_duplicates(), on='movieId', how='left')

    return top_movies[['title', 'avg_rating', 'num_reviews']]


def collaborative_based_recommendation(user_id, top_n, k):
    """Recommend movies using collaborative filtering based on similar users' preferences."""
    # Create a user-movie ratings matrix
    user_movie_ratings = merged_df.pivot_table(index='userId', columns='movieId', values='rating')

    # Compute cosine similarity between users
    user_similarity = cosine_similarity(user_movie_ratings.fillna(0))

    # Identify the k most similar users
    similar_users = user_similarity[user_id - 1].argsort()[-(k+1):-1]

    # Get movie ratings from similar users
    similar_users_ratings = merged_df[merged_df['userId'].isin(similar_users)]

    # Aggregate movie ratings
    top_movies = similar_users_ratings.groupby('movieId').agg(
        avg_rating=('rating', 'mean'),
        num_reviews=('rating', 'count')
    ).reset_index()

    # Get top movies based on average rating
    top_movies = top_movies.sort_values(by='avg_rating', ascending=False).head(top_n)

    # Merge to get movie titles
    top_movies = top_movies.merge(merged_df[['movieId', 'title']].drop_duplicates(), on='movieId', how='left')

    return top_movies[['title', 'avg_rating', 'num_reviews']]

# -----------------------------------------
# Streamlit App Layout
# -----------------------------------------

st.title("Movie Recommendation System By Corban Enam Bubutor")

# Sidebar selection to choose which recommender to use
recommender_type = st.sidebar.selectbox(
    "Select Recommendation Type",
    ("Popularity Based", "Content-Based", "Collaborative Filtering")
)

if recommender_type == "Popularity Based":
    st.header("Genre-Based Recommendation")
    genre = st.selectbox("Select Genre", unique_genres)
    min_reviews = st.number_input("Minimum Number of Reviews", min_value=1, value=50)
    top_n = st.number_input("Number of Recommendations", min_value=1, value=10)
    
    if st.button("Get Recommendations"):
        recommendations = popularity_based_recommendation(genre, min_reviews, top_n)
        st.write(recommendations)

elif recommender_type == "Content-Based":
    st.header("Movie Similarity Recommendation")
    movie = st.selectbox("Select a Movie", unique_movies)
    top_n = st.number_input("Number of Similar Movies", min_value=1, value=10)
    
    if st.button("Get Recommendations"):
        recommendations = content_based_recommendation(movie, top_n)
        st.write(recommendations)

elif recommender_type == "Collaborative Filtering":
    st.header("User-Based Recommendation")
    user_id = st.selectbox("Select User ID", unique_users)
    top_n = st.number_input("Number of Recommended Movies", min_value=1, value=10)
    k = st.number_input("Number of Similar Users (k)", min_value=1, value=5)
    
    if st.button("Get Recommendations"):
        recommendations = collaborative_based_recommendation(user_id, top_n, k)
        st.write(recommendations)
