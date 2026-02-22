import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import random

# --- 1. CONFIG ---
st.set_page_config(page_title="VibeLab Pro", page_icon="🔥", layout="centered")

if 'lang' not in st.session_state: st.session_state.lang = 'EN'
if 'tracks' not in st.session_state: st.session_state.tracks = []

# --- 2. ELITE CSS (ZERO SYNTAX ERRORS) ---
st.markdown(r"""
<style>
    .stApp { background-color: #0b0d11; color: #ffffff; }
    .main-title { 
        background: linear-gradient(90deg, #1DB954, #19e68c);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 70px; font-weight: 900; text-align: center; margin-bottom: 0px;
    }
    .stButton>button { 
        background: linear-gradient(45deg, #1DB954, #1ed760) !important; 
        color: white !important; font-weight: bold; border-radius: 30px; 
        height: 55px; width: 100%; border: none; font-size: 18px;
    }
    .stSelectbox label, .stTextInput label { color: #1DB954 !important; font-size: 1.1rem !important; }
    .song-card { 
        background: rgba(255,255,255,0.03); padding: 20px; border-radius: 20px; 
        margin-bottom: 15px; border: 1px solid rgba(255,255,255,0.1);
        display: flex; align-items: center; gap: 20px; transition: transform 0.2s;
    }
    .song-card:hover { transform: scale(1.02); background: rgba(255,255,255,0.07); }
    .pop-tag { background: #1DB954; color: black; padding: 2px 8px; border-radius: 10px; font-size: 10px; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# --- 3. EXPANDED CONTENT DATA ---
# הוספתי כאן המון ז'אנרים ואווירות כדי שלא ישעמם
GENRES = {
    'EN': ["Global Pop", "Hard Rock", "Deep House", "Melodic Techno", "Lo-Fi Hip Hop", "Latin Hits", "Jazz Fusion", "Afrobeats", "K-Pop", "80s Retro"],
    'HE': ["מזרחית פרימיום", "פופ ישראלי", "היפ הופ ציוני", "רוק ישראלי", "נוסטלגיה", "אלקטרוניקה", "חסידי מודרני", "אינדי מקומי"],
}
VIBES = {
    'EN': ["Summer Party", "Sad Hours", "Workout Power", "Night Drive", "Coffee Shop", "Meditation", "Gaming Focus"],
    'HE': ["מסיבה מטורפת", "שקיעה רומנטית", "רעל בעיניים", "נסיעת לילה", "רוגע מוחלט", "יום עבודה", "דיכאון איכותי"],
}

DATA = {
    'EN': {'title': 'VIBELAB PRO', 'name': 'Full Name', 'gen_label': 'Select Genre', 'vib_label': 'Select Vibe', 'btn': 'DISCOVER SOUNDS ⚡', 'surprise': 'SURPRISE ME 🎲'},
    'HE': {'title': 'וייב-לאב PRO', 'name': 'שם מלא', 'gen_label': 'בחר ז\'אנר', 'vib_label': 'מה האווירה?', 'btn': 'תביא לי להיטים ⚡', 'surprise': 'הפתע אותי 🎲'}
}

# --- 4. SPOTIFY ---
@st.cache_resource
def connect_spotify():
    try:
        return spotipy.Spotify(auth_manager=SpotifyClientCredentials(
            client_id=st.secrets["CLIENT_ID"].strip(),
            client_secret=st.secrets["CLIENT_SECRET"].strip()
        ))
    except: return None

sp = connect_spotify()

# --- 5. UI ---
c_lang = st.columns([5, 1, 1])
with c_lang[1]: 
    if st.button("EN"): st.session_state.lang = 'EN'
with c_lang[2]: 
    if st.button("HE"): st.session_state.lang = 'HE'

L = DATA[st.session_state.lang]
current_genres = GENRES[st.session_state.lang]
current_vibes = VIBES[st.session_state.lang]

st.markdown(f'<h1 class="main-title">{L["title"]}</h1>', unsafe_allow_html=True)
st.write(f"<p style='text-align:center; color:#888;'>Smart curation for music addicts</p>", unsafe_allow_html=True)

u_name = st.text_input(L['name'], placeholder="Enter your name...")

col1, col2 = st.columns(2)
with col1:
    u_genre = st.selectbox(L['gen_label'], current_genres)
with col2:
    u_vibe = st.selectbox(L['vib_label'], current_vibes)

# כפתורי פעולה
btn_col1, btn_col2 = st.columns([2, 1])
generate_btn = btn_col1.button(L['btn'])
surprise_btn = btn_col2.button(L['surprise'])

search_query = None
if generate_btn:
    search_query = f"{u_genre} {u_vibe}"
elif surprise_btn:
    u_genre = random.choice(current_genres)
    u_vibe = random.choice(current_vibes)
    search_query = f"{u_genre} {u_vibe}"
    st.info(f"🎲 Random Vibe: {u_genre} + {u_vibe}")

if search_query:
    if not u_name:
        st.warning("Please enter your name first!")
    else:
        with st.spinner('Scanning Spotify Database...'):
            try:
                res = sp.search(q=search_query, limit=15, type='track')
                if res and res['tracks']['items']:
                    st.session_state.tracks = res['tracks']['items']
                else:
                    st.error("No matches found. Try another mix.")
            except:
                st.error("Spotify is overwhelmed. Wait 5s.")

# --- 6. RESULTS ---
if st.session_state.tracks:
    st.write(f"### {u_name}, here's your personalized soundscape:")
    for t in st.session_state.tracks:
        pop = t['popularity']
        st.markdown(f"""
        <div class="song-card">
            <img src="{t['album']['images'][0]['url']}" width="70" style="border-radius:12px;">
            <div style="flex-grow:1;">
                <div style="color:white; font-weight:bold; font-size:1.1rem;">{t['name']}</div>
                <div style="color:#1DB954; font-size:0.9rem;">{t['artists'][0]['name']}</div>
                <span class="pop-tag">🔥 {pop}% Popularity</span>
            </div>
            <a href="{t['external_urls']['spotify']}" target="_blank" style="text-decoration:none;">
                <div style="background:#1DB954; color:black; padding:10px 20px; border-radius:30px; font-weight:bold; font-size:0.8rem;">PLAY</div>
            </a>
        </div>
        """, unsafe_allow_html=True)
