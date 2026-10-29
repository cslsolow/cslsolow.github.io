(() => {
  const themes = ['mist', 'pine', 'clay', 'mauve', 'ink', 'midnight', 'wine', 'celadon', 'amber', 'rose', 'indigo', 'forest'];
  const params = new URLSearchParams(window.location.search);
  const fromUrl = params.get('theme');
  const embedded = params.get('embed') === '1';
  let stored = null;
  try { stored = localStorage.getItem('silin-homepage-theme'); } catch (_) { /* Storage can be unavailable in private browsing. */ }
  const theme = themes.includes(fromUrl) ? fromUrl : (themes.includes(stored) ? stored : 'amber');
  document.documentElement.dataset.theme = theme;
  let storedLanguage = null;
  try { storedLanguage = localStorage.getItem('silin-homepage-language'); } catch (_) { /* URL and default still work without storage. */ }
  const fromLanguageUrl = params.get('lang');
  const language = ['en', 'zh'].includes(fromLanguageUrl) ? fromLanguageUrl : (['en', 'zh'].includes(storedLanguage) ? storedLanguage : 'en');
  document.documentElement.lang = language === 'zh' ? 'zh-CN' : 'en';
  if (embedded) document.documentElement.classList.add('embed');
})();
