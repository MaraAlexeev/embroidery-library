"""Render the selected design pages, photographs and repository notes."""
from pathlib import Path, PurePosixPath
import html
import json
import re

START = '<!-- finished-embroidery:start -->'
END = '<!-- finished-embroidery:end -->'
EMPTY = 'No finished-piece photos have been shared yet.'
INSP_START = '<!-- inspiration:start -->'
INSP_END = '<!-- inspiration:end -->'


def collect_photos(root, patterns, field='finished_photos', folder='photos'):
    photos = []
    docs = (root / 'docs').resolve()
    for pattern in patterns:
        slug = pattern['id']
        if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', slug):
            raise ValueError('Invalid pattern slug')
        for photo in pattern.get(field, []):
            if photo.get('approved_for_publication') is not True:
                raise ValueError('Photo has not been selected for public sharing')
            src = photo['src']
            path = PurePosixPath(src)
            expected = ('patterns', slug, folder)
            if (path.parts[:3] != expected or len(path.parts) != 4
                    or not re.fullmatch(r'[a-zA-Z0-9][a-zA-Z0-9._-]*', path.name)
                    or path.suffix.lower() not in ('.jpg', '.jpeg', '.png', '.webp')):
                raise ValueError('Photo must be a local image in its design photos folder')
            file = docs / src
            if not file.is_file() or file.resolve() != file.absolute():
                raise ValueError('Photo is missing or uses a symlink: ' + src)
            if not isinstance(photo.get('alt'), str) or not photo['alt'].strip():
                raise ValueError('A photo needs descriptive alt text')
            for text_field in ('caption', 'credit'):
                if text_field in photo and not isinstance(photo[text_field], str):
                    raise ValueError('Photo ' + text_field + ' must be plain text')
            photos.append(dict(photo, pattern_id=slug, pattern_title=pattern['title']))
    return photos


def html_section(photos, prefix=''):
    cards = []
    for photo in photos:
        src = html.escape(prefix + photo['src'], quote=True)
        title = html.escape(photo['pattern_title'])
        pattern_url = html.escape(prefix + 'patterns/' + photo['pattern_id'] + '/', quote=True)
        caption = html.escape(photo.get('caption', ''))
        credit = html.escape(photo.get('credit', ''))
        dimensions = ''
        if photo.get('width') and photo.get('height'):
            dimensions = f' width="{int(photo["width"])}" height="{int(photo["height"])}"'
        cards.append(
            '<figure class="finished-photo"><a class="finished-photo-image" href="' + src + '">'
            '<img src="' + src + '" alt="' + html.escape(photo['alt'], quote=True) + '"' + dimensions + ' loading="lazy">'
            '</a><figcaption><a class="finished-photo-title" href="' + pattern_url + '">' + title + '</a>'
            + ('<p>' + caption + '</p>' if caption else '')
            + ('<p class="photo-credit">Photo: ' + credit + '</p>' if credit else '')
            + '</figcaption></figure>')
    content = '<div class="finished-photo-grid">' + ''.join(cards) + '</div>' if cards else '<p class="photo-empty">' + EMPTY + '</p>'
    return (START + '\n<section class="finished-embroidery wrap" id="finished-embroidery" aria-labelledby="finished-embroidery-title">'
            '<p class="eyebrow">ON FABRIC</p><h2 id="finished-embroidery-title">Finished embroidery</h2>'
            '<p class="photo-intro">Photographs of completed pieces, shared alongside their patterns.</p>'
            + content + '</section>\n' + END)


def markdown_photos(photos, prefix):
    # HTML inside Markdown keeps alt text and captions safe and predictable on GitHub.
    if not photos:
        return EMPTY
    rows = []
    for photo in photos:
        rows.append('<img src="' + html.escape(prefix + photo['src'], quote=True)
                    + '" alt="' + html.escape(photo['alt'], quote=True) + '" width="560">\n\n'
                    + '<strong>' + html.escape(photo['pattern_title']) + '</strong>'
                    + (' — ' + html.escape(photo['caption']) if photo.get('caption') else '')
                    + ('<br>Photo: ' + html.escape(photo['credit']) if photo.get('credit') else ''))
    return '\n\n'.join(rows)


def replace_section(path, section, start=START, end=END):
    text = path.read_text(encoding='utf-8')
    if text.count(start) != 1 or text.count(end) != 1:
        raise ValueError('Expected exactly one finished-photo section in ' + str(path))
    before, rest = text.split(start)
    _, after = rest.split(end)
    path.write_text(before + section + after, encoding='utf-8')


def render(root):
    from render_design_pages import render_design_page
    patterns = json.loads((root / 'docs/catalog.json').read_text(encoding='utf-8'))['patterns']
    photos = collect_photos(root, patterns)
    inspiration = collect_photos(root, patterns, 'inspiration_images', 'inspiration')
    replace_section(root / 'docs/index.html', html_section(photos))
    photo_links = ' · '.join('[' + p['title'] + '](docs/patterns/' + p['id'] + '/photos/)' for p in patterns)
    replace_section(root / 'README.md', START + '\n## Finished embroidery\n\n'
                    + 'Photographs of the physical pieces, separate from the software previews.\n\n'
                    + markdown_photos(photos, 'docs/')
                    + '\n\n[View the finished embroidery section](https://maraalexeev.github.io/embroidery-library/#finished-embroidery).'
                    + '\n\nPhoto folders: ' + photo_links + '. '
                    + 'See [FINISHED_EMBROIDERY.md](FINISHED_EMBROIDERY.md) for adding selected photographs.\n' + END)
    replace_section(root / 'README.md', INSP_START + '\n## Inspiration and design artwork\n\n'
                    + markdown_photos(inspiration, 'docs/')
                    + '\n\nReference artwork is labeled separately from physical embroidery.\n' + INSP_END,
                    INSP_START, INSP_END)
    for pattern in patterns:
        selected = [photo for photo in photos if photo['pattern_id'] == pattern['id']]
        folder = root / 'docs/patterns' / pattern['id']
        references = [photo for photo in inspiration if photo['pattern_id'] == pattern['id']]
        render_design_page(root, pattern, selected, references)
        photo_folder = folder / 'photos'
        photo_folder.mkdir(exist_ok=True)
        (photo_folder / 'README.md').write_text(
            '# ' + pattern['title'] + ' — finished embroidery\n\n'
            + 'Photographs of completed physical embroidery belong in this folder.\n\n'
            + markdown_photos(selected, '../../../')
            + '\n\nOnly owner-selected photos are published. Add approved photos to this design’s '
            + '`finished_photos` list in [catalog.json](../../../catalog.json), then follow '
            + '[the photo guide](../../../../FINISHED_EMBROIDERY.md).\n', encoding='utf-8')
    print('Rendered media sections for ' + str(len(patterns)) + ' designs; ' + str(len(photos)) + ' photos and ' + str(len(inspiration)) + ' artwork images.')


if __name__ == '__main__':
    render(Path(__file__).resolve().parent)
