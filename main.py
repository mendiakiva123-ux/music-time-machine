import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import random

# --- 1. CONFIG ---
st.set_page_config(page_title="VibeLab PRO", page_icon="🔥", layout="centered")

if 'lang' not in st.session_state: st.session_state.lang = 'HE'
if 'tracks' not in st.session_state: st.session_state.tracks = []

# --- 2. ELITE CSS (PREMIUM DESIGN) ---
st.markdown(r"""
<style>
    .stApp { 
        background: linear-gradient(135deg, #0e1117 0%, #050505 100%);
        color: white; 
    }
    .main-title { 
        background: linear-gradient(90deg, #1DB954, #1ed760);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 65px; font-weight: 900; text-align: center; margin-bottom: 0px;
    }
    .stButton>button { 
        background: linear-gradient(45deg, #1DB954, #19a34a) !important; 
        color: white !important; font-weight: bold; border-radius: 30px; 
        height: 50px; width: 100%; border: none; transition: 0.3s;
    }
    .stButton>button:hover { transform: translateY(-2px); box-shadow: 0 5px 15px rgba(29,185,84,0.4); }
    .song-box { 
        background: rgba(255,255,255,0.03); padding: 20px; border-radius: 20px; 
        margin-bottom: 12px; border: 1px solid rgba(255,255,255,0.05);
        display: flex; align-items: center; gap: 15px; transition: 0.3s;
    }
    .song-box:hover { background: rgba(255,255,255,0.07); transform: scale(1.01); }
    .popularity-tag { 
        background: #1DB954; color: black; padding: 2px 8px; 
        border-radius: 10px; font-size: 10px; font-weight: bold; 
    }
    label { color: #1DB954 !important; font-weight: bold !important; }
</style>
""", unsafe_allow_html=True)

# --- 3. DATA ENGINE ---
DATA = {
    'EN': {
        'title': 'VIBELAB PRO', 'sub': 'Premium AI Music Experience',
        'name': 'Your Name', 'gen': 'Genre', 'vib': 'Vibe', 'btn': 'GENERATE VIBE ⚡',
        'genres': ["Pop", "Hip Hop", "Techno", "Rock", "Latin Hits", "Jazz", "80s Retro"],
        'vibes': ["Party Mode", "Chill & Relax", "Gym Energy", "Deep Focus", "Night Drive"],
        'dl': "📥 Download List"
    },
    'HE': {
        'title': 'VIBELAB PRO', 'sub': 'חווית מוזיקה בסטנדרט גבוה',
        'name': 'איך קוראים לך?', 'gen': 'סגנון מוזיקלי', 'vib': 'מה הוייב?', 'btn': 'צור פלייליסט ⚡',
        'genres': ["מזרחית", "ישראלי", "פופ", "היפ הופ", "אלקטרוני", "חסידי", "רוק", "נוסטלגיה"],
        'vibes': ["מסיבה", "רגוע", "כושר", "ריכוז", "נסיעת לילה"],
        'dl': "📥 הורד רשימת שירים"
    }
}

# --- 4. SPOTIFY ---
@st.cache_resource
def get_sp():
    try:
        return spotipy.Spotify(auth_manager=SpotifyClientCredentials(
            client_id=st.secrets["CLIENT_ID"].strip(),
            client_secret=st.secrets["CLIENT_SECRET"].strip()
        ))
    except: return None

sp = get_sp()

# --- 5. UI ---
c_lang = st.columns([5, 1, 1])
if c_lang[1].button("EN"): 
    st.session_state.lang = 'EN'
    st.rerun()
if c_lang[2].button("HE"): 
    st.session_state.lang = 'HE'
    st.rerun()

L = DATA[st.session_state.lang]

st.markdown(f'<h1 class="main-title">{L["title"]}</h1>', unsafe_allow_html=True)
st.write(f"<p style='text-align:center; color:gray; margin-top:-10px;'>{L['sub']}</p>", unsafe_allow_html=True)

u_name = st.text_input(L['name'], placeholder="...")

col1, col2 = st.columns(2)
with col1:
    u_genre = st.selectbox(L['gen'], L['genres'])
with col2:
    u_vibe = st.selectbox(L['vib'], L['vibes'])

# כפתורי פעולה
btn_col, surp_col = st.columns([4, 1])
do_search = btn_col.button(L['btn'])
do_surprise = surp_col.button("🎲")

search_query = None
if do_search:
    search_query = f"{u_genre} {u_vibe} hits"
elif do_surprise:
    u_genre = random.choice(L['genres'])
    u_vibe = random.choice(L['vibes'])
    search_query = f"{u_genre} {u_vibe} hits"
    st.toast(f"🎲 Random Mix: {u_genre} + {u_vibe}")

if search_query:
    if not u_name:
        st.warning("Please enter your name")
    elif not sp:
        st.error("Spotify Connection Failed")
    else:
        with st.spinner('Curating your experience...'):
            try:
                res = sp.search(q=search_query, limit=12, type='track')
                if res and res['tracks']['items']:
                    st.session_state.tracks = res['tracks']['items']
                    st.balloons()
                else:
                    st.warning("No results found.")
            except:
                st.error("Spotify is busy. Wait 5s.")

# --- 6. RESULTS ---
if st.session_state.tracks:
    st.write(f"### {u_name}, here is your {u_vibe} mix:")
    
    # כפתור הורדה
    list_text = "\n".join([f"{t['name']} - {t['artists'][0]['name']}" for t in st.session_state.tracks])
    st.download_button(L['dl'], list_text, file_name="my_vibe_list.txt")

    for t in st.session_state.tracks:
        pop = t['popularity']
        st.markdown(f"""
        <div class="song-box">
            <img src="{t['album']['images'][0]['url']}" width="65" style="border-radius:12px;">
            <div style="flex-grow:1;">
                <div style="color:white; font-weight:bold; font-size:16px;">{t['name']}</div>
                <div style="color:#1DB954; font-size:13px; margin-bottom:5px;">{t['artists'][0]['name']}</div>
                <span class="popularity-tag">🔥 {pop}% Popular</span>
            </div>
            <a href="{t['external_urls']['spotify']}" target="_blank" 
               style="background:#1DB954; color:black; padding:8px 18px; border-radius:20px; text-decoration:none; font-weight:bold; font-size:12px;">
               PLAY
            </a>
        </div>
        """, unsafe_allow_html=True)
