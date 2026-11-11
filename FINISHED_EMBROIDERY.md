# Finished embroidery photographs

Use this section for photographs of real completed embroidery. Keep software previews, concept artwork and generated mockups in their existing preview roles.

- [Waggle Dance photo folder](docs/patterns/waggle-dance/photos/)
- [Navier–Stokes photo folder](docs/patterns/navier-stokes/photos/)
- Website photos: [Waggle Dance](https://maraalexeev.github.io/embroidery-library/patterns/waggle-dance/#finished-embroidery) · [Navier–Stokes](https://maraalexeev.github.io/embroidery-library/patterns/navier-stokes/#finished-embroidery)

## Adding a photograph

1. Select the exact photo for public sharing. Approval to share a pattern does not automatically approve every photograph of it. Check for personal names, identifiable people and private details in the image; remove location metadata from the public copy.
2. Save the selected public copy as JPEG, PNG or WebP in `docs/patterns/<design-id>/photos/`, with a simple descriptive filename. Preserve the original photo privately.
3. Add an entry to that design’s `finished_photos` array in `docs/catalog.json`. Paths are relative to the catalog. Supply accurate alt text, an optional caption, and credit when known and intended for publication. Do not invent fabric details, dates or photographer names.

```json
{
  "src": "patterns/waggle-dance/photos/finished-piece-01.jpg",
  "alt": "Three embroidered honeybees and their looping trail on blue fabric",
  "caption": "Completed Waggle Dance embroidery",
  "approved_for_publication": true
}
```

This is an example entry, not a photo currently in the collection. Optional `credit` is plain text.

4. Run `python3 render_finished_photos.py`. This updates complete design pages and their DESIGN.md companions, the repository README, and photo-folder READMEs from the explicit catalog entries. The design-page structure is documented in [DESIGN_PAGES.md](DESIGN_PAGES.md). It never searches for or imports photographs from the working collection. Empty lists display a short “no photos shared yet” message, without broken image placeholders. The landing page contains only the collection; photos stay on the design pages and in the repository.
5. Review the generated pages and captions. Add the exact image paths to `.gitignore` exceptions and `PUBLIC_FILES.json`; update hashes for the changed pages and catalog, then run `python3 check_publication.py`. Publish only the reviewed files and verify the live pages.

Photos live alongside the design pages and are separate from the machine-file ZIP packages. Adding a photo does not change a PES file or its testing status. Update testing notes only when there is actual evidence for the specific file version.

## Personal website integration

Each public pattern’s `finished_photos` list is available in `docs/catalog.json`. A future personal website can show those photographs when the list is nonempty and omit the image gallery when empty. Resolve `src` relative to the catalog URL. Retain captions and intended credits, and distinguish photographs from the design’s software preview.

## Inspiration and design artwork

The separate `inspiration_images` array uses the same fields and explicit selection rule, with images in `docs/patterns/<design-id>/inspiration/`. The renderer shows these on the design page and in the repository README when available. Captions must identify original references, redraws and concept artwork accurately. Include known source attribution; do not present a recreated drawing as the original inspiration image or as a photograph of a finished piece.
