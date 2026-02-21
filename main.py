<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Ultimate Music Hub</title>
    <style>
        :root {
            --primary-color: #1db954;
            --bg-dark: #121212;
            --card-bg: #1e1e1e;
            --text-main: #ffffff;
            --text-dim: #b3b3b3;
        }

        body {
            font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
            margin: 0;
            background-color: var(--bg-dark);
            color: var(--text-main);
            transition: all 0.3s ease;
        }

        /* בורר שפות בולט בצד */
        #lang-switcher {
            position: fixed;
            top: 30px;
            right: 30px;
            display: flex;
            flex-direction: column;
            gap: 12px;
            z-index: 1000;
        }

        .lang-btn {
            background: rgba(29, 185, 84, 0.2);
            color: white;
            border: 1px solid var(--primary-color);
            padding: 10px 18px;
            border-radius: 30px;
            cursor: pointer;
            font-weight: 600;
            backdrop-filter: blur(5px);
            transition: all 0.2s;
        }

        .lang-btn:hover, .lang-btn.active {
            background: var(--primary-color);
            box-shadow: 0 0 15px var(--primary-color);
        }

        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 60px 20px;
        }

        header {
            text-align: center;
            margin-bottom: 50px;
        }

        h1 { font-size: 3rem; margin-bottom: 10px; }
        .update-status { color: var(--primary-color); font-size: 0.9rem; margin-bottom: 20px; }

        /* מבנה הגריד */
        .section-wrapper { margin-bottom: 60px; }
        .genre-group { margin-bottom: 30px; }
        .genre-name {
            font-size: 1.5rem;
            border-left: 4px solid var(--primary-color);
            padding-left: 15px;
            margin-bottom: 20px;
            color: var(--text-main);
        }

        .artists-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
            gap: 20px;
        }

        .artist-card {
            background: var(--card-bg);
            padding: 20px;
            border-radius: 12px;
            text-align: center;
            border: 1px solid transparent;
            transition: all 0.3s;
        }

        .artist-card:hover {
            border-color: var(--primary-color);
            transform: translateY(-5px);
            background: #252525;
        }

        .artist-name { display: block; font-size: 1.1rem; font-weight: bold; margin-bottom: 5px; }
        .sub-type { color: var(--text-dim); font-size: 0.85rem; }

        /* התאמת RTL */
        body.rtl { direction: rtl; }
        body.rtl .genre-name { border-left: none; border-right: 4px solid var(--primary-color); padding-left: 0; padding-right: 15px; }
        body.rtl #lang-switcher { right: auto; left: 30px; }

        /* אנימציית טעינה לעדכון אוטומטי */
        .loading-bar {
            height: 3px;
            width: 0%;
            background: var(--primary-color);
            position: fixed;
            top: 0;
            left: 0;
            transition: width 0.5s;
        }
    </style>
