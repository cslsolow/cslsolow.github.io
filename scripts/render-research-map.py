#!/usr/bin/env python3
"""Render a clustered paper network with overlapping topic memberships."""
from pathlib import Path
import html
import json
import re

ROOT = Path(__file__).resolve().parents[1]
page = (ROOT / 'index.html').read_text()
papers = {paper['title']: paper for paper in json.loads((ROOT / 'content.json').read_text())['publications']}
graph = json.loads((ROOT / 'research-map.json').read_text())
nodes, topics, edges = graph['nodes'], graph['topics'], graph['edges']
assert len(nodes) == len({node['id'] for node in nodes}), 'Duplicate graph node'
assert len(nodes) == len({node['title'] for node in nodes}) == len(papers), 'Every publication needs exactly one graph node'
assert {node['title'] for node in nodes} == set(papers), 'Publication coverage mismatch'
topic_ids = {topic['id'] for topic in topics}
assert len(topic_ids) == len(topics), 'Duplicate topic'
assert all(node['topics'] and len(set(node['topics'])) == len(node['topics']) and set(node['topics']) <= topic_ids for node in nodes), 'Invalid topic membership'
by_id = {node['id']: node for node in nodes}
assert all(edge['source'] in by_id and edge['target'] in by_id and edge['source'] != edge['target'] for edge in edges), 'Invalid graph edge'
assert len({tuple(sorted((e['source'], e['target']))) for e in edges}) == len(edges), 'Duplicate graph edge'


def esc(value):
    return html.escape(str(value), quote=True)


def bilingual(tag, css, en, zh, extra=''):
    return f'<{tag} class="{css}" data-tree-en="{esc(en)}" data-tree-zh="{esc(zh)}"{extra}>{html.escape(en)}</{tag}>'


venues = {'arXiv': 'Preprint', 'ASE 2026': 'ASE 2026', 'ISSTA 2026': 'ISSTA 2026',
          'Internetware 2026': 'Internetware 2026', 'IP&M · 2027': 'IP&M 2027',
          'EMNLP 2026': 'EMNLP 2026', 'NeurIPS 2026 · Meta-Agents Workshop': 'NeurIPS 2026 Workshop'}
parts = ['    <!-- research-map:start -->',
         '    <section id="research-map" class="research-map" aria-labelledby="research-map-title">',
         '      ' + bilingual('h2', '', 'Research connections', '研究关联', ' id="research-map-title"'),
         '      ' + bilingual('p', 'research-map-note', 'Shared ideas connect these papers. A paper can belong to more than one topic.', '用共享的研究主题连接论文；一篇论文可以同时属于多个簇。'),
         '      <div class="network-toolbar"><div class="network-filters" role="group" aria-label="Research topics">',
         '        ' + bilingual('button', 'network-filter', 'All topics', '全部主题', ' type="button" data-topic-filter="all" aria-pressed="true" hidden')]
for topic in topics:
    parts.append('        ' + bilingual('button', 'network-filter', topic['en'], topic['zh'], f' type="button" data-topic-filter="{esc(topic["id"])}" aria-pressed="false" hidden'))
parts.extend(['      </div><button class="network-fit" type="button" data-tree-en="Fit graph" data-tree-zh="缩放全图" hidden>Fit graph</button></div>',
              '      <div class="network-viewport" tabindex="0" aria-label="Research network. Scroll horizontally to explore on smaller screens.">',
              '      <svg class="research-network" viewBox="0 0 820 768" role="group" aria-labelledby="network-title network-description">',
              '        <title id="network-title">Research topics and paper connections</title>',
              '        <desc id="network-description">13 papers in five overlapping topics. SkillForge links experience, data synthesis and repository knowledge. Lines indicate shared themes, not citation relationships.</desc>',
              '        <g class="network-clusters">'])
