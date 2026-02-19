import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from datetime import datetime

# פונקציה לטעינת המפתחות בצורה בטוחה
def get_spotify_conn():
    try:
        # הקוד בודק את ה-Secrets שלך
        cid = st.secrets.get("CLIENT_ID") or st.secrets.get("client_id")
        csec = st.secrets.get("CLIENT_SECRET") or st.secrets.get("client_secret")
        
        if not cid or not csec:
            return None
            
        auth_manager = SpotifyClientCredentials(client_id=cid.strip(), client_secret=csec.strip())
        return spotipy.Spotify(auth_manager=auth_manager)
    except:
        return None

sp = get_spotify_conn()

st.title("⚡ Music Time Machine")

if sp is None:
    st.error("Missing Credentials! Please check your Streamlit Secrets.")
    st.info("וודא שב-Secrets רשום CLIENT_ID ו-CLIENT_SECRET באותיות גדולות.")
    st.stop()

# כאן המשך הקוד של האפליקציה...
user_name = st.text_input("הכנס שם")
dob = st.date_input("תאריך לידה", min_value=datetime(1950, 1, 1))
genre = st.selectbox("ז'אנר", ['Pop', 'Rock', 'Hip Hop', 'Jazz'])

if st.button("Generate ✨"):
    st.write(f"היי {user_name}, מיד נבנה לך פסקול ל-{dob}!")
    # כאן תבוא פונקציית החיפוש שלך
