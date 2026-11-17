#!/usr/bin/env python3
"""Render the bilingual research tree as static, accessible HTML."""
from pathlib import Path
import html
import json
import re

ROOT = Path(__file__).resolve().parents[1]
page = (ROOT / 'index.html').read_text()
papers = {paper['title']: paper for paper in json.loads((ROOT / 'content.json').read_text())['publications']}
questions = json.loads((ROOT / 'research-map.json').read_text())['questions']
icons = {}
for block in re.findall(r'<article class="publication"[^>]*>.*?</article>', page, re.S):
    title = html.unescape(re.search(r'<h3 class="paper-title">.*?<a [^>]*>(.*?)</a>', block, re.S).group(1))
    icons[title] = re.search(r'<svg.*?</svg>', block, re.S).group()


def label(tag, css, en, zh):
    return f'<{tag} class="{css}" data-tree-en="{html.escape(en, quote=True)}" data-tree-zh="{html.escape(zh, quote=True)}">{html.escape(en)}</{tag}>'


venues = {
    'arXiv': 'Preprint',
    'ASE 2026': "ASE ’26",
    'ISSTA 2026': "ISSTA ’26",
    'Internetware 2026': "Internetware ’26",
    'IP&M · 2027': "IP&M ’27",
    'EMNLP 2026': "EMNLP ’26",
    'NeurIPS 2026 · Meta-Agents Workshop': "NeurIPS ’26 Workshop"
}
parts = [
    '    <!-- research-map:start -->',
    '    <section id="research-map" class="research-map" aria-labelledby="research-map-title">',
    '      <h2 id="research-map-title" data-tree-en="Research map" data-tree-zh="研究脉络">Research map</h2>',
    '      <p class="research-map-note" data-tree-en="The questions connecting my work. Select a paper to explore." data-tree-zh="从研究问题出发，串起我的工作。点击论文节点可查看详情。">The questions connecting my work. Select a paper to explore.</p>',
    '      <ol class="research-tree">'
]
seen = []
for index, question in enumerate(questions, 1):
    parts.append(f'        <li class="tree-question-group" data-question="{html.escape(question["id"], quote=True)}">')
    parts.append('          <h3 class="tree-question"><span class="tree-question-number" aria-hidden="true">Q' + str(index) + '</span>' + label('span', 'tree-question-text', question['en'], question['zh']) + '</h3>')
    parts.append('          <ul class="tree-branches">')
    for branch in question['branches']:
        parts.append('            <li class="tree-branch">')
        parts.append('              ' + label('h4', 'tree-branch-label', branch['en'], branch['zh']))
        parts.append('              <ul class="tree-papers">')
        for work in branch['papers']:
            title = work['title']
            paper = papers[title]
            seen.append(title)
            venue = venues.get(paper['venue'], paper['venue'])
            parts.append('                <li><a class="tree-paper" lang="en" href="' + html.escape(paper['paper'], quote=True) + '" target="_blank" rel="noopener noreferrer" title="' + html.escape(title, quote=True) + '"><span class="tree-paper-icon">' + icons[title] + '</span><span class="tree-paper-name">' + html.escape(work['short']) + '</span><span class="tree-paper-venue">' + html.escape(venue) + '</span></a></li>')
        parts.extend(['              </ul>', '            </li>'])
    parts.extend(['          </ul>', '        </li>'])
parts.extend(['      </ol>', '    </section>', '    <!-- research-map:end -->'])
assert len(seen) == len(set(seen)) == len(papers), 'Each publication must appear exactly once in the research map'
assert set(seen) == set(papers)
result, count = re.subn(r'    <!-- research-map:start -->.*?    <!-- research-map:end -->', lambda _: '\n'.join(parts), page, flags=re.S)
assert count == 1, 'Expected exactly one research-map placeholder'
(ROOT / 'index.html').write_text(result)
print(f'Rendered {len(questions)} research questions and {len(seen)} paper nodes.')
