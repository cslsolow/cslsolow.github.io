"""Check the research-map renderer and its publication coverage contract."""
from pathlib import Path
import json
import re
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


class ResearchMapTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name)
        (self.root / 'scripts').mkdir()
        for name in ('index.html', 'content.json', 'research-map.json'):
            shutil.copyfile(ROOT / name, self.root / name)
        shutil.copyfile(ROOT / 'scripts/render-research-map.py', self.root / 'scripts/render-research-map.py')

    def render(self):
        return subprocess.run([sys.executable, str(self.root / 'scripts/render-research-map.py')], capture_output=True, text=True)

    def test_complete_unique_static_tree_and_idempotent_render(self):
        before = (self.root / 'index.html').read_text()
        self.assertEqual(self.render().returncode, 0)
        first = (self.root / 'index.html').read_text()
        self.assertEqual(first, before)
        self.assertEqual(self.render().returncode, 0)
        self.assertEqual((self.root / 'index.html').read_text(), first)
        tree = re.search(r'<section id="research-map".*?</section>', first, re.S).group()
        papers = json.loads((self.root / 'content.json').read_text())['publications']
        self.assertEqual(tree.count('class="tree-paper"'), len(papers))
        self.assertEqual(tree.count('class="tree-question"'), 3)
        self.assertEqual(tree.count('class="tree-branch"'), 8)
        self.assertEqual(tree.count('class="tree-topic-svg"'), 8)
        self.assertEqual(tree.count('class="tree-root-svg"'), 3)
        self.assertEqual(tree.count('class="tree-topic-tooltip"'), 8)
        for paper in papers:
            self.assertIn('href="' + paper['paper'].replace('&', '&amp;') + '"', tree)
        for section in ('about', 'news', 'publications'):
            expression = r'<section id="' + section + r'".*?</section>'
            self.assertEqual(re.search(expression, before, re.S).group(), re.search(expression, first, re.S).group())

    def test_duplicate_paper_does_not_overwrite_page(self):
        path = self.root / 'research-map.json'
        data = json.loads(path.read_text())
        branch = data['questions'][0]['branches'][0]
        branch['papers'].append(branch['papers'][0])
        path.write_text(json.dumps(data))
        before = (self.root / 'index.html').read_text()
        result = self.render()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('Each publication must appear exactly once', result.stderr)
        self.assertEqual((self.root / 'index.html').read_text(), before)

    def test_missing_paper_does_not_overwrite_page(self):
        path = self.root / 'research-map.json'
        data = json.loads(path.read_text())
        data['questions'][0]['branches'][0]['papers'].pop()
        path.write_text(json.dumps(data))
        before = (self.root / 'index.html').read_text()
        self.assertNotEqual(self.render().returncode, 0)
        self.assertEqual((self.root / 'index.html').read_text(), before)


if __name__ == '__main__':
    unittest.main()
