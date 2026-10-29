const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');

const source = fs.readFileSync(path.join(__dirname, '..', 'theme-init.js'), 'utf8');
const cases = [
  { name: 'new visitors start in English', query: '', stored: null, expected: 'en' },
  { name: 'Chinese URL works for new visitors', query: '?lang=zh', stored: null, expected: 'zh-CN' },
  { name: 'saved Chinese is restored', query: '', stored: 'zh', expected: 'zh-CN' },
  { name: 'English URL overrides saved Chinese', query: '?lang=en', stored: 'zh', expected: 'en' },
  { name: 'Chinese URL overrides saved English', query: '?lang=zh', stored: 'en', expected: 'zh-CN' },
  { name: 'invalid URL falls back to saved language', query: '?lang=invalid', stored: 'zh', expected: 'zh-CN' },
  { name: 'invalid preference falls back to English', query: '', stored: 'invalid', expected: 'en' },
  { name: 'Chinese URL works when storage is blocked', query: '?lang=zh', blocked: true, expected: 'zh-CN' },
  { name: 'blocked storage keeps English available', query: '', blocked: true, expected: 'en' }
];
for (const scenario of cases) {
  test(scenario.name, () => {
    const root = { dataset: {}, lang: 'en', classList: { add() {} } };
    vm.runInNewContext(source, {
      URLSearchParams,
      window: { location: { search: scenario.query + (scenario.query ? '&' : '?') + 'theme=amber' } },
      document: { documentElement: root },
      localStorage: { getItem(key) {
        if (scenario.blocked) throw new Error('Storage is unavailable');
        return key === 'silin-homepage-language' ? scenario.stored : null;
      } }
    });
    assert.equal(root.lang, scenario.expected);
    assert.equal(root.dataset.theme, 'amber');
  });
}
