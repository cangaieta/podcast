---
layout: landing
title: "Tots els Episodis"
permalink: /episodis/
---

<div class="episodes-header">
  <div class="header-nav">
    <a href="{{ '/' | relative_url }}" class="btn-back-header">← Tornar a l'inici</a>
    <a href="https://docs.google.com/forms/d/e/1FAIpQLSe1bA1mx4xQhM_6gspCBxSr2KE0M-26eks1wwwk5B4r4z1Psg/viewform" target="_blank" class="btn-cta-header">Uneix-te</a>
  </div>
  <h1>Tots els Episodis del Podcast</h1>
</div>

<div class="episodes-page">
  {% assign sorted_episodes = site.episodes | sort: 'date' | reverse %}

  {% if sorted_episodes.size == 0 %}
    <div class="no-episodes">
      <h2>🎙️ Properament...</h2>
      <p>Estem preparant els primers episodis del podcast. Torna aviat!</p>
      <a href="{{ '/' | relative_url }}" class="btn-back">← Tornar a l'inici</a>
    </div>
  {% else %}
    <div class="episodes-grid">
      {% for episode in sorted_episodes %}
        <article class="episode-card">
          {% if episode.thumbnail %}
          <a href="{{ episode.url | relative_url }}" class="episode-thumb-link" tabindex="-1" aria-hidden="true">
            {% include episode-thumb.html episode=episode class="episode-thumb" size=140 %}
          </a>
          {% endif %}

          <div class="episode-body">
          <header class="episode-header">
            <h2><a href="{{ episode.url | relative_url }}">{{ episode.title }}</a></h2>
            <div class="episode-meta">
              <time datetime="{{ episode.date | date_to_xmlschema }}">{{ episode.date | date: "%d/%m/%Y" }}</time>
              {% if episode.duration %}<span class="duration">{{ episode.duration }}</span>{% endif %}
            </div>
          </header>

          {% if episode.audio_file %}
          <div class="audio-player">
            <audio controls preload="none">
              {% if episode.audio_file contains "http" %}
              <source src="{{ episode.audio_file }}" type="audio/mpeg">
              {% else %}
              <source src="{{ '/episodes/' | append: episode.audio_file | relative_url }}" type="audio/mpeg">
              {% endif %}
              El teu navegador no suporta l'element d'audio.
            </audio>
          </div>
          {% endif %}

          <div class="episode-description">
            <p>{{ episode.description }}</p>
          </div>

          <div class="episode-actions">
            <a href="{{ episode.url | relative_url }}" class="btn-read">Llegir més</a>
            {% if episode.audio_file %}
              {% if episode.audio_file contains "http" %}
              <a href="{{ episode.audio_file }}" download class="btn-download">⬇️ Descarregar</a>
              {% else %}
              <a href="{{ '/episodes/' | append: episode.audio_file | relative_url }}" download class="btn-download">⬇️ Descarregar</a>
              {% endif %}
            {% endif %}
          </div>
          </div>
        </article>
      {% endfor %}
    </div>
  {% endif %}
</div>

<style>
.episodes-header {
  max-width: 1000px;
  margin: 0 auto;
  padding: 2rem 2rem 0 2rem;
  position: relative;
}

.header-nav {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}

.btn-back-header {
  background: transparent;
  color: #956B5A !important;
  padding: 0.8rem 1.5rem;
  text-decoration: none;
  font-size: 0.95rem;
  font-weight: 500;
  border: 2px solid #956B5A;
  border-radius: 8px;
  box-shadow: none;
  transition: border-color 0.2s ease;
}

.btn-back-header:visited,
.btn-back-header:active {
  color: #956B5A !important;
}

.btn-back-header:hover {
  color: #7A5548 !important;
  border-color: #7A5548;
  background: transparent;
  box-shadow: none;
}

.btn-cta-header {
  display: inline-block;
  background: #B8907D;
  color: white;
  padding: 1rem 2rem;
  text-decoration: none;
  border-radius: 8px;
  transition: all 0.25s ease;
  font-weight: 700;
  border: 2px solid #A67B6A;
  box-shadow: 0 4px 12px rgba(0,0,0,0.15);
}

.btn-cta-header:hover {
  background: #956B5A;
  border-color: #7A5548;
}

.btn-back-header:hover {
  background: #A67B6A;
  border-color: #956B5A;
  box-shadow: 0 8px 20px rgba(0,0,0,0.2);
}

