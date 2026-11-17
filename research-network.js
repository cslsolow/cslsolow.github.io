(() => {
  const section = document.querySelector('#research-map');
  if (!section) return;
  const graph = section.querySelector('.research-network');
  const viewport = section.querySelector('.network-viewport');
  const nodes = [...section.querySelectorAll('.network-node')];
  const edges = [...section.querySelectorAll('.network-edge')];
  const clusters = [...section.querySelectorAll('.network-cluster')];
  const filters = [...section.querySelectorAll('[data-topic-filter]')];
  const caption = section.querySelector('.network-selection');
  const fit = section.querySelector('.network-fit');
  const byId = new Map(nodes.map(node => [node.dataset.nodeId, node]));
  let topic = 'all';
  let hovered = null;

  function memberships(node) { return node.dataset.topics.split(' '); }
  edges.forEach(edge => {
    if (memberships(byId.get(edge.dataset.source))[0] !== memberships(byId.get(edge.dataset.target))[0]) {
      edge.classList.add('network-edge-bridge');
    }
  });
  function showConnections() {
    const chinese = document.documentElement.lang === 'zh-CN';
    const active = new Set();
    if (hovered) active.add(hovered);
    else if (topic !== 'all') nodes.forEach(node => { if (memberships(node).includes(topic)) active.add(node.dataset.nodeId); });
    const neighborhood = new Set(active);
    edges.forEach(edge => {
      if (active.has(edge.dataset.source) || active.has(edge.dataset.target)) {
        neighborhood.add(edge.dataset.source);
        neighborhood.add(edge.dataset.target);
      }
    });
    const selectedTopics = new Set();
    active.forEach(id => memberships(byId.get(id)).forEach(id => selectedTopics.add(id)));
    graph.classList.toggle('has-selection', active.size > 0);
    nodes.forEach(node => {
      const id = node.dataset.nodeId;
      node.classList.toggle('is-active', active.has(id));
      node.classList.toggle('is-related', neighborhood.has(id));
    });
    edges.forEach(edge => edge.classList.toggle('is-active', active.has(edge.dataset.source) || active.has(edge.dataset.target)));
    clusters.forEach(cluster => cluster.classList.toggle('is-active', selectedTopics.has(cluster.dataset.topic)));
    filters.forEach(button => button.setAttribute('aria-pressed', String(button.dataset.topicFilter === topic)));
    if (hovered) {
      const node = byId.get(hovered);
      const labels = memberships(node).map(id => clusters.find(cluster => cluster.dataset.topic === id).querySelector('text').textContent);
      caption.textContent = node.querySelector('.network-node-name').textContent + ' · ' + labels.join(' / ');
    } else if (topic !== 'all') {
      const label = clusters.find(cluster => cluster.dataset.topic === topic).querySelector('text').textContent;
      caption.textContent = label + (chinese ? ' · ' + active.size + ' 篇论文（含跨簇论文）' : ' · ' + active.size + ' papers, including shared-topic work');
    } else {
      caption.textContent = chinese ? caption.dataset.treeZh : caption.dataset.treeEn;
    }
    viewport.setAttribute('aria-label', chinese ? '研究关联图。小屏幕下可左右滑动，也可缩放全图。' : 'Research network. Scroll horizontally on smaller screens, or fit the full graph.');
    section.querySelector('.network-filters').setAttribute('aria-label', chinese ? '研究主题' : 'Research topics');
  }
  function focusNode(event) {
    const node = event.target.closest('.network-node');
    if (!node) return;
    hovered = node.dataset.nodeId;
    showConnections();
  }
  graph.addEventListener('pointerover', focusNode);
  graph.addEventListener('focusin', focusNode);
  graph.addEventListener('pointerleave', () => {
    if (!graph.contains(document.activeElement)) { hovered = null; showConnections(); }
  });
  graph.addEventListener('focusout', event => {
    if (!graph.contains(event.relatedTarget)) { hovered = null; showConnections(); }
  });
  filters.forEach(button => {
    button.hidden = false;
    button.addEventListener('click', () => {
      topic = button.dataset.topicFilter;
      hovered = null;
      showConnections();
    });
  });
  fit.hidden = false;
  fit.setAttribute('aria-pressed', 'false');
  fit.addEventListener('click', () => {
    const fitted = viewport.classList.toggle('network-fitted');
    fit.setAttribute('aria-pressed', String(fitted));
    fit.dataset.treeEn = fitted ? 'Actual size' : 'Fit graph';
    fit.dataset.treeZh = fitted ? '恢复大小' : '缩放全图';
    fit.textContent = document.documentElement.lang === 'zh-CN' ? fit.dataset.treeZh : fit.dataset.treeEn;
  });
  document.addEventListener('homepage-language-change', showConnections);
  showConnections();
})();
