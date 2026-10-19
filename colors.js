(() => {
  const requested = new URLSearchParams(location.search).get('set');
  const collection = ['new', 'original'].includes(requested) ? requested : 'all';
  document.querySelectorAll('.palette-card').forEach(card => {
    card.hidden = collection !== 'all' && card.dataset.collection !== collection;
  });
  document.querySelectorAll('[data-palette-set]').forEach(link => {
    if (link.dataset.paletteSet === collection) link.setAttribute('aria-current', 'page');
  });
  if (collection === 'new') {
    document.querySelector('#palette-title').textContent = '再试六种新的配色。';
    document.querySelector('#palette-description').textContent = '酒红、青瓷、琥珀、蔷薇、靛蓝与墨绿夜色。保持同一布局，直接比较它们的气质。';
  } else if (collection === 'original') {
    document.querySelector('#palette-title').textContent = '回看原来的六套配色。';
    document.querySelector('#palette-description').textContent = '雾蓝、松绿、陶土、灰紫、黑白与深夜。也可以切换到新增方案或一起比较。';
  }

  const previews = document.querySelectorAll('.mini-preview');
  function sizePreview(element) {
    const scale = element.clientWidth / 1200;
    element.style.setProperty('--preview-scale', scale);
    element.style.height = `${Math.round(930 * scale)}px`;
  }
  previews.forEach(sizePreview);
  if ('ResizeObserver' in window) {
    const observer = new ResizeObserver(entries => entries.forEach(entry => sizePreview(entry.target)));
    previews.forEach(element => observer.observe(element));
  } else {
    window.addEventListener('resize', () => previews.forEach(sizePreview));
  }
})();