.episodes-header h1 {
  color: var(--verd-natura);
  font-size: 2.5rem;
  margin: 0;
  text-align: center;
}

.episodes-page {
  max-width: 1000px;
  margin: 0 auto;
  padding: 0 2rem 2rem 2rem;
}

.no-episodes {
  text-align: center;
  padding: 4rem 2rem;
  background: var(--bg-secondary);
  border-radius: 15px;
  margin: 2rem 0;
}

.no-episodes h2 {
  color: var(--verd-natura);
  margin-bottom: 1rem;
}

.btn-back {
  display: inline-block;
  background: #B8907D;
  color: white;
  padding: 1rem 2rem;
  text-decoration: none;
  border-radius: 8px;
  margin-top: 1rem;
  transition: all 0.25s ease;
  font-weight: 700;
  border: 2px solid #A67B6A;
  box-shadow: 0 4px 12px rgba(0,0,0,0.15);
}

.btn-back:hover {
  background: #A67B6A;
  border-color: #956B5A;
  box-shadow: 0 8px 20px rgba(0,0,0,0.2);
}

.episodes-grid {
  display: grid;
  gap: 2rem;
  margin: 2rem 0;
}

.episode-card {
  background: var(--bg-primary);
  border-radius: 15px;
  padding: 2rem;
  box-shadow: 0 5px 15px var(--shadow-color);
  transition: all 0.3s ease;
  border: 1px solid var(--border-color);
  display: flex;
  gap: 2rem;
  align-items: flex-start;
}

.episode-card:hover {
  box-shadow: 0 10px 30px var(--shadow-color-strong);
}

.episode-thumb-link {
  flex-shrink: 0;
  display: block;
  line-height: 0;
}

.episode-thumb {
  width: 140px;
  height: 140px;
  border-radius: 12px;
  box-shadow: 0 6px 20px rgba(0,0,0,0.25);
  object-fit: cover;
  display: block;
}

/* Perquè el contingut llarg no desbordi la fila flex */
.episode-body {
  flex: 1;
  min-width: 0;
}

.episode-header h2 {
  margin: 0 0 0.5rem 0;
  font-size: 1.5rem;
  color: var(--verd-natura);
}

.episode-header h2 a {
  color: inherit;
  text-decoration: none;
}

.episode-header h2 a:hover {
  color: var(--terra-cuita);
}

.episode-meta {
  color: var(--text-tertiary);
  font-size: 0.9rem;
  margin-bottom: 1rem;
}

.episode-meta .duration {
  margin-left: 1rem;
  background: var(--bg-secondary);
  padding: 0.2rem 0.5rem;
  border-radius: 4px;
  color: var(--text-primary);
}

.audio-player {
  margin: 1.5rem 0;
}

.audio-player audio {
  width: 100%;
}

.episode-description {
  margin: 1rem 0;
  line-height: 1.6;
  color: var(--text-secondary);
}

.episode-actions {
  display: flex;
  gap: 1rem;
  margin-top: 1.5rem;
}

.btn-read, .btn-download {
  padding: 1rem 2rem;
  border-radius: 8px;
  text-decoration: none;
  font-size: 0.9rem;
  font-weight: 700;
  transition: all 0.25s ease;
  border: 2px solid transparent;
  box-shadow: 0 4px 12px rgba(0,0,0,0.15);
}

.btn-read {
  background: #7A9B7F;
  color: white;
  border-color: #6A8A70;
}

.btn-read:hover {
  background: #6A8A70;
  border-color: #5A7A60;
  box-shadow: 0 8px 20px rgba(0,0,0,0.2);
}

.btn-download {
  background: #B8907D;
  color: white;
  border-color: #A67B6A;
}

.btn-download:hover {
  background: #A67B6A;
  border-color: #956B5A;
  box-shadow: 0 8px 20px rgba(0,0,0,0.2);
}

@media (max-width: 768px) {
  .episodes-page {
    padding: 1rem;
  }

  .episode-card {
    padding: 1.5rem;
    /* Apilada: la caràtula creix en comptes d'encongir-se */
    flex-direction: column;
    align-items: center;
    gap: 1.5rem;
  }

  .episode-thumb {
    width: 200px;
    height: 200px;
  }

  .episode-body {
    width: 100%;
  }

  .episode-actions {
    flex-direction: column;
  }
}
</style>