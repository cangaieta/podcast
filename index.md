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

            <!-- Manual Instructions Prominently Featured -->
            <div class="manual-subscription-primary">
                <div class="manual-header">
                    <h3>📋 Subscripció Manual (Recomanada)</h3>
                    <p>Mètode més fiable i compatible amb totes les apps de podcasts</p>
                </div>

                <div class="rss-copy-section">
                    <label for="rss-input">URL del Feed RSS:</label>
                    <div class="rss-input-group">
                        <input type="text" id="rss-input" value="{{ site.url }}{{ site.baseurl }}/feed.xml" readonly>
                        <button onclick="copyRSS()" class="copy-btn">📋 Copiar</button>
                    </div>
                </div>

                <div class="manual-steps">
                    <div class="step-card">
                        <div class="step-number">1</div>
                        <div class="step-content">
                            <h4>Copia l'URL RSS</h4>
                            <p>Utilitza el botó "Copiar" de dalt per copiar l'adreça del feed</p>
                        </div>
                    </div>
                    <div class="step-card">
                        <div class="step-number">2</div>
                        <div class="step-content">
                            <h4>Obre la teva app de podcasts</h4>
                            <p>Qualsevol app: Apple Podcasts, Google Podcasts, Pocket Casts, Castro...</p>
                        </div>
                    </div>
                    <div class="step-card">
                        <div class="step-number">3</div>
                        <div class="step-content">
                            <h4>Cerca l'opció "Afegir per URL"</h4>
                            <p>Normalment a la secció de subscripcions o biblioteca</p>
                        </div>
                    </div>
                    <div class="step-card">
                        <div class="step-number">4</div>
                        <div class="step-content">
                            <h4>Enganxa l'URL i subscriu-te</h4>
                            <p>Ja estaràs subscrit i rebràs els nous episodis automàticament</p>
                        </div>
                    </div>
                </div>
            </div>

            <!-- App-specific instructions -->
            <div class="app-specific-help">
                <h3>🔧 Instruccions específiques per app</h3>
                <div class="app-instructions-grid">
                    <details class="app-detail">
                        <summary><strong>🍎 Apple Podcasts</strong></summary>
                        <div class="instruction-content">
                            <p><strong>iPhone/iPad:</strong></p>
                            <ol>
                                <li>Obre Apple Podcasts</li>
                                <li>Toca "Biblioteca" (baix de la pantalla)</li>
                                <li>Toca "Editar" (dalt dreta)</li>
                                <li>Toca "Afegir un programa per URL"</li>
                                <li>Enganxa l'URL i toca "Subscriure's"</li>
                            </ol>
                            <p><strong>Mac:</strong></p>
                            <ol>
                                <li>Obre Apple Podcasts</li>
                                <li>Ves a "Biblioteca"</li>
                                <li>Menú "Fitxer" → "Subscriure a podcast"</li>
                                <li>Enganxa l'URL i confirma</li>
                            </ol>
                        </div>
                    </details>

                    <details class="app-detail">
                        <summary><strong>🟢 Google Podcasts</strong></summary>
                        <div class="instruction-content">
                            <ol>
                                <li>Obre Google Podcasts</li>
                                <li>Toca "Explorar" (menú inferior)</li>
                                <li>Toca "Subscripcions"</li>
                                <li>Toca el botó "+" o "Afegir per RSS"</li>
                                <li>Enganxa l'URL</li>
                            </ol>
                        </div>
                    </details>

                    <details class="app-detail">
                        <summary><strong>🟤 Pocket Casts</strong></summary>
                        <div class="instruction-content">
                            <ol>
                                <li>Obre Pocket Casts</li>
                                <li>Toca "Podcasts" (menú inferior)</li>
                                <li>Toca el botó "+" (dalt dreta)</li>
                                <li>Selecciona "Add podcast by URL"</li>
                                <li>Enganxa l'URL i confirma</li>
                            </ol>
                        </div>
                    </details>

                    <details class="app-detail">
                        <summary><strong>☁️ Overcast</strong></summary>
                        <div class="instruction-content">
                            <ol>
                                <li>Obre Overcast</li>
                                <li>Toca el botó "+" (dalt dreta)</li>
                                <li>Selecciona "Add URL"</li>
                                <li>Enganxa l'URL del feed</li>
                            </ol>
                        </div>
                    </details>

                    <details class="app-detail">
                        <summary><strong>📻 Castro</strong></summary>
                        <div class="instruction-content">
                            <ol>
                                <li>Obre Castro</li>
                                <li>Toca la lupa (Cercar)</li>
                                <li>Toca "Add from URL" (dalt dreta)</li>
                                <li>Enganxa l'URL del feed</li>
                                <li>Toca "Subscribe"</li>
                            </ol>
                        </div>
                    </details>

                    <details class="app-detail">
                        <summary><strong>⬇️ Downcast</strong></summary>
                        <div class="instruction-content">
                            <ol>
                                <li>Obre Downcast</li>
                                <li>Toca "Add Podcast"</li>
                                <li>Selecciona "By URL"</li>
                                <li>Enganxa l'URL del feed</li>
                                <li>Toca "Add"</li>
                            </ol>
                        </div>
                    </details>

                    <details class="app-detail">
                        <summary><strong>🤖 AntennaPod</strong></summary>
                        <div class="instruction-content">
                            <p><strong>Android només</strong></p>
                            <ol>
                                <li>Obre AntennaPod</li>
                                <li>Toca "Add Podcast" (botó +)</li>
                                <li>Selecciona "By RSS address"</li>
                                <li>Enganxa l'URL del feed</li>
                                <li>Toca "Confirm"</li>
                            </ol>
                        </div>
                    </details>

                    <details class="app-detail">
                        <summary><strong>🟣 Spotify</strong></summary>
                        <div class="instruction-content">
                            <p><strong>⚠️ Limitació:</strong> Spotify no suporta feeds RSS externs directament.</p>
                            <p><strong>Alternativa:</strong> Utilitza Apple Podcasts, Google Podcasts o Pocket Casts per escoltar el nostre podcast.</p>
                        </div>
                    </details>
                </div>
            </div>

            <!-- iPhone automatic subscription -->
            <div class="iphone-automatic-subscription" id="iphone-subscription">
                <h3>🍎 Subscripció automàtica (iPhone/iPad)</h3>
                <p>Els següents botons obren directament la teva app de podcasts:</p>

                <div class="subscribe-options">
                    <button onclick="subscribeApplePodcasts()" class="subscribe-btn apple-btn">
                        🍎 Apple Podcasts
                    </button>
                    <button onclick="subscribeOvercast()" class="subscribe-btn overcast-btn">
                        ☁️ Overcast
                    </button>
                    <button onclick="subscribeCastro()" class="subscribe-btn castro-btn">
                        📻 Castro
                    </button>
                    <button onclick="subscribeDowncast()" class="subscribe-btn downcast-btn">
                        ⬇️ Downcast
                    </button>
                    <button onclick="subscribePocketCasts()" class="subscribe-btn pocket-btn">
                        🟤 Pocket Casts
                    </button>
                </div>
            </div>

            <!-- Android subscription with three subsections -->
            <div class="android-manual-subscription" id="android-subscription">
                <h3>🤖 Subscripció per Android</h3>
                <p>Els URL schemes automàtics no funcionen bé en Android. Utilitza una d'aquestes opcions:</p>

                <!-- Subsection 1: Subscribe on Android button -->
                <div class="android-subscribe-button-section">
                    <h4>🌐 Subscripció Universal (Recomanat)</h4>
                    <div class="subscribe-android-button">
                        <a href="https://www.subscribeonandroid.com/cangaieta.github.io/podcast/feed.xml"
                           title="Subscribe on Android"
                           target="_blank"
                           rel="noopener">
                            <img src="https://assets.blubrry.com/soa/BadgeLarge.png"
                                 alt="Subscribe on Android"
                                 style="border:0; max-width: 200px; height: auto;" />
                        </a>
                    </div>
                    <p class="android-description">
                        Detecta automàticament les teves apps de podcasts instal·lades i t'ajuda a subscriure't.
                    </p>
                </div>

                <!-- Subsection 2: Manual subscription steps -->
                <div class="android-manual-steps">
                    <h4>📱 Subscripció Manual</h4>
                    <div class="manual-steps-left">
                        <div class="step-card-left">
                            <div class="step-number">1</div>
                            <div class="step-content-left">
                                <h5>Copia l'URL del feed RSS</h5>
                                <div class="rss-input-group">
                                    <input type="text" id="rss-input-android" value="{{ site.url }}{{ site.baseurl }}/feed.xml" readonly>
                                    <button onclick="copyRSSNoAlert()" class="copy-btn">📋 Copiar</button>
                                </div>
                            </div>
                        </div>
                        <div class="step-card-left">
                            <div class="step-number">2</div>
                            <div class="step-content-left">
                                <h5>Obre la teva app de podcasts</h5>
                                <p>AntennaPod, Pocket Casts, Podcast Addict, Player FM...</p>
                            </div>
                        </div>
                        <div class="step-card-left">
                            <div class="step-number">3</div>
                            <div class="step-content-left">
                                <h5>Afegeix per URL o RSS</h5>
                                <p>Cerca l'opció "Afegir podcast per URL", "Add by RSS" o similar</p>
                            </div>
                        </div>
                        <div class="step-card-left">
                            <div class="step-number">4</div>
                            <div class="step-content-left">
                                <h5>Enganxa i subscriu-te</h5>
                                <p>Enganxa l'URL copiat i confirma la subscripció</p>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Subsection 3: App-specific instructions -->
                <div class="android-app-instructions">
                    <h4>🔧 Instruccions per app específica</h4>
                    <div class="android-apps-left">
                        <details class="android-app-detail">
                            <summary><strong>🤖 AntennaPod</strong></summary>
                            <div class="android-instruction-content">
                                <ol>
                                    <li>Obre AntennaPod</li>
                                    <li>Toca "Add Podcast" (botó +)</li>
                                    <li>Selecciona "By RSS address"</li>
                                    <li>Enganxa l'URL del feed</li>
                                    <li>Toca "Confirm"</li>
                                </ol>
                            </div>
                        </details>

                        <details class="android-app-detail">
                            <summary><strong>🟤 Pocket Casts</strong></summary>
                            <div class="android-instruction-content">
                                <ol>
                                    <li>Obre Pocket Casts</li>
                                    <li>Toca "Podcasts" (menú inferior)</li>
                                    <li>Toca el botó "+" (dalt dreta)</li>
                                    <li>Selecciona "Add podcast by URL"</li>
                                    <li>Enganxa l'URL i confirma</li>
                                </ol>
                            </div>
                        </details>

                        <details class="android-app-detail">
                            <summary><strong>📻 Podcast Addict</strong></summary>
                            <div class="android-instruction-content">
                                <ol>
                                    <li>Obre Podcast Addict</li>
                                    <li>Toca el menú (☰)</li>
                                    <li>Selecciona "Add Podcast"</li>
                                    <li>Toca "Add Podcast by URL"</li>
                                    <li>Enganxa l'URL del feed</li>
                                </ol>
                            </div>
                        </details>

                        <details class="android-app-detail">
                            <summary><strong>🎵 Player FM</strong></summary>
                            <div class="android-instruction-content">
                                <ol>
                                    <li>Obre Player FM</li>
                                    <li>Toca "Discover" i després la lupa</li>
                                    <li>Toca "Add custom RSS URL"</li>
                                    <li>Enganxa l'URL del feed</li>
                                </ol>
                            </div>
                        </details>
                    </div>
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
        <p><small>Contingut generat amb IA • Fonts sempre transparents</small></p>
    </div>
</footer>