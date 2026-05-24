const appState = {
  lang: localStorage.getItem("gamehub-lang") || "es"
};

const LABELS = {
  es: {
    brandCopy: "Noticias, rankings y comunidad del videojuego.",
    nav: {
      home: "Descubrir",
      catalog: "Catalogo",
      blog: "Comunidad",
      media: "Multimedia",
      news: "Noticias",
      agenda: "Agenda",
      team: "Equipo",
      contact: "Contacto",
      auth: "Iniciar sesion",
      dashboard: "Dashboard"
    },
    footer: "© 2026. Disenado para la comunidad.",
    login: "Iniciar sesion",
    topRated: "TOP VALORADOS",
    fullList: "Ver listado completo",
    viewDescription: "Ver descripcion",
    play: "Ver trailer oficial",
    contactSent: "Mensaje enviado en modo demo. Cuando exista backend, esto ira a la API real.",
    authDemo: "Flujo simulado correctamente. Pendiente de conexion con backend Python y MySQL."
  },
  en: {
    brandCopy: "Gaming news, rankings and community.",
    nav: {
      home: "Discover",
      catalog: "Catalog",
      blog: "Community",
      media: "Media",
      news: "News",
      agenda: "Agenda",
      team: "Team",
      contact: "Contact",
      auth: "Sign in",
      dashboard: "Dashboard"
    },
    footer: "© 2026. Designed for the community.",
    login: "Sign in",
    topRated: "TOP RATED",
    fullList: "See full list",
    viewDescription: "View description",
    play: "Watch official trailer",
    contactSent: "Message sent in demo mode. Once the backend exists, this will call the real API.",
    authDemo: "Mock flow completed successfully. Pending connection to the Python backend and MySQL."
  }
};

function label(key) {
  return key.split(".").reduce((acc, part) => acc?.[part], LABELS[appState.lang]) ?? key;
}

function mountShell(activePage) {
  const header = document.querySelector("[data-site-header]");
  const footer = document.querySelector("[data-site-footer]");

  if (header) {
    header.innerHTML = `
      <div class="brand-wrap">
        <a href="index.html"><img class="brand-mark" src="assets/images/logo-white.png" alt="Game-Hub"></a>
        <p class="brand-copy">${label("brandCopy")}</p>
      </div>
      <nav class="main-nav">
        ${navLink(label("nav.home"), "index.html", activePage)}
        ${navLink(label("nav.catalog"), "catalogo.html", activePage)}
        ${navLink(label("nav.blog"), "blog.html", activePage)}
        ${navLink(label("nav.media"), "multimedia.html", activePage)}
        ${navLink(label("nav.news"), "noticias.html", activePage)}
        ${navLink(label("nav.agenda"), "agenda.html", activePage)}
      </nav>
      <div class="header-actions">
        <span class="search-icon">🔍</span>
        <button class="lang-toggle" type="button" id="lang-toggle">${appState.lang.toUpperCase()}</button>
      </div>
      <a class="login-button primary-btn" href="auth.html">${label("login")}</a>
    `;
  }

  if (footer) {
    footer.innerHTML = `
      <div>
        <strong>GAME-HUB</strong>
        <p class="muted">${label("footer")}</p>
      </div>
      <div class="footer-links">
        <a href="contacto.html">${label("nav.contact")}</a>
        <a href="equipo.html">${label("nav.team")}</a>
        <a href="dashboard.html">${label("nav.dashboard")}</a>
      </div>
    `;
  }

  document.getElementById("lang-toggle")?.addEventListener("click", () => {
    appState.lang = appState.lang === "es" ? "en" : "es";
    localStorage.setItem("gamehub-lang", appState.lang);
    boot(activePage);
  });
}

function navLink(text, href, activePage) {
  return `<a class="${href === activePage ? "active" : ""}" href="${href}">${text}</a>`;
}

function renderHome() {
  const newsTarget = document.querySelector(".home-news-list");
  const topTarget = document.querySelector(".home-top-rated");
  if (newsTarget) {
    newsTarget.innerHTML = window.GAMEHUB_DATA.homeNews.map((item) => `
      <a class="news-feature link-card" href="${item.href || '#'}">
        <div class="thumb-box"><img src="${item.image}" alt="${item.title}"></div>
        <div>
          <span class="eyebrow ${item.categoryClass || ""}">${item.category}</span>
          <h3>${item.title}</h3>
          <p class="muted">${item.excerpt}</p>
        </div>
      </a>
    `).join("");
  }
  if (topTarget) {
    topTarget.innerHTML = `
      <article class="top-rated">
        <h3>${label("topRated")}</h3>
        ${window.GAMEHUB_DATA.topRated.map((item) => `
          <div class="top-item">
            <div class="top-rank">${item.rank}</div>
            <div>
              <strong>${item.title}</strong>
              <div class="muted">${item.genre}</div>
            </div>
            <div class="score-badge ${item.scoreClass}">${item.score}</div>
          </div>
        `).join("")}
        <a class="simple-outline-btn" href="blog.html">${label("fullList")}</a>
      </article>
    `;
  }
}

