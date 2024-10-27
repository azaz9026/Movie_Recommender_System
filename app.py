import pickle
import streamlit as st
import requests

# Load the data
movies = pickle.load(open('movie_list.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

# Set up TMDb API
TMDB_API_KEY = "26792435acd673fbf4f46dcfd0906aa8"  # Replace with your TMDb API key
TMDB_BASE_URL = "https://api.themoviedb.org/3/search/movie"
TMDB_IMAGE_BASE_URL = "https://image.tmdb.org/t/p/w500"  # w500 is the image width, can be changed

def fetch_poster_url(movie_title):
    """Fetches the movie poster URL from TMDb API or returns a placeholder URL if not available."""
    response = requests.get(
        TMDB_BASE_URL,
        params={"api_key": TMDB_API_KEY, "query": movie_title}
    )
    if response.status_code == 200:
        data = response.json()
        if data['results']:
            poster_path = data['results'][0].get('poster_path')
            if poster_path:
                return f"{TMDB_IMAGE_BASE_URL}{poster_path}"
    # Placeholder image if no poster is found
    return "https://via.placeholder.com/500x750?text=No+Image+Available"

# Title and Introduction
st.title("🎬 Movie Recommender System")
st.markdown("### Discover movies similar to your favorites!")
st.write("Select a movie from the dropdown, and we'll recommend five similar movies tailored to your taste. Enjoy exploring! 🍿")

# Movie selection
movie_list = movies['title'].values
selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list
)

# Recommendation function
def get_recommendations(movie_title):
    index = movies[movies['title'] == movie_title].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])

    recommended_movies = []
    for i in distances[1:6]:
        movie_data = {
            'title': movies.iloc[i[0]].title,
            'poster_url': fetch_poster_url(movies.iloc[i[0]].title),
            'genre': movies.iloc[i[0]].get('genre', 'Genre N/A'),
            'rating': movies.iloc[i[0]].get('rating', 'Rating N/A')
        }
        recommended_movies.append(movie_data)
    
    return recommended_movies

# Show recommendations with improved layout and styling
if st.button("Show Recommendations"):
    st.subheader(f"Movies recommended for: {selected_movie}")
    recommended_movies = get_recommendations(selected_movie)

    # Display recommendations in a structured layout
    for movie in recommended_movies:
        with st.container():
            st.markdown(f"#### {movie['title']}")
            col1, col2 = st.columns([1, 3])
            
            with col1:
                st.image(movie['poster_url'], width=120)  # Movie poster
            with col2:
                st.write(f"**Genre:** {movie['genre']}")
                st.write(f"**Rating:** {movie['rating']} ⭐")
                # Optional: Add any additional info like release date, director, etc.

        # Divider with icon and text
        st.markdown("""
            <div style="text-align: center; margin: 20px 0;">
                <span style="font-size: 24px; color: #888;">🎞️</span>
                <span style="font-size: 16px; color: #888; margin-left: 5px;">Scroll down for more recommendations</span>
            </div>
            """, unsafe_allow_html=True)
