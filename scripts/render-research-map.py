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


def svg(paths, css):
    return '<svg class="' + css + '" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.65" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false">' + paths + '</svg>'


question_icons = {
    'understand': '<path d="M2 12s3.5-6 10-6 10 6 10 6-3.5 6-10 6S2 12 2 12Z"/><circle cx="12" cy="12" r="3"/><path d="M12 2v2m0 16v2M4 4l1.5 1.5M18.5 18.5 20 20"/>',
    'evolve': '<path d="M19 8a8 8 0 0 0-13-2L3 9m0-5v5h5m-3 7a8 8 0 0 0 13 2l3-3m0 5v-5h-5"/><path d="m12 7 1.4 3.6L17 12l-3.6 1.4L12 17l-1.4-3.6L7 12l3.6-1.4Z"/>',
    'reliability': '<path d="m12 3 8 3v6c0 4.5-4.5 7.5-8 9-3.5-1.5-8-4.5-8-9V6Z"/><path d="m8 12 3 3 5-6"/>'
}
topic_icons = {
    'Repository understanding': '<path d="M3 6a2 2 0 0 1 2-2h5l2 3h7a2 2 0 0 1 2 2v3M3 6v12a2 2 0 0 0 2 2h6"/><circle cx="16" cy="15" r="4"/><path d="m19 18 3 3"/>',
    'Planning & reasoning': '<circle cx="5" cy="5" r="2"/><circle cx="19" cy="19" r="2"/><path d="M5 7v7a3 3 0 0 0 3 3h3a3 3 0 0 0 0-6h-1a3 3 0 0 1 0-6h7m-3-3 3 3-3 3"/>',
    'Context management': '<path d="M3 3h7M3 7h5m-5 4h4M21 3h-7m7 4h-5m5 4h-4M7 14l5 5 5-5m-5-8v13M5 22h14"/>',
    'Experience & skills': '<path d="M12 5v16M3 4c3-1 6-1 9 1 3-2 6-2 9-1v15c-3-1-6-1-9 1-3-2-6-2-9-1Z"/><path d="m7 8 .8 2.2L10 11l-2.2.8L7 14l-.8-2.2L4 11l2.2-.8M15 9h3m-3 4h3"/>',
    'Training data synthesis': '<ellipse cx="9" cy="5" rx="6" ry="3"/><path d="M3 5v11c0 1.7 2.7 3 6 3m6-14v4M3 10c0 1.7 2.7 3 6 3M3 15c0 1.7 2.7 3 6 3"/><path d="m17 10 1.5 4L22 15.5l-3.5 1.4L17 21l-1.5-4.1-3.5-1.4 3.5-1.5Z"/>',
    'Recursive self-improvement': '<path d="M20 10a8 8 0 1 0-2 8M20 4v6h-6"/><path d="m8 12 4-4 4 4m-4-4v9"/><circle cx="20" cy="18" r="2"/>',
    'Generation & testing': '<path d="m8 5-6 6 6 6m8-12 6 6-3 3m-6-12-3 18"/><path d="m15 19 2 2 5-5"/>',
    'Benchmarks & generalization': '<path d="M3 18a9 9 0 1 1 18 0M6 18h12M12 18l4-7M5 11l2 1m3-7 .5 2M18 7l-1.5 1.5"/><circle cx="12" cy="18" r="1.5"/>'
}


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
    '      <p class="research-map-note" data-tree-en="Explore the questions behind my work. Hover or focus a topic icon for its label." data-tree-zh="从研究问题出发，串起我的工作。悬停或点按图标可查看方向，点击论文可阅读。">Explore the questions behind my work. Hover or focus a topic icon for its label.</p>',
    '      <ol class="research-tree">'
]
seen = []
for index, question in enumerate(questions, 1):
    parts.append(f'        <li class="tree-question-group" data-question="{html.escape(question["id"], quote=True)}">')
    parts.append('          <h3 class="tree-question"><span class="tree-question-icon">' + svg(question_icons[question['id']], 'tree-root-svg') + '</span><span class="tree-question-heading"><span class="tree-question-number" aria-hidden="true">0' + str(index) + '</span>' + label('span', 'tree-question-text', question['en'], question['zh']) + '</span></h3>')
    parts.append('          <ul class="tree-branches">')
    for branch in question['branches']:
        parts.append('            <li class="tree-branch">')
        parts.append('              <h4 class="tree-branch-label" tabindex="0" aria-label="' + html.escape(branch['en'], quote=True) + '">' + svg(topic_icons[branch['en']], 'tree-topic-svg') + label('span', 'tree-topic-tooltip', branch['en'], branch['zh']) + '</h4>')
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
