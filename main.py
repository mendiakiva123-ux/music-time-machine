import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from datetime import datetime

# עיצוב בסיסי ונקי
st.set_page_config(page_title="My Music Journey", layout="centered")

# פונקציית חיבור לספוטיפיי - מנקה רווחים אוטומטית
def get_sp_connection():
    try:
        cid = st.secrets["CLIENT_ID"].strip()
        csec = st.secrets["CLIENT_SECRET"].strip()
        auth_manager = SpotifyClientCredentials(client_id=cid, client_secret=csec)
        return spotipy.Spotify(auth_manager=auth_manager)
    except Exception as e:
        st.error(f"שגיאה בחיבור: וודא שהמפתחות ב-Secrets תקינים.")
        return None

sp = get_sp_connection()

st.title("🎵 הפסקול של החיים שלי")
st.write("הכנס פרטים וקבל את השירים שליוו אותך לאורך השנים!")

# קלט מהמשתמש
col1, col2 = st.columns(2)
with col1:
    name = st.text_input("שם:", value="מנדי")
with col2:
    birth_year = st.number_input("שנת לידה:", min_value=1950, max_value=2025, value=2004)

genre = st.selectbox("בחר סגנון מוזיקלי:", ["Pop", "Rock", "Hip Hop", "Dance"])

if st.button("הצג את הפסקול שלי! ✨"):
    if sp:
        st.balloons()
        st.subheader(f"👋 היי {name}, הנה המוזיקה שלך:")
        
        current_year = datetime.now().year
        # נבדוק שנים נבחרות כדי שיהיה מהיר ולא ייתקע
        years_to_check = [birth_year, birth_year+5, birth_year+10, birth_year+15, current_year]
        
        for year in years_to_check:
            if year > current_year: continue
            
            # חיפוש פשוט מאוד
            query = f"year:{year} genre:{genre}"
            results = sp.search(q=query, limit=1, type='track')
            
            if results['tracks']['items']:
                track = results['tracks']['items'][0]
                age = year - birth_year
                
                # הצגת התוצאה בתיבה נעימה
                with st.expander(f"📅 שנת {year} (גיל {age})"):
                    st.write(f"**שיר:** {track['name']}")
                    st.write(f"**אמן:** {track['artists'][0]['name']}")
                    st.image(track['album']['images'][0]['url'], width=150)
                    if track['preview_url']:
                        st.audio(track['preview_url'])
                    st.markdown(f"[האזן בספוטיפיי]({track['external_urls']['spotify']})")
            else:
                st.write(f"לא מצאתי שיר לשנת {year}")
    else:
        st.warning("המערכת לא מחוברת לספוטיפיי. בדוק את הגדרות ה-Secrets.")