function renderCatalog() {
  const target = document.querySelector(".catalog-grid");
  if (!target) return;
  target.innerHTML = window.GAMEHUB_DATA.catalogGames.map((game) => `
    <article class="catalog-card link-card">
      <div class="catalog-cover"><img src="${game.image}" alt="${game.title}"></div>
      <div class="catalog-body">
        <h3 class="catalog-title">${game.title}</h3>
        <div class="catalog-meta">${game.genre}</div>
        <div class="catalog-footer">
          <div class="rating-line"><span>⭐</span><span>${game.score}</span></div>
          <a class="text-link" href="${game.href || '#'}">${label("viewDescription")}</a>
        </div>
      </div>
    </article>
  `).join("");
}

function renderCommunity() {
  const target = document.querySelector(".community-list");
  if (!target) return;
  target.innerHTML = window.GAMEHUB_DATA.communityRanking.map((game) => `
    <article class="community-row link-card">
      <div class="community-score">${game.score}</div>
      <div>
        <div class="muted" style="text-align:center; font-weight:800; margin-bottom:10px;">${game.position}</div>
        <div class="community-cover"><img src="${game.image}" alt="${game.title}"></div>
      </div>
      <div>
        <div class="community-title">
          <h3 style="margin:0;">${game.title}</h3>
          <span class="platform-tag">${game.platform}</span>
        </div>
        <p class="muted">${game.description}</p>
        <a class="community-link" href="${game.href || '#'}">${label("viewDescription")}</a>
      </div>
    </article>
  `).join("");
}

function renderMedia() {
  const hero = document.querySelector(".video-hero");
  const grid = document.querySelector(".video-grid");
  if (hero) {
    const item = window.GAMEHUB_DATA.videos.featured;
    hero.innerHTML = `
      <div class="video-frame">
        <div class="play-orb">▶</div>
      </div>
      <div class="video-meta">
        <div>
          <h2 style="margin:0 0 6px;">${item.title}</h2>
          <p class="muted" style="margin:0;">${item.subtitle}</p>
        </div>
        <div style="text-align:right;">
          <div class="eyebrow blue">${item.quality}</div>
          <div class="muted" style="margin-top:6px;">${item.views}</div>
        </div>
      </div>
    `;
  }
  if (grid) {
    grid.innerHTML = window.GAMEHUB_DATA.videos.latest.map((video) => `
      <article>
        <div class="video-thumb">
          <img src="${video.image}" alt="${video.title}">
        </div>
        <div class="video-card-title">${video.title}</div>
        <div class="video-card-meta">${video.meta} · ${video.duration}</div>
      </article>
    `).join("");
  }
}

function renderBlog() {
  const target = document.querySelector(".blog-feed");
  if (!target) return;
  target.innerHTML = window.GAMEHUB_DATA.blogPosts.map((post) => `
    <article class="card">
      <span class="eyebrow">Opinion</span>
      <h2>${post.title}</h2>
      <p class="muted">${post.summary}</p>
      <div class="muted">${post.author} · ${post.comments} comentarios</div>
    </article>
  `).join("");
}

function renderNews() {
  const target = document.querySelector(".news-feed");
  if (!target) return;
  target.innerHTML = window.GAMEHUB_DATA.homeNews.map((item) => `
    <article class="card">
      <div class="news-card-image"><img src="${item.image}" alt="${item.title}"></div>
      <span class="eyebrow ${item.categoryClass || ""}">${item.category}</span>
      <h2>${item.title}</h2>
      <p class="muted">${item.excerpt}</p>
      <a class="community-link" href="${item.href || '#'}">${label("viewDescription")}</a>
    </article>
  `).join("");
}

function renderTeam() {
  const target = document.querySelector(".team-grid");
  if (!target) return;
  target.innerHTML = window.GAMEHUB_DATA.team.map((member) => `
    <article class="card">
      <span class="eyebrow">${member.role}</span>
      <h3>${member.name}</h3>
      <p class="muted">${member.bio}</p>
    </article>
  `).join("");
}

function renderAgenda() {
  const target = document.querySelector(".agenda-list");
  if (!target) return;
  target.innerHTML = window.GAMEHUB_DATA.events.map((event) => `
    <article class="card">
      <span class="eyebrow">${event.type}</span>
      <h3>${event.title}</h3>
      <p class="muted">${event.date}</p>
      <div class="muted">${event.place}</div>
    </article>
  `).join("");
}

