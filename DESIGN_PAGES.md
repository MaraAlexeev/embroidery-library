# Design pages

Each design page opens with a two-column comparison: inspiration on the left and the finished embroidery photograph on the right. The images stay in this order on narrow screens. If no physical photograph is available, the right side uses a clearly labeled software preview; missing inspiration gets a short text notice. Images retain their complete contents without cropping.

The landing page shows only the collection, without a physical-photo gallery or preparation section.

Below the comparison, each design page and its `DESIGN.md` companion follow the same order:

1. Backstory and inspiration, including approved reference or concept images when available.
2. File overview and design variations, with a software preview, dimensions and downloads.
3. Physical embroidery, with completed-piece photos and recorded sewing observations.
4. Troubleshooting and lessons from the design process.

The content lives with each pattern in `docs/catalog.json`. Run `python3 render_finished_photos.py` to rebuild the design pages, design notes and photo sections. This command does not alter embroidery files or ZIP packages. Review changes and refresh the exact paths and hashes in `PUBLIC_FILES.json` before publication.

## Content fields

- `backstory`: an ordered list of plain-text paragraphs based on the saved design history. Do not invent personal motives or undocumented outcomes.
- `inspiration_images`: approved references, redraws or concept artwork. Label each accurately and include known attribution. See the [image guide](FINISHED_EMBROIDERY.md).
- `package_summary` and `file_overview`: descriptions of the actual downloadable files. Each file-overview item has a `title`, `description`, and `links` containing `label` and catalog-relative `path`.
- `physical_notes` and `finished_photos`: observations and photographs of sewn pieces. Distinguish a photograph from a documented test of a particular file, machine setup or wash cycle.
- `troubleshooting` and `lessons_learned`: lists of objects with plain-text `title` and `body`. Separate practical advice from changes actually made and results actually reported.
- `variations` and `variations_note`: separately selected versions of the same design, such as with text, without text, different sizes or different hoop placements.

## Adding a variation

Publish a variation only after it is selected for sharing. Preserve existing files and URLs. Give the new version its own folder or distinct filenames, README, ZIP, preview, dimensions and testing notes. Apply the embroidery export checks to any new or re-exported machine file.

Each variation contains these fields:

```json
{
  "id": "without-text",
  "title": "Original — without text",
  "lettering": "No text",
  "description": "Describe what this version contains and how it differs.",
  "dimensions_mm": [72.8, 49.8],
  "download": "patterns/waggle-dance/Waggle-Dance-PES.zip",
  "machine_file": "patterns/waggle-dance/Waggle-Dance-v1.pes",
  "source": "patterns/waggle-dance/Waggle-Dance-editable.svg",
  "instructions": "patterns/waggle-dance/README.txt",
  "preview": "patterns/waggle-dance/Waggle-Dance-preview.png",
  "preview_alt": "Describe this version's software preview.",
  "approved_for_publication": true
}
```

Use a unique, stable `id`. Only `download`, `machine_file`, `source`, `instructions` and `preview` paths belonging to this design are accepted. A differing variation preview appears on its card. Omit optional source, instructions or preview fields if unavailable; the ZIP is required. Do not add a “with text” download until that version actually exists and has been selected. The current pages explicitly say when only one version has been shared.

The catalog can also supply the same sections to a future personal website. Resolve media and file paths relative to the catalog URL and retain the distinction between concept artwork, stitch previews and physical photographs.
