# Publishing selected embroidery designs

Publish a design only after the owner explicitly selects it for public sharing. Selection does not authorize sharing other designs or automatically publishing later revisions.

1. Work in this separate collection. Never initialize or publish the parent working folder.
2. Copy only individually reviewed files for the selected design. Inspect filenames, SVG metadata, previews, text, and every ZIP member for personal content or private links.
3. Inspect the actual PES start, every color entry and trimmed restarts. Preserve intentional anchors and trims. Document physical sew-out evidence separately from software checks. Preserve a successfully sewn original when the owner requests it.
4. Keep the numbered thread sequence, dimensions, testing notes, individual files and ZIP consistent. Use distinct filenames for stitch revisions; do not silently replace preserved originals.
5. Add only the reviewed paths and SHA-256 hashes to `PUBLIC_FILES.json` and the corresponding exact paths to `.gitignore`. Run `python3 check_publication.py` before uploading. The manifest is a review aid, not a privacy scanner.
6. Inspect the complete proposed upload. Push only this collection. GitHub Pages serves `main` → `/docs`; it contains no connection to the private working collection.
7. Verify the live design pages and downloads after publishing.

## Design pages and variations

Follow [DESIGN_PAGES.md](DESIGN_PAGES.md) to maintain backstories, file overviews, physical observations and process lessons in the catalog. Add separately selected variations with distinct files and their own instructions. Rebuild the static pages with `python3 render_finished_photos.py`.

## Finished-piece photos

Use the dedicated [finished embroidery workflow](FINISHED_EMBROIDERY.md) for photographs. Only photos explicitly listed in a design's `finished_photos` catalog entries are rendered. A successful sew-out report alone is not a photograph. Adding photos never re-exports a PES file or automatically updates its testing status.

## Integrating a personal website later

Use `docs/catalog.json` as the public content catalog. Resolve its relative URLs against the catalog URL. Design pages use `patterns/<slug>/`; images and download files live beside each page. Keep these slugs stable. The personal website can use the preview, title, description and testing status while linking to the canonical design page or download. No personal-website changes are made by this repository.

GitHub Pages setup: Settings → Pages → Deploy from a branch → main → /docs.
