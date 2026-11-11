"""Build the design story, files, variations, finished pieces and process notes."""
from pathlib import PurePosixPath
import html
import re


def esc(value):
    return html.escape(str(value), quote=True)


def local_url(root, pattern, src):
    path = PurePosixPath(src)
    if (path.is_absolute() or '..' in path.parts
            or path.parts[:2] != ('patterns', pattern['id'])
            or any(not re.fullmatch(r'[A-Za-z0-9._-]+', part) for part in path.parts)):
        raise ValueError('Expected a file belonging to this design: ' + src)
    file = root / 'docs' / src
    if not file.is_file() or file.resolve() != file.absolute():
        raise ValueError('Missing file or symlink: ' + src)
    return '../../' + src


def paragraphs(items):
    return ''.join('<p>' + esc(item) + '</p>' for item in items)


def image_cards(root, pattern, images):
    cards = []
    for item in images:
        src = esc(local_url(root, pattern, item['src']))
        dimensions = ''
        if item.get('width') and item.get('height'):
            dimensions = f' width="{int(item["width"])}" height="{int(item["height"])}"'
        cards.append('<figure class="process-image"><a href="' + src + '"><img src="' + src
                     + '" alt="' + esc(item['alt']) + '"' + dimensions + ' loading="lazy"></a>'
                     + '<figcaption>' + esc(item.get('caption', ''))
                     + ('<br>' + esc(item['credit']) if item.get('credit') else '')
                     + '</figcaption></figure>')
    return '<div class="process-image-grid">' + ''.join(cards) + '</div>' if cards else ''


def render_design_page(root, pattern, photos, inspiration):
    title = esc(pattern['title'])
    story = paragraphs(pattern.get('backstory', [])) or '<p>Backstory notes will be added here.</p>'
    references = image_cards(root, pattern, inspiration)
    inspiration_body = ('<div id="inspiration"><h3>Inspiration &amp; design artwork</h3>' + references + '</div>') if references else ''
    preview = esc(local_url(root, pattern, pattern['preview']))
    preview_dimensions = ''
    if pattern.get('preview_width') and pattern.get('preview_height'):
        preview_dimensions = f' width="{int(pattern["preview_width"])}" height="{int(pattern["preview_height"])}"'
    facts = [
        ('Machine', pattern['machine']),
        ('Design size', ' × '.join(str(x) for x in pattern['dimensions_mm']) + ' mm'),
        ('Hoop', '100 × 100 mm / 4 × 4 in'),
        ('Format', pattern['file_format']),
        ('Sewing points', f'{pattern["sewing_points"]:,}'),
        ('Thread loads', pattern['color_steps']),
    ]
    facts_html = '<dl>' + ''.join('<div><dt>' + esc(k) + '</dt><dd>' + esc(v) + '</dd></div>' for k, v in facts) + '</dl>'
    file_rows = []
    for item in pattern.get('file_overview', []):
        links = ' · '.join('<a href="' + esc(local_url(root, pattern, link['path'])) + '">' + esc(link['label']) + '</a>' for link in item.get('links', []))
        file_rows.append('<li><h3>' + esc(item['title']) + '</h3><p>' + esc(item['description']) + '</p><div class="file-links">' + links + '</div></li>')
    variants = []
    variant_ids = set()
    for item in pattern.get('variations', []):
        ident = item['id']
        if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', ident) or ident in variant_ids:
            raise ValueError('Invalid or duplicate variation ID')
        variant_ids.add(ident)
        if item.get('approved_for_publication') is not True:
            raise ValueError('Variation has not been selected for publication')
        zip_url = esc(local_url(root, pattern, item['download']))
        links = ' · '.join('<a href="' + esc(local_url(root, pattern, item[key])) + '">' + label + '</a>' for key, label in (
            ('machine_file', 'PES only'), ('source', 'Editable source'), ('instructions', 'Instructions')) if item.get(key))
        extra_preview = ''
        if item.get('preview') and item['preview'] != pattern['preview']:
            extra_preview = '<img class="variation-preview" src="' + esc(local_url(root, pattern, item['preview'])) + '" alt="' + esc(item.get('preview_alt', item['title'] + ' software preview')) + '" loading="lazy">'
        size = ' × '.join(str(x) for x in item['dimensions_mm']) + ' mm'
        variants.append('<article class="variation-card" id="variation-' + ident + '">'
                        + '<p class="eyebrow">' + esc(item['lettering']) + '</p><h4>' + esc(item['title']) + '</h4>'
                        + extra_preview + '<p>' + esc(item['description']) + '</p><p class="variation-size">' + esc(size) + '</p>'
                        + '<a class="button" href="' + zip_url + '">Download pattern ZIP <span aria-hidden="true">↓</span></a>'
                        + '<div class="file-links">' + links + '</div></article>')
    variations_html = '<div class="variation-grid">' + ''.join(variants) + '</div>' if variants else '<p>No variations have been shared yet.</p>'
    troubleshooting = ''.join('<details class="troubleshooting-note"><summary>' + esc(item['title']) + '</summary>'
                              + '<p>' + esc(item['body']) + '</p></details>' for item in pattern.get('troubleshooting', []))
    lessons = ''.join('<li><h4>' + esc(item['title']) + '</h4><p>' + esc(item['body']) + '</p></li>' for item in pattern.get('lessons_learned', []))
    physical_images = image_cards(root, pattern, photos) or '<p>No finished-piece photographs have been shared yet.</p>'
    page = f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="description" content="{esc(pattern['description'])} Backstory, files, finished embroidery and process notes.">
