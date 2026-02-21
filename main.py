<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>VibeLab | Professional Music Library</title>
    <style>
        :root {
            --accent: #1db954;
            --bg: #0d0d0d;
            --surface: #1a1a1a;
        }

        body {
            font-family: 'Inter', -apple-system, sans-serif;
            background-color: var(--bg);
            color: white;
            margin: 0;
            line-height: 1.6;
        }

        /* סרגל שפות מהיר וקומפקטי בצד */
        #lang-nav {
            position: fixed;
            top: 20px;
            right: 20px;
            display: flex;
            flex-direction: column;
            gap: 8px;
            z-index: 1000;
        }

        .nav-link {
            background: var(--surface);
            color: white;
            border: 1px solid #333;
            padding: 8px 16px;
            border-radius: 4px;
            cursor: pointer;
            font-size: 12px;
            font-weight: 600;
            text-align: center;
            transition: 0.2s;
        }

        .nav-link:hover, .nav-link.active {
            background: var(--accent);
            border-color: var(--accent);
        }

        .main-container {
            max-width: 1100px;
            margin: 0 auto;
            padding: 60px 20px;
        }

        header { text-align: center; margin-bottom: 60px; }
        h1 { font-size: 4rem; font-weight: 900; margin: 0; letter-spacing: -3px; }
        .tagline { color: var(--accent); font-weight: 600; text-transform: uppercase; letter-spacing: 2px; }

        /* מערכת סינון ז'אנרים מהירה */
        .master-filter {
            display: flex;
            justify-content: center;
            margin-bottom: 50px;
            gap: 10px;
        }

        .filter-btn {
            background: #222;
            border: none;
            color: #aaa;
            padding: 10px 20px;
            border-radius: 20px;
            cursor: pointer;
            transition: 0.3s;
        }

        .filter-btn.active {
            background: white;
            color: black;
        }

        /* תצוגת תוכן */
        .lang-section { margin-bottom: 100px; scroll-margin-top: 100px; }
        .lang-title { font-size: 1.8rem; margin-bottom: 30px; border-bottom: 2px solid #222; padding-bottom: 10px; }

        .genre-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
            gap: 30px;
        }

        .genre-card {
            background: var(--surface);
            padding: 25px;
            border-radius: 12px;
            transition: 0.3s;
        }

        .genre-card:hover { transform: translateY(-5px); background: #252525; }
        
        .genre-label { color: var(--accent); font-size: 0.8rem; font-weight: bold; margin-bottom: 10px; display: block; }
        .artist-list { list-style: none; padding: 0; margin: 0; }
        .artist-list li { margin-bottom: 6px; font-weight: 500; opacity: 0.9; }

        /* RTL Support */
        body.rtl { direction: rtl; }
        body.rtl #lang-nav { right: auto; left: 20px; }
    </style>
</head>
<body class="ltr">

    <nav id="lang-nav">
        <button class="nav-link active" onclick="setLang('en')">US ENGLISH</button>
        <button class="nav-link" onclick="setLang('he')">IL עברית</button>
        <button class="nav-link" onclick="setLang('ru')">RU RUSSIAN</button>
        <button class="nav-link" onclick="setLang('ar')">SA ARABIC</button>
    </nav>

    <div class="main-container">
        <header>
            <div class="tagline">Global AI Music Curator</div>
            <h1>VIBELAB</h1>
        </header>

        <div class="master-filter">
            <button class="filter-btn active" onclick="filterGenre('all')">Show All</button>
            <button class="filter-btn" onclick="filterGenre('Pop')">Pop</button>
            <button class="filter-btn" onclick="filterGenre('Rock')">Rock</button>
            <button class="filter-btn" onclick="filterGenre('Hip-Hop')">Hip-Hop</button>
            <button class="filter-btn" onclick="filterGenre('Classic')">Traditional</button>
        </div>

        <div id="catalog"></div>
    </div>

    <script>
        const data = {
            en: {
                label: "English Library",
                content: [
                    { genre: "Pop", artists: ["Taylor Swift", "The Weeknd", "Dua Lipa", "Harry Styles", "Ariana Grande"] },
                    { genre: "Rock", artists: ["Linkin Park", "Arctic Monkeys", "Queen", "Nirvana", "The Killers"] },
                    { genre: "Hip-Hop", artists: ["Kendrick Lamar", "Drake", "Eminem", "Travis Scott", "J. Cole"] }
                ]
            },
            he: {
                label: "ספרייה עברית",
                content: [
                    { genre: "Classic", artists: ["אייל גולן", "זוהר ארגוב", "ישי ריבו", "פאר טסי", "חנן בן ארי"] },
                    { genre: "Pop", artists: ["נועה קירל", "מרגי", "אנה זק", "סטטיק", "רן דנקר"] },
                    { genre: "Rock", artists: ["ברי סחרוף", "היהודים", "מוניקה סקס", "תיסלם", "שלום חנוך"] },
                    { genre: "Hip-Hop", artists: ["טונה", "רביד פלוטניק", "נורוז", "זיקיי", "ג'ימבו ג'יי"] }
                ]
            },
            ru: {
                label: "Русская библиотека",
                content: [
                    { genre: "Pop", artists: ["Zivert", "Polina Gagarina", "Jony", "Niletto", "Artik & Asti"] },
                    { genre: "Rock", artists: ["Kino", "Bi-2", "Splin", "Mumiy Troll", "DDT"] },
                    { genre: "Hip-Hop", artists: ["Oxxxymiron", "Scriptonite", "Miyagi", "Basta", "Noize MC"] }
                ]
            },
            ar: {
                label: "المكتبة العربية",
                content: [
                    { genre: "Classic", artists: ["Umm Kulthum", "Fairuz", "Abdel Halim Hafez", "Warda", "George Wassouf"] },
                    { genre: "Pop", artists: ["Amr Diab", "Nancy Ajram", "Elissa", "Tamer Hosny", "Mohamed Hamaki"] },
                    { genre: "Hip-Hop", artists: ["Wegz", "Marwan Pablo", "Toto", "Balti", "Afroto"] }
                ]
            }
        };

        let activeGenre = 'all';

        function setLang(lang) {
            document.body.className = (lang === 'he' || lang === 'ar') ? 'rtl' : 'ltr';
            document.querySelectorAll('.nav-link').forEach(b => b.classList.remove('active'));
            event.target.classList.add('active');
            render();
            // Scroll to the selected language section
            window.scrollTo({ top: 0, behavior: 'smooth' });
        }

        function filterGenre(genre) {
            activeGenre = genre;
            document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
            event.target.classList.add('active');
            render();
        }

        function render() {
            const catalog = document.getElementById('catalog');
            catalog.innerHTML = '';

            const order = ['en', 'he', 'ru', 'ar'];
            
            order.forEach(key => {
                const section = data[key];
                let sectionHtml = `
                    <div class="lang-section">
                        <h2 class="lang-title">${section.label}</h2>
                        <div class="genre-grid">
                `;

                let count = 0;
                section.content.forEach(item => {
                    if (activeGenre === 'all' || item.genre === activeGenre) {
                        count++;
                        sectionHtml += `
                            <div class="genre-card">
                                <span class="genre-label">${item.genre}</span>
                                <ul class="artist-list">
                                    ${item.artists.map(a => `<li>${a}</li>`).join('')}
                                </ul>
                            </div>
                        `;
                    }
                });

                sectionHtml += `</div></div>`;
                if (count > 0) catalog.innerHTML += sectionHtml;
            });
        }

        window.onload = render;
    </script>
</body>
</html>
