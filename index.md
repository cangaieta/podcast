---
layout: landing
title: "Podcast Associació Veïnal Can Gaietà"
description: "Podcast informatiu que ofereix una font d'informació alternativa sobre els esdeveniments de Tiana. Contingut generat amb IA basant-se en fonts oficials."
---

<header class="header">
    <nav class="nav">
        <a href="#" class="logo">🏘️ Can Gaietà</a>
        <ul class="nav-links">
            <li><a href="#about">Sobre el podcast</a></li>
            <li><a href="#disclaimer">Disclaimer</a></li>
            <li><a href="#subscribe">Subscriu-te</a></li>
            <li><a href="/episodis">Episodis</a></li>
        </ul>
    </nav>
</header>

<main>
    <!-- Hero Section -->
    <section class="hero">
        <div class="hero-content">
            <img src="{{ '/assets/logo-podcast.png' | relative_url }}" alt="Logo Podcast Can Gaietà" class="podcast-logo">
            <h1>Podcast Can Gaietà</h1>
            <p class="subtitle">Informació transparent sobre el que passa a Tiana</p>
            <p class="description">
                Una font d'informació alternativa sobre els esdeveniments del poble,
                discussions del ple de l'ajuntament i sessions del CAUT.
                Contingut generat amb IA basant-se en fonts oficials.
            </p>
            <div class="cta-buttons">
                <a href="#subscribe" class="btn btn-primary">
                    🎧 Escolta ara
                </a>
                <a href="#about" class="btn btn-secondary">
                    📖 Més informació
                </a>
            </div>
        </div>
    </section>

    <!-- About Section -->
    <section id="about" class="about fade-in">
        <div class="container">
            <h2 class="section-title">Què és aquest podcast?</h2>
            <div class="about-grid">
                <div class="about-card">
                    <div class="icon">🏛️</div>
                    <h3>Ple de l'Ajuntament</h3>
                    <p>Analitzem i comentem les decisions i discussions que es prenen en les sessions municipals de Tiana.</p>
                </div>
                <div class="about-card">
                    <div class="icon">🏗️</div>
                    <h3>Sessions del CAUT</h3>
                    <p>Seguiment del Consell Assessor Urbanístic de Tiana i els projectes que afecten el nostre veïnat.</p>
                </div>
                <div class="about-card">
                    <div class="icon">🤖</div>
                    <h3>Generat amb IA</h3>
                    <p>Utilitzem Google NotebookLM per crear contingut basat en fonts oficials i documentació real.</p>
                </div>
                <div class="about-card">
                    <div class="icon">📚</div>
                    <h3>Fonts Transparents</h3>
                    <p>Sempre proporcionem les fonts originals perquè puguis consultar la informació directament.</p>
                </div>
                <div class="about-card">
                    <div class="icon">⏱️</div>
                    <h3>Episodis Curts</h3>
                    <p>Programes de ~10 minuts, perfectes per mantenir-te informat sense perdre temps.</p>
                </div>
                <div class="about-card">
                    <div class="icon">🎙️</div>
                    <h3>Accessible a Tothom</h3>
                    <p>Pots usar tu mateix Google NotebookLM. És gratuït amb qualsevol compte de Google!</p>
                </div>
            </div>
        </div>
    </section>

    <!-- Disclaimer Section -->
    <section id="disclaimer" class="disclaimer fade-in">
        <div class="disclaimer-content">
            <h2>⚠️ Disclaimer Important</h2>
            <p>
                Tot el contingut d'aquest podcast (guions i audio) està creat amb
                <span class="highlight">Google NotebookLM</span>,
                una eina d'intel·ligència artificial.
            </p>
            <p>
                Encara que el contingut es basa en <strong>fonts oficials reals</strong>,
                pot contenir interpretacions o matisos de la IA que no encaixin completament amb la realitat.
            </p>
            <p>
                <strong>Sempre proporcionem les fonts de dades originals</strong>
                perquè puguis consultar la informació directament i formar-te la teva pròpia opinió.
            </p>
        </div>
    </section>

    <!-- Subscribe Section -->
    <section id="subscribe" class="subscribe fade-in">
        <div class="container">
            <h2>Subscriu-te al Podcast</h2>
            <p>Mantén-te informat dels últims esdeveniments de Can Gaietà i Tiana</p>

            <div class="subscribe-options">
                <a href="{{ '/feed.xml' | relative_url }}" class="subscribe-btn">
                    📡 RSS Feed
                </a>
                <a href="https://github.com/cangaieta/podcast" target="_blank" class="subscribe-btn">
                    💻 GitHub
                </a>
                <button onclick="copyRSS()" class="subscribe-btn">
                    📋 Copiar URL RSS
                </button>
            </div>

            <div class="rss-info">
                <h3>Per subscriure't des de la teva app de podcasts:</h3>
                <p>Copia aquesta URL i afegeix-la a la teva aplicació de podcasts favorita:</p>
                <div class="rss-url">{{ site.url }}{{ site.baseurl }}/feed.xml</div>
                <p><em>Compatible amb Apple Podcasts, Spotify, Google Podcasts, i totes les apps de podcasts principals.</em></p>
            </div>
        </div>
    </section>
</main>

<!-- Footer -->
<footer class="footer">
    <div class="container">
        <div class="footer-links">
            <a href="#about">Sobre nosaltres</a>
            <a href="#disclaimer">Disclaimer</a>
            <a href="https://cangaieta.cat" target="_blank">Web oficial AV Can Gaietà</a>
            <a href="{{ '/feed.xml' | relative_url }}">RSS</a>
            <a href="https://github.com/cangaieta/podcast">GitHub</a>
            <a href="https://notebooklm.google" target="_blank">Google NotebookLM</a>
        </div>
        <p>&copy; {{ 'now' | date: '%Y' }} Associació Veïnal de Can Gaietà - Tiana</p>
        <p><small>Contingut generat amb IA • Fonts sempre transparents</small></p>
    </div>
</footer>