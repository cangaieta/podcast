---
layout: landing
title: "Tots els Episodis"
permalink: /episodis/
---

# Tots els Episodis del Podcast

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
          <header class="episode-header">
            <h2><a href="{{ episode.url }}">{{ episode.title }}</a></h2>
            <div class="episode-meta">
              <time datetime="{{ episode.date | date_to_xmlschema }}">{{ episode.date | date: "%d/%m/%Y" }}</time>
              {% if episode.duration %}<span class="duration">{{ episode.duration }}</span>{% endif %}
            </div>
          </header>

          {% if episode.audio_file %}
          <div class="audio-player">
            <audio controls preload="none">
              <source src="{{ '/episodes/' | append: episode.audio_file | relative_url }}" type="audio/mpeg">
              El teu navegador no suporta l'element d'audio.
            </audio>
          </div>
          {% endif %}

          <div class="episode-description">
            <p>{{ episode.description }}</p>
          </div>

          <div class="episode-actions">
            <a href="{{ episode.url }}" class="btn-read">Llegir més</a>
            {% if episode.audio_file %}
              <a href="{{ '/episodes/' | append: episode.audio_file | relative_url }}" download class="btn-download">⬇️ Descarregar</a>
            {% endif %}
          </div>
        </article>
      {% endfor %}
    </div>
  {% endif %}
</div>

<style>
.episodes-page {
  max-width: 1000px;
  margin: 0 auto;
  padding: 2rem;
}

.no-episodes {
  text-align: center;
  padding: 4rem 2rem;
  background: #f8f9fa;
  border-radius: 15px;
  margin: 2rem 0;
}

.no-episodes h2 {
  color: #4C8150;
  margin-bottom: 1rem;
}

.btn-back {
  display: inline-block;
  background: #CD6155;
  color: white;
  padding: 0.8rem 1.5rem;
  text-decoration: none;
  border-radius: 25px;
  margin-top: 1rem;
  transition: all 0.3s ease;
}

.btn-back:hover {
  background: #B85450;
  transform: translateY(-2px);
}

.episodes-grid {
  display: grid;
  gap: 2rem;
  margin: 2rem 0;
}

.episode-card {
  background: white;
  border-radius: 15px;
  padding: 2rem;
  box-shadow: 0 5px 15px rgba(0,0,0,0.08);
  transition: all 0.3s ease;
}

.episode-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 30px rgba(0,0,0,0.15);
}

.episode-header h2 {
  margin: 0 0 0.5rem 0;
  font-size: 1.5rem;
  color: #4C8150;
}

.episode-header h2 a {
  color: inherit;
  text-decoration: none;
}

.episode-header h2 a:hover {
  color: #CD6155;
}

.episode-meta {
  color: #666;
  font-size: 0.9rem;
  margin-bottom: 1rem;
}

.episode-meta .duration {
  margin-left: 1rem;
  background: #F5EEDC;
  padding: 0.2rem 0.5rem;
  border-radius: 4px;
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
  color: #555;
}

.episode-actions {
  display: flex;
  gap: 1rem;
  margin-top: 1.5rem;
}

.btn-read, .btn-download {
  padding: 0.6rem 1.2rem;
  border-radius: 20px;
  text-decoration: none;
  font-size: 0.9rem;
  font-weight: 500;
  transition: all 0.3s ease;
}

.btn-read {
  background: #4C8150;
  color: white;
}

.btn-read:hover {
  background: #3d6640;
  transform: translateY(-2px);
}

.btn-download {
  background: #E67E22;
  color: white;
}

.btn-download:hover {
  background: #D35400;
  transform: translateY(-2px);
}

@media (max-width: 768px) {
  .episodes-page {
    padding: 1rem;
  }

  .episode-card {
    padding: 1.5rem;
  }

  .episode-actions {
    flex-direction: column;
  }
}
</style>