function renderDashboard() {
  const copy = document.querySelector(".dashboard-copy");
  const stats = document.querySelector(".dashboard-stats");
  if (copy) copy.textContent = window.GAMEHUB_DATA.dashboard.welcome;
  if (stats) {
    stats.innerHTML = window.GAMEHUB_DATA.dashboard.stats.map((stat) => `
      <article class="card">
        <div class="eyebrow">${stat.label}</div>
        <h2>${stat.value}</h2>
      </article>
    `).join("");
  }
}

function renderArticleDetail() {
  const target = document.querySelector(".article-layout");
  if (!target) return;
  const article = window.GAMEHUB_DATA.articleDetail;
  target.innerHTML = `
    <article class="article-card">
      <span class="tag-badge" style="margin-bottom:16px;">${article.category}</span>
      <h1 class="article-headline">${article.title}</h1>
      <div class="article-author-row article-meta">
        <strong>Por ${article.author}</strong>
        <span>${article.meta}</span>
      </div>
      <div class="share-row article-meta" style="justify-content:flex-end; margin-top:12px;">
        <span>Compartir:</span>
        <span>𝕏</span>
        <span>fb</span>
      </div>
      <div class="article-hero-image">
        IMAGEN DEL ARTICULO
        <span class="image-credit">${article.imageCredit}</span>
      </div>
      <div class="article-body">
        <p>${article.intro}</p>
        <h2>${article.sectionTitle}</h2>
        <p>${article.body1}</p>
      </div>
      <div class="quote-block">
        <blockquote>"${article.quote}"</blockquote>
        <cite>— ${article.quoteAuthor}</cite>
      </div>
      <div class="article-body">
        <p>${article.body2}</p>
      </div>
      <div class="tag-row" style="margin-top:24px;">
        <span class="muted">Etiquetas:</span>
        ${article.tags.map((tag) => `<span class="tag-pill">${tag}</span>`).join("")}
      </div>
    </article>
  `;
}

function renderGameDetail() {
  const target = document.querySelector(".game-detail-layout");
  if (!target) return;
  const game = window.GAMEHUB_DATA.gameDetail;
  target.innerHTML = `
    <article class="game-detail-card">
      <div class="game-hero-grid">
        <div class="game-cover"><img src="assets/images/elden-ring.jpg" alt="${game.title}"></div>
        <div>
          <h1 class="detail-title">${game.title}</h1>
          <div class="detail-meta-row game-copy" style="margin-bottom:16px;">
            <span><strong>Desarrollador:</strong> <span style="color:#38bdf8; font-weight:700;">${game.developer}</span></span>
            <span><strong>Editor:</strong> ${game.publisher}</span>
          </div>
          <div class="platform-row" style="margin-bottom:20px;">
            ${game.platforms.map((platform) => `<span class="platform-pill">${platform}</span>`).join("")}
          </div>
          <div class="game-copy">Fecha de lanzamiento: ${game.releaseDate}</div>
          <div class="game-copy" style="margin-top:8px;">Genero: ${game.genre}</div>
        </div>
        <div>
          <div class="muted" style="text-align:center; font-size:0.75rem; font-weight:800; margin-bottom:12px;">RATING GLOBAL</div>
          <div class="detail-score">${game.score}</div>
          <div class="detail-qualifier">${game.qualifier}</div>
        </div>
      </div>

      <section style="margin-bottom:36px;">
        <h2>RESUMEN Y DETALLES</h2>
        <div class="card" style="background:#f8fafc; color:#0f172a; box-shadow:none; border:1px solid #e2e8f0;">
          <p class="game-copy" style="margin:0;">${game.summary}</p>
        </div>
      </section>

      <section>
        <h2>MULTIMEDIA Y GAMEPLAY</h2>
        <div class="media-gallery">
          ${game.media.map((item) => `<div class="media-tile">${item.label}</div>`).join("")}
        </div>
      </section>
    </article>
  `;
}

function initContactForm() {
  const form = document.querySelector("#contact-form");
  const notice = document.querySelector(".form-notice");
  if (!form || !notice || form.dataset.bound === "true") return;
  form.addEventListener("submit", (event) => {
    event.preventDefault();
    notice.textContent = label("contactSent");
    form.reset();
  });
  form.dataset.bound = "true";
}

function initAuthForms() {
  const forms = document.querySelectorAll(".mock-form");
  forms.forEach((form) => {
    if (form.dataset.bound === "true") return;
    form.addEventListener("submit", (event) => {
      event.preventDefault();
      const target = form.querySelector(".form-feedback");
      if (target) target.textContent = label("authDemo");
    });
    form.dataset.bound = "true";
  });
}

function boot(activePage) {
  document.documentElement.lang = appState.lang;
  mountShell(activePage);
  renderHome();
  renderCatalog();
  renderCommunity();
  renderMedia();
  renderBlog();
  renderNews();
  renderTeam();
  renderAgenda();
  renderDashboard();
  renderArticleDetail();
  renderGameDetail();
  initContactForm();
  initAuthForms();
}
