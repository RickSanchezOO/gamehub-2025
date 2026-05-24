const API_BASE = 'http://127.0.0.1:5000/api';

async function apiFetch(endpoint) {
  try {
    const res = await fetch(`${API_BASE}${endpoint}`);
    if (!res.ok) throw new Error('API error');
    return await res.json();
  } catch (e) {
    return null;
  }
}

async function loadNews() {
  const data = await apiFetch('/news');
  if (!data || data.length === 0) return null;
  return data.map(n => ({
    category: n.tags || 'Noticias',
    categoryClass: '',
    title: n.title,
    excerpt: n.excerpt,
    image: n.image || 'assets/images/hardware-news.png',
    href: 'articulo.html'
  }));
}

async function loadGames() {
  const data = await apiFetch('/games');
  if (!data || data.length === 0) return null;
  return data.map(g => ({
    title: g.title,
    genre: g.genre || '',
    platform: '',
    score: g.communityScore || g.pressScore || '—',
    description: g.description || '',
    image: g.image || 'assets/images/hero-cyber-frontier.png',
    href: 'juego.html'
  }));
}

async function loadRanking() {
  const data = await apiFetch('/games/ranking');
  if (!data || data.length === 0) return null;
  return data.map((g, i) => ({
    rank: String(i + 1).padStart(2, '0'),
    title: g.title,
    genre: '',
    score: g.communityScore || '—',
    scoreClass: 'green'
  }));
}

async function loadPosts() {
  const data = await apiFetch('/posts');
  if (!data || data.length === 0) return null;
  return data.map(p => ({
    title: p.title,
    summary: p.excerpt,
    author: p.author,
    comments: 0
  }));
}

async function loadEvents() {
  const data = await apiFetch('/events');
  if (!data || data.length === 0) return null;
  return data.map(e => ({
    title: e.name,
    date: e.date,
    place: e.location || '',
    type: 'Evento'
  }));
}

async function loadMedia() {
  const data = await apiFetch('/media');
  if (!data || data.length === 0) return null;
  return data;
}

async function loadTeam() {
  const data = await apiFetch('/team');
  if (!data || data.length === 0) return null;
  return data.map(u => ({
    name: u.displayName,
    role: u.role,
    bio: ''
  }));
}

async function loadDashboard() {
  const data = await apiFetch('/dashboard');
  if (!data) return null;
  return data;
}

window.GAMEHUB_API = {
  loadNews,
  loadGames,
  loadRanking,
  loadPosts,
  loadEvents,
  loadMedia,
  loadTeam,
  loadDashboard
};