<title>{title} · Mara's Embroidery Library</title><link rel="stylesheet" href="../../styles.css"></head>
<body><a class="skip" href="#main">Skip to content</a>
<header class="wrap"><a class="brand" href="../../index.html"><span class="mark" aria-hidden="true">✳</span> Mara's Embroidery Library</a><nav aria-label="Main"><a href="../../index.html#collection">The collection</a><a href="../../index.html#finished-embroidery">Finished embroidery</a><a href="https://github.com/MaraAlexeev/embroidery-library">GitHub ↗</a></nav></header>
<main id="main" class="pattern-page">
<div class="pattern-heading wrap"><a class="back" href="../../index.html#collection">← Back to the collection</a><p class="eyebrow">{esc(pattern['category'])}</p><h1>{title}</h1><p class="intro">{esc(pattern['description'])}</p></div>
<nav class="page-nav wrap" aria-label="On this page"><a href="#backstory">Backstory</a><a href="#files">Files &amp; variations</a><a href="#finished-embroidery">Physical embroidery</a><a href="#process">Troubleshooting &amp; lessons</a></nav>
<section class="design-section wrap" id="backstory" aria-labelledby="backstory-title"><p class="eyebrow">01 / THE IDEA</p><h2 id="backstory-title">Backstory &amp; inspiration</h2><div class="backstory-layout"><div class="prose">{story}</div>{inspiration_body}</div></section>
<section class="design-section wrap" id="files" aria-labelledby="files-title"><p class="eyebrow">02 / THE PATTERN</p><h2 id="files-title">Files &amp; variations</h2>
<div class="file-overview"><figure class="process-image preview-image"><a href="{preview}"><img src="{preview}" alt="{esc(pattern['preview_alt'])}"{preview_dimensions} loading="lazy"></a><figcaption>Software stitch preview · colors and fabric are approximate.</figcaption></figure><div>{facts_html}<p class="file-summary">{esc(pattern.get('package_summary', ''))}</p><ul class="file-list">{''.join(file_rows)}</ul></div></div>
<div class="variations" id="variations"><h3>Design variations</h3><p class="prose">{esc(pattern.get('variations_note', 'Shared versions of this design.'))}</p>{variations_html}</div></section>
<section class="design-section wrap" id="finished-embroidery" aria-labelledby="finished-embroidery-title"><p class="eyebrow">03 / ON FABRIC</p><h2 id="finished-embroidery-title">Physical embroidery</h2><div class="prose">{paragraphs(pattern.get('physical_notes', []))}</div>{physical_images}</section>
<section class="design-section wrap" id="process" aria-labelledby="process-title"><p class="eyebrow">04 / FROM THE WORKTABLE</p><h2 id="process-title">Troubleshooting &amp; lessons learned</h2><div class="process-columns"><div><h3>Troubleshooting</h3>{troubleshooting or '<p>No troubleshooting notes have been recorded yet.</p>'}</div><div><h3>What changed along the way</h3><ul class="lesson-list">{lessons or '<li>Design-process notes will be added here.</li>'}</ul></div></div></section>
</main><footer class="wrap"><span>Made by Mara Alexeev with Codex</span></footer></body></html>
'''
    folder = root / 'docs/patterns' / pattern['id']
    (folder / 'index.html').write_text(page, encoding='utf-8')

    # A repository companion keeps the story and lessons readable on GitHub.
    md = '# ' + pattern['title'] + ' — design notes\n\n## Backstory and inspiration\n\n' + '\n\n'.join(pattern.get('backstory', [])) + '\n\n'
    for item in inspiration:
        md += '<img src="' + esc(str(PurePosixPath(item['src']).relative_to('patterns/' + pattern['id']))) + '" alt="' + esc(item['alt']) + '" width="560">\n\n' + esc(item.get('caption', '')) + '\n\n'
    md += '## Files and variations\n\n' + pattern.get('package_summary', '') + '\n\n'
    for item in pattern.get('variations', []):
        md += '### ' + item['title'] + '\n\n' + item['lettering'] + '. ' + item['description'] + '\n\n'
        for key, label in (('download', 'Download ZIP'), ('machine_file', 'PES'), ('source', 'Editable source'), ('instructions', 'Instructions')):
            if item.get(key):
                md += '[' + label + '](' + str(PurePosixPath(item[key]).relative_to('patterns/' + pattern['id'])) + ') · '
        md = md.removesuffix(' · ') + '\n\n'
    md += pattern.get('variations_note', '') + '\n\n## Physical embroidery\n\n' + '\n\n'.join(pattern.get('physical_notes', [])) + '\n\n'
    for item in photos:
        md += '<img src="' + esc(str(PurePosixPath(item['src']).relative_to('patterns/' + pattern['id']))) + '" alt="' + esc(item['alt']) + '" width="560">\n\n' + esc(item.get('caption', '')) + '\n\n'
    md += '## Troubleshooting\n\n'
    for item in pattern.get('troubleshooting', []):
        md += '### ' + item['title'] + '\n\n' + item['body'] + '\n\n'
    md += '## Lessons learned\n\n'
    for item in pattern.get('lessons_learned', []):
        md += '### ' + item['title'] + '\n\n' + item['body'] + '\n\n'
    (folder / 'DESIGN.md').write_text(md, encoding='utf-8')
