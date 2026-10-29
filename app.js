(() => {
  const root = document.documentElement;
  const labels = { mist: '雾蓝', pine: '松绿', clay: '陶土', mauve: '灰紫', ink: '黑白', midnight: '深夜', wine: '酒红', celadon: '青瓷', amber: '琥珀', rose: '蔷薇', indigo: '靛蓝', forest: '墨绿夜' };
  const englishLabels = { mist: 'Mist', pine: 'Pine', clay: 'Clay', mauve: 'Mauve', ink: 'Ink', midnight: 'Midnight', wine: 'Wine', celadon: 'Celadon', amber: 'Amber', rose: 'Rose', indigo: 'Indigo', forest: 'Forest' };
  const buttons = [...document.querySelectorAll('[data-set-theme]')];
  const currentTheme = document.querySelector('#current-theme');
  const announce = document.querySelector('#theme-announcement');
  function updateTheme(theme, persist) {
    if (!Object.hasOwn(labels, theme)) return;
    root.dataset.theme = theme;
    buttons.forEach(button => button.setAttribute('aria-pressed', String(button.dataset.setTheme === theme)));
    if (currentTheme) currentTheme.textContent = root.lang === 'zh-CN' ? labels[theme] : englishLabels[theme];
    if (persist) {
      try { localStorage.setItem('silin-homepage-theme', theme); } catch (_) { /* Switching still works without storage. */ }
      const url = new URL(window.location.href);
      url.searchParams.set('theme', theme);
      history.replaceState(null, '', url);
      if (announce) announce.textContent = root.lang === 'zh-CN' ? '已切换为' + labels[theme] + '配色' : 'Switched to the ' + englishLabels[theme] + ' theme';
    }
  }
  document.addEventListener('homepage-language-change', () => updateTheme(root.dataset.theme, false));
  updateTheme(root.dataset.theme, false);
  buttons.forEach(button => button.addEventListener('click', () => updateTheme(button.dataset.setTheme, true)));
  const appearance = document.querySelector('.appearance');
  document.addEventListener('keydown', event => {
    if (event.key === 'Escape' && appearance?.open) {
      appearance.open = false;
      appearance.querySelector('summary').focus();
    }
  });
  const papers = [...document.querySelectorAll('.publication')];
  const yearGroups = [...document.querySelectorAll('.year-group')];
  const categories = [...document.querySelectorAll('[data-category]')];
  const yearSelect = document.querySelector('#year-filter');
  const count = document.querySelector('#result-count');
  const empty = document.querySelector('#empty-state');
  let category = 'all';
  function filterPapers() {
    const year = yearSelect.value;
    let visible = 0;
    papers.forEach(paper => {
      const matchesCategory = category === 'all' || (category === 'first' && (paper.dataset.first === 'true' || paper.dataset.cofirst === 'true')) || (category === 'reviewed' && paper.dataset.reviewed === 'true');
      const show = matchesCategory && (year === 'all' || paper.dataset.year === year);
      paper.hidden = !show;
      visible += Number(show);
    });
    yearGroups.forEach(group => { group.hidden = ![...group.querySelectorAll('.publication')].some(paper => !paper.hidden); });
    categories.forEach(button => button.setAttribute('aria-pressed', String(button.dataset.category === category)));
    count.textContent = `${visible} of ${papers.length} works`;
    empty.hidden = visible > 0;
  }
  categories.forEach(button => button.addEventListener('click', () => { category = button.dataset.category; filterPapers(); }));
  yearSelect.addEventListener('change', filterPapers);
  document.querySelectorAll('[data-reset-filters]').forEach(button => button.addEventListener('click', () => { category = 'all'; yearSelect.value = 'all'; filterPapers(); }));
  filterPapers();
  const sections = [...document.querySelectorAll('main > section[id]')];
  const navLinks = [...document.querySelectorAll('.nav-links a')];
  if ('IntersectionObserver' in window) {
    const observer = new IntersectionObserver(entries => {
      const target = entries.find(entry => entry.isIntersecting);
      if (!target) return;
      navLinks.forEach(link => {
        const active = link.getAttribute('href') === `#${target.target.id}`;
        link.classList.toggle('active', active);
        if (active) link.setAttribute('aria-current', 'location'); else link.removeAttribute('aria-current');
      });
    }, { rootMargin: '-12% 0px -65% 0px', threshold: 0 });
    sections.forEach(section => observer.observe(section));
  }
})();
