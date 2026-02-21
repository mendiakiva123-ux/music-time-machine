<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>VibeLab - Global AI Music Curator</title>
    <style>
        :root {
            --spotify-green: #1db954;
            --bg-black: #0a0a0a;
            --card-bg: #181818;
            --text-white: #ffffff;
            --text-gray: #a7a7a7;
        }

        /* עיצוב כללי נקי - ללא המלבן למעלה */
        body {
            font-family: 'Circular Sp', Helvetica, Arial, sans-serif;
            background-color: var(--bg-black);
            color: var(--text-white);
            margin: 0;
            padding: 0;
            transition: direction 0.3s ease;
        }

        /* בורר שפות בולט בצד - UX משופר */
        #language-control {
            position: fixed;
            top: 25px;
            right: 25px;
            display: flex;
            flex-direction: column;
            gap: 12px;
            z-index: 9999;
        }

        .lang-btn {
            background: rgba(255, 255, 255, 0.1);
            color: white;
            border: 1px solid rgba(255, 255, 255, 0.3);
            padding: 10px 20px;
            border-radius: 4px;
            cursor: pointer;
            font-size: 14px;
            font-weight: bold;
            text-transform: uppercase;
            transition: 0.3s;
            min-width: 120px;
        }

        .lang-btn:hover, .lang-btn.active {
            background: var(--spotify-green);
            border-color: var(--spotify-green);
            box-shadow: 0 0 15px rgba(29, 185, 84, 0.4);
        }

        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 40px 20px;
        }

        h1 { font-size: 3.5rem; text-align: center; margin-bottom: 10px; letter-spacing: -2px; }
        .subtitle { text-align: center; color: var(--text-gray); margin-bottom: 40px; }

        /* סננים (Filters) */
        .filter-bar {
            display: flex;
            justify-content: center;
            gap: 15px;
            margin-bottom: 50px;
        }

        .filter-select {
            background: #282828;
            color: white;
            border: none;
            padding: 12px 20px;
            border-radius: 5px;
            font-size: 16px;
            cursor: pointer;
        }

        /* מבנה התוכן */
        .language-block { margin-bottom: 80px; }
        .lang-header {
            font-size: 2rem;
            border-bottom: 1px solid #333;
            padding-bottom: 15px;
            margin-bottom: 30px;
            color: var(--spotify-green);
        }

        .genre-section { margin-bottom: 40px; }
        .genre-title { font-size: 1.4rem; margin-bottom: 20px; color: #eee; }

        .artists-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
            gap: 20px;
        }

        .artist-card {
            background: var(--card-bg);
            padding: 20px;
            border-radius: 8px;
            text-align: center;
            transition: 0.3s;
            cursor: pointer;
            position: relative;
            overflow: hidden;
        }

        .artist-card:hover { background: #282828; transform: translateY(-5px); }
        .artist-card::after {
            content: '▶';
            position: absolute;
            bottom: 10px;
            right: 10px;
            color: var(--spotify-green);
            opacity: 0;
            transition: 0.3s;
        }
        .artist-card:hover::after { opacity: 1; }

        .artist-name { display: block; font-weight: bold; margin-bottom: 8px; }
        .artist-tag { font-size: 0.8rem; color: var(--text-gray); text-transform: uppercase; }

        /* RTL Adjustments */
        body.rtl { direction: rtl; }
        body.rtl #language-control { right: auto; left: 25px; }
    </style>
</head>
<body class="ltr">

    <div id="language-control">
        <button class="lang-btn active" id="btn-en" onclick="updateView('en')">English</button>
        <button class="lang-btn" id="btn-he" onclick="updateView('he')">Hebrew / עברית</button>
        <button class="lang-btn" id="btn-ru" onclick="updateView('ru')">Russian / Русский</button>
        <button class="lang-btn" id="btn-ar" onclick="updateView('ar')">Arabic / العربية</button>
    </div>

    <div class="container">
        <h1>VIBELAB</h1>
        <p class="subtitle">The Global AI Music Curator</p>

        <div class="filter-bar">
            <select id="genre-filter" class="filter-select" onchange="renderContent()">
                <option value="all">All Genres (No Filter)</option>
                <option value="Pop">Pop</option>
                <option value="Rock">Rock</option>
                <option value="Hip-Hop">Hip-Hop</option>
                <option value="Classic">Classic/Traditional</option>
            </select>
        </div>

        <div id="main-content"></div>
    </div>

    <script>
        const musicData = {
            en: {
                label: "English Music",
                genres: {
                    "Pop": ["Taylor Swift", "The Weeknd", "Dua Lipa", "Harry Styles", "Ariana Grande"],
                    "Rock": ["Linkin Park", "Arctic Monkeys", "Queen", "Nirvana", "Red Hot Chili Peppers"],
                    "Hip-Hop": ["Kendrick Lamar", "Drake", "Eminem", "Travis Scott", "J. Cole"]
                }
            },
            he: {
                label: "מוזיקה ישראלית",
                genres: {
                    "Pop": ["נועה קירל", "מרגי", "אנה זק", "סטטיק", "רן דנקר"],
                    "Rock": ["ברי סחרוף", "היהודים", "מוניקה סקס", "תיסלם", "שלום חנוך"],
                    "Classic": ["אייל גולן", "זוהר ארגוב", "ישי ריבו", "פאר טסי", "חנן בן ארי"]
                }
            },
            ru: {
                label: "Русская Музыка",
                genres: {
                    "Pop": ["Zivert", "Polina Gagarina", "Jony", "Niletto", "Artik & Asti"],
                    "Rock": ["Kino", "Bi-2", "Splin", "Mumiy Troll", "Korol i Shut"],
                    "Hip-Hop": ["Oxxxymiron", "Scriptonite", "Miyagi", "Basta", "Morgenshtern"]
                }
            },
            ar: {
                label: "موسيقى عربية",
                genres: {
                    "Pop": ["Amr Diab", "Nancy Ajram", "Elissa", "Tamer Hosny", "Mohamed Hamaki"],
                    "Classic": ["Umm Kulthum", "Fairuz", "Abdel Halim", "Warda", "George Wassouf"],
                    "Hip-Hop": ["Wegz", "Marwan Pablo", "Toto", "Balti", "Afroto"]
                }
            }
        };

        let currentLang = 'en';

        function updateView(lang) {
            currentLang = lang;
            document.body.className = (lang === 'he' || lang === 'ar') ? 'rtl' : 'ltr';
            
            document.querySelectorAll('.lang-btn').forEach(b => b.classList.remove('active'));
            document.getElementById(`btn-${lang}`).classList.add('active');
            
            renderContent();
        }

        function renderContent() {
            const container = document.getElementById('main-content');
            const genreFilter = document.getElementById('genre-filter').value;
            container.innerHTML = '';

            // סדר: אנגלית -> עברית -> רוסית -> ערבית
            const order = ['en', 'he', 'ru', 'ar'];

            order.forEach(lang => {
                const data = musicData[lang];
                let langHtml = `<div class="language-block"><h2 class="lang-header">${data.label}</h2>`;
                let hasContent = false;

                for (const [genre, artists] of Object.entries(data.genres)) {
                    if (genreFilter === 'all' || genre === genreFilter) {
                        hasContent = true;
                        langHtml += `
                            <div class="genre-section">
                                <h3 class="genre-title">${genre}</h3>
                                <div class="artists-grid">
                                    ${artists.map(a => `
                                        <div class="artist-card">
                                            <span class="artist-name">${a}</span>
                                            <span class="artist-tag">${genre}</span>
                                        </div>
                                    `).join('')}
                                </div>
                            </div>`;
                    }
                }
                langHtml += `</div>`;
                if (hasContent) container.innerHTML += langHtml;
            });
        }

        // טעינה ראשונית
        window.onload = renderContent;
    </script>
</body>
</html>
