(() => {
  const root = document.documentElement;
  const toggle = document.querySelector('#language-toggle');
  const about = document.querySelector('#about-copy');
  const chineseAbout = document.querySelector('#about-zh');
  const englishAbout = document.createDocumentFragment();
  englishAbout.append(...[...about.childNodes].map(node => node.cloneNode(true)));

  // Only these elements are translated. The entire Publications section stays English.
  const translations = [
    ['.skip-link', '跳至正文'],
    ['.nav-links a[href="#about"]', '关于我'],
    ['.nav-links a[href="#news"]', '动态'],
    ['.nav-links a[href="#publications"]', '论文'],
    ['#about-title', '关于我'],
    ['#news-title', '最新动态'],
    ['.profile-role', '即将入学的博士生'],
    ['.profile-subtitle', '香港科技大学（广州） · MAYU Lab'],
    ['.profile-location', '中国，上海'],
    ['.profile-note .eyebrow', '研究方向'],
    ['.profile-focus', '编程智能体、自我改进与仓库级代码生成。'],
    ['.footer span:last-child', '最近更新：2026 年 10 月'],
    ['#theme-label', '配色 · '],
    ['.appearance-heading > span', '试试不同的配色', 'Choose a theme'],
    ['.appearance-heading > small', '同一布局，即时切换', 'Preview instantly'],
    ['.compare-link', '比较全部 12 套配色 ↗', 'Compare all 12 themes ↗']
  ].map(([selector, zh, en]) => {
    const element = document.querySelector(selector);
    return { element, zh, english: [...element.childNodes].map(node => node.cloneNode(true)), en };
  });
  const attributes = [
    ['.nav-wrap', 'aria-label', '主导航'],
    ['.profile', 'aria-label', '个人资料'],
    ['.portrait', 'alt', 'Silin Chen 的头像']
  ].map(([selector, attribute, zh]) => {
    const element = document.querySelector(selector);
    return { element, attribute, zh, en: element.getAttribute(attribute) };
  });
  const news = [...document.querySelectorAll('#news li')].map(item => {
    const paragraph = item.querySelector('p');
    const time = item.querySelector('time');
    return { paragraph, english: paragraph.cloneNode(true), time, dateText: time.textContent,
      dateTitle: time.getAttribute('title') };
  });
  const description = document.querySelector('meta[name="description"]');
  const englishDescription = description.content;
  const englishTitle = document.title;

  function strong(text) {
    const node = document.createElement('strong');
    node.textContent = text;
    return node;
  }
  function englishClone(node) {
    const copy = node.cloneNode(true);
    copy.lang = 'en';
    return copy;
  }
  function chineseNews(original) {
    const fragment = document.createDocumentFragment();
    const links = [...original.querySelectorAll('a')];
    if (links.some(link => link.hostname === 'www.swebench.com')) {
      fragment.append(englishClone(links[0]), ' 在 ', englishClone(links[1]), ' 的',
        strong('开源模型与开源 scaffold'), ' 类别中取得', strong('第二名'), '！');
    } else {
      const onlinePublication = original.textContent.includes('published online');
      fragment.append('我们的论文 ', englishClone(links[0]), onlinePublication ? ' 已在 ' : ' 已被 ',
        englishClone(original.querySelector('strong')), onlinePublication ? ' 在线发表。' : ' 接收。');
    }
    return fragment;
  }
  function updateLanguage(language, persist = false) {
    if (!['en', 'zh'].includes(language)) return;
    const chinese = language === 'zh';
    root.lang = chinese ? 'zh-CN' : 'en';
    translations.forEach(({ element, zh, english, en }) => {
      if (chinese || en) element.textContent = chinese ? zh : en;
      else element.replaceChildren(...english.map(node => node.cloneNode(true)));
    });
    attributes.forEach(({ element, attribute, zh, en }) => element.setAttribute(attribute, chinese ? zh : en));
    about.replaceChildren((chinese ? chineseAbout.content : englishAbout).cloneNode(true));
    news.forEach(({ paragraph, english, time, dateText, dateTitle }) => {
      paragraph.replaceChildren(...(chinese ? [chineseNews(english)] : [...english.childNodes].map(node => node.cloneNode(true))));
      const date = time.getAttribute('datetime');
      time.textContent = chinese ? date.slice(0, 4) + '年' + Number(date.slice(5, 7)) + '月' : dateText;
      if (chinese && date.length === 10) time.title = date.slice(0, 4) + '年' + Number(date.slice(5, 7)) + '月' + Number(date.slice(8, 10)) + '日';
      else if (dateTitle) time.title = dateTitle;
      else time.removeAttribute('title');
    });
    document.title = chinese ? 'Silin Chen — 软件工程与人工智能' : englishTitle;
    description.content = chinese ? 'Silin Chen，即将入读香港科技大学（广州）博士项目，研究面向软件工程的大语言模型、编程智能体、自我改进、评测基准与仓库级代码生成。' : englishDescription;
    document.querySelector('.appearance-panel').lang = root.lang;
    toggle.textContent = chinese ? 'English' : '中文';
    toggle.lang = chinese ? 'en' : 'zh-CN';
    toggle.setAttribute('aria-label', chinese ? 'Switch to English' : '切换到中文');
    toggle.hidden = false;
    if (persist) {
      try { localStorage.setItem('silin-homepage-language', language); } catch (_) { /* URL still persists the choice for this page. */ }
      const url = new URL(window.location.href);
      url.searchParams.set('lang', language);
      history.replaceState(null, '', url);
      document.querySelector('#language-announcement').textContent = chinese ? '已切换到中文，论文部分保留英文。' : 'Switched to English.';
    }
    document.dispatchEvent(new CustomEvent('homepage-language-change', { detail: { language } }));
  }
  toggle.addEventListener('click', () => updateLanguage(root.lang === 'zh-CN' ? 'en' : 'zh', true));
  updateLanguage(root.lang === 'zh-CN' ? 'zh' : 'en');
})();