for topic in topics:
    tid = topic['id']
    text_x = topic['x'] + 18 if tid != 'synthesis' else 568
    parts.append(f'          <g class="network-cluster" data-topic="{esc(tid)}"><rect x="{topic["x"]}" y="{topic["y"]}" width="{topic["width"]}" height="{topic["height"]}" rx="22"/><circle cx="{text_x}" cy="{topic["y"] + 25}" r="3"/><text x="{text_x + 11}" y="{topic["y"] + 30}" data-tree-en="{esc(topic["en"])}" data-tree-zh="{esc(topic["zh"])}">{html.escape(topic["en"])}</text></g>')
parts.append('        </g><g class="network-edges" aria-hidden="true">')
for edge in edges:
    a, b = by_id[edge['source']], by_id[edge['target']]
    parts.append(f'          <line class="network-edge" data-source="{esc(a["id"])}" data-target="{esc(b["id"])}" x1="{a["x"]}" y1="{a["y"]}" x2="{b["x"]}" y2="{b["y"]}"/>')
parts.append('        </g><g class="network-nodes">')
for node in nodes:
    paper = papers[node['title']]
    x, y, width = node['x'], node['y'], node['width']
    height = node.get('height', 58)
    shared = ' network-node-shared' if len(node['topics']) > 1 else ''
    parts.append(f'          <a class="network-node{shared}" data-node-id="{esc(node["id"])}" data-topics="{esc(" ".join(node["topics"]))}" href="{esc(paper["paper"])}" target="_blank" rel="noopener noreferrer" lang="en" aria-label="{esc(paper["title"])}"><title>{html.escape(paper["title"])}</title><rect x="{x-width/2:g}" y="{y-height/2:g}" width="{width}" height="{height}" rx="10"/>')
    for index, tid in enumerate(node['topics']):
        parts.append(f'            <circle class="network-membership" data-topic="{esc(tid)}" cx="{x-width/2+12 + index*9:g}" cy="{y-16}" r="3"/>')
    parts.append(f'            <text class="network-node-name" x="{x}" y="{y+2}" text-anchor="middle">{html.escape(node["short"])}</text><text class="network-node-venue" x="{x}" y="{y+18}" text-anchor="middle">{html.escape(venues.get(paper["venue"], paper["venue"]))}</text></a>')
parts.extend(['        </g>',
              '        ' + bilingual('text', 'network-bridge-note', 'Experience × data synthesis', '经验学习 × 数据合成', ' x="447" y="280" text-anchor="middle"'),
              '      </svg></div>',
              '      <div class="network-caption"><p class="network-selection" role="status" aria-live="polite" data-tree-en="Hover or focus a paper to highlight its connections. Select a topic to explore a cluster." data-tree-zh="悬停或聚焦论文以高亮关联，点击主题可查看对应簇。">Hover or focus a paper to highlight its connections. Select a topic to explore a cluster.</p>',
              '        ' + bilingual('span', 'network-scroll-hint', 'Swipe to explore · lines = shared themes', '左右滑动查看 · 连线表示相关研究主题'),
              '      </div>',
              '      <details class="network-topic-index"><summary data-tree-en="Browse papers by topic" data-tree-zh="按主题浏览论文">Browse papers by topic</summary><div class="network-topic-list">'])
for topic in topics:
    parts.append('        <div>' + bilingual('h3', '', topic['en'], topic['zh']) + '<ul>')
    for node in nodes:
        if topic['id'] in node['topics']:
            paper = papers[node['title']]
            parts.append(f'          <li><a href="{esc(paper["paper"])}" target="_blank" rel="noopener noreferrer" lang="en">{html.escape(node["short"])}</a></li>')
    parts.append('        </ul></div>')
parts.extend(['      </div></details>', '    </section>', '    <!-- research-map:end -->'])
result, count = re.subn(r'    <!-- research-map:start -->.*?    <!-- research-map:end -->', lambda _: '\n'.join(parts), page, flags=re.S)
assert count == 1, 'Expected one research-map placeholder'
(ROOT / 'index.html').write_text(result)
print(f'Rendered {len(nodes)} paper nodes, {len(topics)} topic clusters, and {len(edges)} connections.')
