(() => {
  const themes = ['mist', 'pine', 'clay', 'mauve', 'ink', 'midnight', 'wine', 'celadon', 'amber', 'rose', 'indigo', 'forest'];
  const params = new URLSearchParams(window.location.search);
  const fromUrl = params.get('theme');
  const embedded = params.get('embed') === '1';
  let stored = null;
  try { stored = localStorage.getItem('silin-homepage-theme'); } catch (_) { /* Storage can be unavailable in private browsing. */ }
  const theme = themes.includes(fromUrl) ? fromUrl : (themes.includes(stored) ? stored : 'amber');
  document.documentElement.dataset.theme = theme;
  if (embedded) document.documentElement.classList.add('embed');
})();