</head>
<body class="ltr">

    <div class="loading-bar" id="loader"></div>

    <div id="lang-switcher">
        <button class="lang-btn active" id="btn-en" onclick="changeLang('en')">English</button>
        <button class="lang-btn" id="btn-he" onclick="changeLang('he')">עברית</button>
        <button class="lang-btn" id="btn-ru" onclick="changeLang('ru')">Русский</button>
        <button class="lang-btn" id="btn-ar" onclick="changeLang('ar')">العربية</button>
    </div>

    <div class="container">
        <header>
            <h1 id="ui-title">Music Explorer</h1>
            <div class="update-status" id="status">Syncing with global charts...</div>
        </header>

        <div id="content-area">
            </div>
    </div>

    <script>
        const library = {
            en: {
                label: "Global Hits",
                sections: [
                    { genre: "Rock & Grunge", artists: ["Nirvana", "Arctic Monkeys", "Led Zeppelin", "Radiohead"] },
                    { genre: "Pop & Synth", artists: ["Harry Styles", "Billie Eilish", "The Weeknd", "Olivia Rodrigo"] },
                    { genre: "Hip-Hop / Rap", artists: ["Kendrick Lamar", "Drake", "Eminem", "Travis Scott"] },
                    { genre: "Jazz & Blues", artists: ["Miles Davis", "B.B. King", "John Coltrane"] }
                ]
            },
            he: {
                label: "מוזיקה ישראלית",
                sections: [
                    { genre: "ים תיכוני", artists: ["אייל גולן", "פאר טסי", "עדן חסון", "אושר כהן"] },
                    { genre: "רוק ישראלי", artists: ["היהודים", "מוניקה סקס", "ברי סחרוף", "שלום חנוך"] },
                    { genre: "היפ הופ מקומי", artists: ["טונה", "רביד פלוטניק", "זיקיי", "ג'ימבו ג'יי"] },
                    { genre: "פופ ואינדי", artists: ["נועה קירל", "נגה ארז", "מרגי", "יסמין מועלם"] }
                ]
            },
            ru: {
                label: "Русская Музыка",
                sections: [
                    { genre: "Russian Rock", artists: ["Kino", "Bi-2", "DDT", "Splin"] },
                    { genre: "Modern Pop", artists: ["Zivert", "Little Big", "Niletto", "Morgenshtern"] },
                    { genre: "Chanson / Folk", artists: ["Mikhail Krug", "Lyube", "Pelageya"] }
                ]
            },
            ar: {
                label: "موسيقى عربية",
                sections: [
                    { genre: "Tarab & Classic", artists: ["Umm Kulthum", "Abdel Halim Hafez", "Fairuz"] },
                    { genre: "Arabic Pop", artists: ["Amr Diab", "Nancy Ajram", "Elissa", "Tamer Hosny"] },
                    { genre: "Alternative Arabic", artists: ["Mashrou' Leila", "Cairokee", "JadaL"] }
                ]
            }
        };

        let currentLang = 'en';

        function render() {
            const area = document.getElementById('content-area');
            const status = document.getElementById('status');
            area.innerHTML = '';
            
            // סדר הצגה: אנגלית -> עברית -> רוסית -> ערבית
            const order = ['en', 'he', 'ru', 'ar'];
            
            order.forEach(langKey => {
                const data = library[langKey];
                const sectionHtml = `
                    <div class="section-wrapper">
                        <h2 style="color: var(--primary-color); border-bottom: 1px solid #333; padding-bottom: 10px;">${data.label}</h2>
                        ${data.sections.map(sec => `
                            <div class="genre-group">
                                <h3 class="genre-name">${sec.genre}</h3>
                                <div class="artists-grid">
                                    ${sec.artists.map(name => `
                                        <div class="artist-card">
                                            <span class="artist-name">${name}</span>
                                            <span class="sub-type">${sec.genre} Artist</span>
                                        </div>
                                    `).join('')}
                                </div>
                            </div>
                        `).join('')}
                    </div>
                `;
                area.innerHTML += sectionHtml;
            });

            status.innerText = `Last updated: ${new Date().toLocaleTimeString()} (Auto-sync active)`;
        }

        function changeLang(lang) {
            currentLang = lang;
            document.body.className = (lang === 'he' || lang === 'ar') ? 'rtl' : 'ltr';
            
            // עדכון כפתורים
            document.querySelectorAll('.lang-btn').forEach(btn => btn.classList.remove('active'));
            document.getElementById(`btn-${lang}`).classList.add('active');

            // אפקט טעינה
            const loader = document.getElementById('loader');
            loader.style.width = '100%';
            setTimeout(() => {
                render();
                loader.style.width = '0%';
            }, 400);
        }

        // מנגנון עדכון אוטומטי (כל 30 שניות מדמה רענון נתונים)
        setInterval(() => {
            const loader = document.getElementById('loader');
            loader.style.width = '40%';
            setTimeout(() => {
                render();
                loader.style.width = '0%';
            }, 800);
        }, 30000);

        window.onload = render;
    </script>
</body>
</html>
