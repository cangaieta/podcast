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
            <li><a href="{{ '/episodis' | relative_url }}">Episodis</a></li>
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
                Una eina per fomentar l'esperit crític sobre els esdeveniments del poble.
                Analitzem discussions del ple i sessions del CAUT des de diferents perspectives.
                Contingut 100% generat amb IA - busca la veritat per tu mateix.
            </p>
            <div class="cta-buttons">
                <button onclick="openPodcast()" class="btn btn-primary">
                    🎧 Escolta ara
                </button>
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
                    <h3>100% Generat amb IA</h3>
                    <p>NotebookLM, Whisper i Claude creen contingut per fomentar el debat crític. No som una font de veritat absolute.</p>
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
            <h2>⚠️ Esperit Crític i Transparència</h2>
            <p>
                Aquest podcast està <strong>completament generat amb intel·ligència artificial</strong> utilitzant
                <span class="highlight">Google NotebookLM</span>, <span class="highlight">Whisper</span> i <span class="highlight">Claude</span>.
            </p>
            <p>
                <strong>El nostre objectiu NO és "informar dels fets tal com són"</strong>,
                sinó <strong>fomentar l'esperit crític</strong> presentant diferents perspectives i conceptes
                sobre els esdeveniments locals.
            </p>
            <p>
                <strong>Et convidem a buscar la veritat per tu mateix.</strong>
                Sempre proporcionem les fonts originals perquè puguis:
            </p>
            <ul>
                <li>✅ Contrastar la informació directament</li>
                <li>✅ Formar-te la teva pròpia opinió</li>
                <li>✅ Qüestionar tant el nostre contingut com les fonts oficials</li>
                <li>✅ Participar activament en el debat públic</li>
            </ul>
            <p>
                <strong>Recorda:</strong> La IA pot contenir interpretacions, biaixos o errors.
                El pensament crític i la verificació independent són sempre essencials.
            </p>
        </div>
    </section>

    <!-- Subscribe Section -->
    <section id="subscribe" class="subscribe fade-in">
        <div class="container">
            <h2>Subscriu-te al Podcast</h2>
            <p>Mantén-te informat dels últims esdeveniments de Can Gaietà i Tiana</p>

            <!-- 1. Subscripció Universal -->
            <div class="universal-subscription">
                <h3>🌐 Subscripció Universal</h3>
                <div class="universal-link-section">
                    <a href="https://www.subscribeonandroid.com/cangaieta.github.io/podcast/feed.xml"
                       target="_blank"
                       rel="noopener"
                       class="universal-subscribe-link">
                        <div class="universal-subscribe-card">
                            <div class="universal-icon">📱</div>
                            <div class="universal-content">
                                <h4>Subscribe on Android</h4>
                                <p>Detecta automàticament les teves apps de podcasts i t'ajuda a subscriure't</p>
                            </div>
                            <div class="universal-arrow">→</div>
                        </div>
                    </a>
                </div>
            </div>

            <!-- 2. Subscripció Manual -->
            <div class="manual-subscription">
                <h3>📋 Subscripció Manual</h3>
                <div class="manual-content">
                    <div class="rss-copy-section">
                        <label for="rss-input">URL del Feed RSS:</label>
                        <div class="rss-input-group">
                            <input type="text" id="rss-input" value="{{ site.url }}{{ site.baseurl }}/feed.xml" readonly>
                            <button onclick="copyRSSNoAlert()" class="copy-btn">📋 Copiar</button>
                        </div>
                    </div>

                    <div class="manual-steps">
                        <div class="step-item">
                            <div class="step-number">1</div>
                            <div class="step-text">
                                <strong>Copia l'URL del feed RSS</strong> utilitzant el botó de dalt
                            </div>
                        </div>
                        <div class="step-item">
                            <div class="step-number">2</div>
                            <div class="step-text">
                                <strong>Obre la teva app de podcasts</strong> favorita (Apple Podcasts, AntennaPod, Pocket Casts...)
                            </div>
                        </div>
                        <div class="step-item">
                            <div class="step-number">3</div>
                            <div class="step-text">
                                <strong>Busca l'opció "Afegir per URL"</strong> normalment a la secció de subscripcions
                            </div>
                        </div>
                        <div class="step-item">
                            <div class="step-number">4</div>
                            <div class="step-text">
                                <strong>Enganxa l'URL i subscriu-te</strong> - ja rebràs els nous episodis automàticament
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- 3. Instruccions per Plataforma -->
            <div class="platform-instructions">
                <h3>🔧 Instruccions per Plataforma</h3>
                <div class="platform-grid">
                    <details class="platform-detail">
                        <summary><strong>🍎 Apple Podcasts</strong></summary>
                        <div class="platform-content">
                            <div class="platform-variant">
                                <strong>iPhone/iPad:</strong>
                                <ol>
                                    <li>Obre Apple Podcasts</li>
                                    <li>Toca "Biblioteca" (baix de la pantalla)</li>
                                    <li>Toca "Editar" (dalt dreta)</li>
                                    <li>Toca "Afegir un programa per URL"</li>
                                    <li>Enganxa l'URL i toca "Subscriure's"</li>
                                </ol>
                            </div>
                            <div class="platform-variant">
                                <strong>Mac:</strong>
                                <ol>
                                    <li>Obre Apple Podcasts</li>
                                    <li>Ves a "Biblioteca"</li>
                                    <li>Menú "Fitxer" → "Subscriure a podcast"</li>
                                    <li>Enganxa l'URL i confirma</li>
                                </ol>
                            </div>
                        </div>
                    </details>

                    <details class="platform-detail">
                        <summary><strong>🤖 AntennaPod</strong></summary>
                        <div class="platform-content">
                            <p class="platform-note">Android només</p>
                            <ol>
                                <li>Obre AntennaPod</li>
                                <li>Toca "Add Podcast" (botó +)</li>
                                <li>Selecciona "By RSS address"</li>
                                <li>Enganxa l'URL del feed</li>
                                <li>Toca "Confirm"</li>
                            </ol>
                        </div>
                    </details>

                    <details class="platform-detail">
                        <summary><strong>🟤 Pocket Casts</strong></summary>
                        <div class="platform-content">
                            <ol>
                                <li>Obre Pocket Casts</li>
                                <li>Toca "Podcasts" (menú inferior)</li>
                                <li>Toca el botó "+" (dalt dreta)</li>
                                <li>Selecciona "Add podcast by URL"</li>
                                <li>Enganxa l'URL i confirma</li>
                            </ol>
                        </div>
                    </details>

                    <details class="platform-detail">
                        <summary><strong>☁️ Overcast</strong></summary>
                        <div class="platform-content">
                            <p class="platform-note">iOS només</p>
                            <ol>
                                <li>Obre Overcast</li>
                                <li>Toca el botó "+" (dalt dreta)</li>
                                <li>Selecciona "Add URL"</li>
                                <li>Enganxa l'URL del feed</li>
                            </ol>
                        </div>
                    </details>

                    <details class="platform-detail">
                        <summary><strong>📻 Castro</strong></summary>
                        <div class="platform-content">
                            <p class="platform-note">iOS només</p>
                            <ol>
                                <li>Obre Castro</li>
                                <li>Toca la lupa (Cercar)</li>
                                <li>Toca "Add from URL" (dalt dreta)</li>
                                <li>Enganxa l'URL del feed</li>
                                <li>Toca "Subscribe"</li>
                            </ol>
                        </div>
                    </details>

                    <details class="platform-detail">
                        <summary><strong>📻 Podcast Addict</strong></summary>
                        <div class="platform-content">
                            <p class="platform-note">Android només</p>
                            <ol>
                                <li>Obre Podcast Addict</li>
                                <li>Toca el menú (☰)</li>
                                <li>Selecciona "Add Podcast"</li>
                                <li>Toca "Add Podcast by URL"</li>
                                <li>Enganxa l'URL del feed</li>
                            </ol>
                        </div>
                    </details>

                    <details class="platform-detail">
                        <summary><strong>🎵 Player FM</strong></summary>
                        <div class="platform-content">
                            <ol>
                                <li>Obre Player FM</li>
                                <li>Toca "Discover" i després la lupa</li>
                                <li>Toca "Add custom RSS URL"</li>
                                <li>Enganxa l'URL del feed</li>
                            </ol>
                        </div>
                    </details>

                    <details class="platform-detail">
                        <summary><strong>🟣 Spotify</strong></summary>
                        <div class="platform-content">
                            <p class="platform-warning">⚠️ Spotify no suporta feeds RSS externs directament.</p>
                            <p><strong>Alternativa:</strong> Utilitza Apple Podcasts, AntennaPod o Pocket Casts.</p>
                        </div>
                    </details>
                </div>
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
        <p><small>100% generat amb IA (NotebookLM + Whisper + Claude) • Fomenta l'esperit crític • Busca la veritat per tu mateix</small></p>
    </div>
</footer>