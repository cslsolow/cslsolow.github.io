"""Validate clustered graph coverage and meaningful cross-topic relationships."""
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

    def save(self, graph):
        (self.root / 'research-map.json').write_text(json.dumps(graph))

    def test_complete_unique_graph_and_idempotence(self):
        before = (self.root / 'index.html').read_text()
        self.assertEqual(self.render().returncode, 0)
        rendered = (self.root / 'index.html').read_text()
        self.assertEqual(rendered, before)
        self.assertEqual(self.render().returncode, 0)
        self.assertEqual((self.root / 'index.html').read_text(), rendered)
        graph = json.loads((self.root / 'research-map.json').read_text())
        papers = json.loads((self.root / 'content.json').read_text())['publications']
        section = re.search(r'<section id="research-map".*?</section>', rendered, re.S).group()
        self.assertEqual(len(re.findall(r'class="network-node(?: network-node-shared)?"', section)), len(papers))
        self.assertEqual(section.count('class="network-cluster"'), len(graph['topics']))
        self.assertEqual(section.count('class="network-edge"'), len(graph['edges']))
        for paper in papers:
            self.assertIn('href="' + paper['paper'].replace('&', '&amp;') + '"', section)
        for name in ('about', 'news', 'publications'):
            pattern = r'<section id="' + name + r'".*?</section>'
            self.assertEqual(re.search(pattern, before, re.S).group(), re.search(pattern, rendered, re.S).group())

    def test_all_papers_analyzed_and_cross_topic_memberships(self):
        graph = json.loads((self.root / 'research-map.json').read_text())
        nodes = {node['id']: node for node in graph['nodes']}
        self.assertEqual(set(graph['analysis']), set(nodes))
        self.assertTrue(all(graph['analysis'].values()))
        self.assertTrue({'experience', 'synthesis', 'understanding'} <= set(nodes['skillforge']['topics']))
        self.assertTrue({'synthesis', 'evaluation'} <= set(nodes['swe-scale']['topics']))
        self.assertTrue({'development', 'evaluation'} <= set(nodes['advertest']['topics']))
        self.assertTrue(all(edge.get('reason') for edge in graph['edges']))
        self.assertTrue(any({edge['source'], edge['target']} == {'skillforge', 'swe-scale'} for edge in graph['edges']))

    def test_duplicate_node_does_not_overwrite_page(self):
        graph = json.loads((self.root / 'research-map.json').read_text())
        graph['nodes'].append(graph['nodes'][0])
        self.save(graph)
        before = (self.root / 'index.html').read_text()
        self.assertNotEqual(self.render().returncode, 0)
        self.assertEqual((self.root / 'index.html').read_text(), before)

    def test_missing_paper_does_not_overwrite_page(self):
        graph = json.loads((self.root / 'research-map.json').read_text())
        graph['nodes'].pop()
        self.save(graph)
        before = (self.root / 'index.html').read_text()
        self.assertNotEqual(self.render().returncode, 0)
        self.assertEqual((self.root / 'index.html').read_text(), before)

    def test_invalid_edge_does_not_overwrite_page(self):
        graph = json.loads((self.root / 'research-map.json').read_text())
        graph['edges'].append({'source': 'missing', 'target': 'skillforge'})
        self.save(graph)
        before = (self.root / 'index.html').read_text()
        self.assertNotEqual(self.render().returncode, 0)
        self.assertEqual((self.root / 'index.html').read_text(), before)


if __name__ == '__main__':
    unittest.main()
