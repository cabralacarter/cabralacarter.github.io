# Carter Cabral website

Static GitHub Pages portfolio for **cartercabral.com**.

## Student resources

The student collection is a separate page at **/resources/**, linked from the
portfolio navigation and the home page. It includes all 16 supplied books,
topic filters, title/skill search, three suggested starting points, direct
PDF reading and downloads, cover images, and publisher attribution.

The page is usable without JavaScript; JavaScript adds search and filtering.
No accounts, online submissions, analytics, server, or package installation are required.

### Tiger Den equipment and documents

The page also includes equipment access information and five PDFs in
`resources/documents/`: the 3D printer and laser cutter request forms, the
printing materials guide, VR safety sheet, and Tiger Den technology overview.
Students bring completed forms to lab staff; the website does not submit forms.
Edit the equipment and document sections in `tools/build_resources.py`, then
rebuild the page. Lab hours and access information come from the supplied
Tiger Den Technology Overview and should be updated when lab arrangements change.

### Publishing this update

If these changes have not already been pushed to GitHub:

1. Open `cabralacarter.github.io` in GitHub Desktop. If needed, clone that
   repository first.
2. Choose **Repository > Show in Explorer**.
3. Copy this package's contents into that repository folder. Merge folders and
   replace the included `index.html` and `styles.css`. Keep `CNAME` as
   `cartercabral.com`.
4. Review the changes, commit them, and choose **Push origin**.
5. Wait for the existing GitHub Pages deployment to finish, then visit
   `https://cartercabral.com/resources/`.

Use GitHub Desktop or Git for this package: some PDFs exceed the browser
uploader's per-file limit. All included files are below GitHub's 100 MiB
regular Git file limit.

The TV QR code should point to the permanent page address:

`https://cartercabral.com/resources/`

Do not publish or print a QR promotion until that address opens successfully.

### Updating the collection

- The generated, deployable page is `resources/index.html`.
- Catalog titles, descriptions, topic tags, authors, and publisher links live
  in `resources/catalog.json`.
- File sizes, page counts, and asset verification information live in
  `resources/manifest.json`.
- PDF copies are in `resources/pdf/`; cover thumbnails are in
  `resources/covers/`.
- To rebuild the HTML after editing the catalog, run:

  ```sh
  python tools/build_resources.py
  ```

The builder uses Python's standard library. The published site does not
require Python. For new books, add the PDF, cover thumbnail, catalog entry,
and corresponding manifest entry before rebuilding. Match existing topic
keys, or add a topic to `TOPICS` in the builder.

## Credits and licenses

The website's book descriptions and interface are original. The books and
their cover artwork belong to their credited authors and Raspberry Pi Press.
Each supplied publication contains a Creative Commons
Attribution-NonCommercial-ShareAlike 3.0 notice, except where otherwise noted
within the publication. The books retain their original credits and notices.

License: https://creativecommons.org/licenses/by-nc-sa/3.0/

Cover thumbnails are resized renderings of each publication's first page.
Photographic PDF images have been optimized where that reduced download
size. Vector text and lossless line art were retained; every PDF's page count
and full extracted text were verified against the supplied original.
Modification and verification details are recorded in `resources/manifest.json`.
The 2024 handbook uses the publisher's smaller official PDF, verified to have
the same page count and extracted text as the uploaded copy.

Publisher information is linked on every book card. See each book for its full
author list and any material excluded from its general license.
