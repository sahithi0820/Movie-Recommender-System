import streamlit as st
import pickle
import requests
import time
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

st.set_page_config(
    page_title="Movie Recommender System",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown(""" 
            <style>
            .stApp {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            }

            .main-header {
            font-size: 3.5rem;
            font-weight: 800;
            text-align: center;
            color: #FFFFFF;
            margin-bottom: 1rem;
            text-shadow: 3px 3px 6px rgba(0,0,0,0.5);
            padding: 1rem;
            background: rgba(0,0,0,0.3);
            border-radius: 15px;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255,255,255,0.1);
            }

            .subtitle {
            text-align: center; 
            color: white; 
            font-size: 1.3rem; 
            margin-bottom: 2rem;
            font-weight: 300;
            text-shadow: 1px 1px 2px rgba(0,0,0,0.5);
            }

            .selectbox-container{
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            padding: 2rem;
            border-radius: 20px;
            border: 1px solid rgba(255, 255, 255, 0.2);
            margin-bottom: 2rem;
            }

            .stSelectbox > div > div {
            background: rgba(255, 255, 255, 0.9);
            border-radius: 10px;
            border: none;
            padding: 10px;
            }

            .stButton > button {
            background: linear-gradient(45deg, #FF6B6B, #FF8E53);
            color: white;
            border: none;
            padding: 15px 40px;
            border-radius: 25px;
            font-weight: 600;
            font-size: 1.1rem;
            transition: all 0.3s ease;
            margin: 2rem 0;
            width: 100%;
            }
        
            .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(255, 107, 107, 0.4);
            }

            .movie-column {
            padding: 1.5rem !important;
            text-align: center;
        }
        
            .movie-title {
            font-weight: 500;
            font-size: 1rem;
            color: white;
            text-align: center;
            margin-top: 1.5rem;
            margin-bottom: 1rem;
            
            min-height: 4rem;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 1rem;
            background: rgba(0,0,0,0.6);
            border-radius: 12px;
            backdrop-filter: blur(5px);
            line-height: 1.4;
        }
        
            .movie-poster-container {
            padding: 0.5rem;
            border-radius: 20px;
            background: rgba(255,255,255,0.1);
            backdrop-filter: blur(10px);
            margin: 0.5rem;
        }
            .movie-poster {
            border-radius: 15px;
            box-shadow: 0 12px 30px rgba(0,0,0,0.4)
            transition: all 0.3s ease;
            width: 100%;
            height: 380px;
            object-fit: cover;
        }
        
            .movie-poster:hover {
            transform: scale(1.05);
            box-shadow: 0 15px 40px rgba(0,0,0,0.6);
        }
        
            .background-pattern {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            opacity: 0.1;
            z-index: -1;
            background-image: url('https://images.unsplash.com/photo-1489599809505-fb40ebc6f13f?ixlib=rb-4.0.3');
            background-size: cover;
        }
        
            .success-message {
            text-align: center;
            font-size: 1.6rem;
            font-weight: 600;
            color: #00ff88;
            margin: 3rem 0;
            text-shadow: 1px 1px 2px rgba(0,0,0,0.5);
            padding: 1.5rem;
            background: rgba(0,0,0,0.4);
            border-radius: 15px;
        }
        
            
            .error-message {
            text-align: center;
            font-size: 1.2rem;
            font-weight: 600;
            color: #ff6b6b;
            margin: 2rem 0;
            padding: 1.5rem;
            background: rgba(255,0,0,0.1);
            border-radius: 15px;
            border: 1px solid rgba(255,0,0,0.3);
        }
            
        /* Remove extra spacing and borders from columns */
        .stColumn {
            padding: 1rem !important;
        }
        
        .block-container {
            padding-top: 2rem;
            max-width: 1200px
        }
            
        .recommendation-grid {
            margin: 2rem 0;
            padding: 1rem;
        }
    </style>

    <div class="background-pattern"></div>
    """, unsafe_allow_html=True) 

# Header with gradient text
st.markdown('<h1 class="main-header">🎬 CineMatch</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Discover Your Next Favorite Movie</p>', unsafe_allow_html=True)

# Create a session with retry strategy
def create_session():
    session = requests.Session()
    retry_strategy = Retry(
        total=3,
        backoff_factor=1,
        status_forcelist=[429, 500, 502, 503, 504],
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    return session

def fetch_poster(movie_id):
   url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
   # Try multiple times with delays
   for attempt in range(3):
    try:
            session = create_session()
            response = session.get(url, timeout=10)
            response.raise_for_status()  # Raise an exception for bad status codes
            data = response.json()
            
            # Check if poster path exists
            if 'poster_path' in data and data['poster_path']:
                poster_path = data['poster_path']
                full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
                return full_path
            else:
                # Return a placeholder image if no poster found
                return "https://via.placeholder.com/500x750/333333/FFFFFF?text=No+Poster+Available"
                
    except requests.exceptions.RequestException as e:
            if attempt < 2:  # If not the last attempt
                time.sleep(2)  # Wait 2 seconds before retrying
                continue
            else:
                st.error(f"Failed to fetch poster after 3 attempts: {str(e)}")
                # Return a placeholder image on error
                return "https://via.placeholder.com/500x750/666666/FFFFFF?text=Error+Loading+Poster"
    
    return "https://via.placeholder.com/500x750/666666/FFFFFF?text=Error+Loading+Poster"


def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        # fetch the movie poster
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)

    return recommended_movie_names,recommended_movie_posters

movies = pickle.load(open('movies.pkl', 'rb'))
movies_list = movies['title'].values
similarity = pickle.load(open('similarity.pkl', 'rb'))
selected_movie = st.selectbox('Type or Select a movie', movies_list)


# Recommendation button with custom styling
col1, col2, col3 = st.columns([1,2,1])
with col2:
    if st.button(
        '✨ Get Movie Recommendations', 
        key='recommend',
        use_container_width=True
    ):
        with st.spinner('🎥 Finding your perfect movie matches...'):
            recommended_movie_names, recommended_movie_posters = recommend(selected_movie)
            
            # Success message
            st.markdown(f'<div class="success-message">🎉 Top recommendations based on <b>"{selected_movie}"</b></div>', unsafe_allow_html=True)
            
            # Display recommendations in beautiful cards
            cols = st.columns(5)
            for idx, col in enumerate(cols):
                with col:
                    st.markdown('<div class="movie-card">', unsafe_allow_html=True)
                    st.image(
                        recommended_movie_posters[idx], 
                        use_column_width=True,
                        output_format="auto"
                    )
                    st.markdown(f'<div class="movie-title">{recommended_movie_names[idx]}</div>', unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("""
<br><br>
<div style="text-align: center; color: white; opacity: 0.7;">
    <p>Made with ❤️ using Streamlit | Movie data from TMDB</p>
</div>
""", unsafe_allow_html=True)