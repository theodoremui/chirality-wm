# Rendering repair and verification

The seven proposals now have [formatted HTML and PDF reading editions](../rendered/index.html). The canonical Markdown files remain in `docs/ideas-codex/`. This repair changes presentation and file references; research designs, scores, and empirical claims are preserved.

## What was repaired

| Problem | Repair |
|---|---|
| Links still used the former `ideas-claude` and `research-claude` folder names | Updated active proposal, review, index, and validation references to the current `ideas-codex` and `research-codex` folders. |
| The pipeline image pointed to an unavailable SVG path | Markdown now embeds the PNG preview and provides an explicit editable SVG link. HTML embeds the SVG directly; PDF preserves its vector paths and selectable labels. |
| Mathematical expressions used incompatible delimiters or code formatting | Standardized inline and display math, converted code-formatted formulas to TeX, and retained literal tensor shapes as code. Checked derivatives, units, powers, subscripts, and set notation. |
| A table contained an unescaped absolute-value delimiter | Replaced the delimiter with mathematical absolute-value notation so all rows retain two columns. |
| A long equation overflowed on a narrow display | Split the equation into aligned rows without changing its meaning. |
| Print layout could leave the pipeline heading apart from its figure | Kept heading and artwork together on a dedicated landscape page. |
| Supporting-file links in exported PDFs were machine-specific | Rewrote local PDF links relative to the PDF directory, preserving portability with the research folder. |

Only version 7 contains an embedded illustration; versions 1–6 have no missing figure references. The shared research index also shows the repaired pipeline preview. Earlier versions retain their own methods and protocol decisions, so the final pipeline has not been inserted into versions where it could misrepresent the earlier design.

## Verification

All seven reading editions were opened in an isolated Chrome session with HTTP(S) requests blocked. Fonts, MathML, and figures are embedded, so reading does not depend on a network connection or a third-party math service. Desktop checks used a 1280-pixel viewport; narrow-screen checks used 390 pixels.

The automated [render audit](render-audit.json) records loaded images, parsed mathematics, table column counts, browser errors, overflow, source hashes, and PDF page properties. It found no unloaded images, MathML errors, raw dollar delimiters, external rendering resources, horizontal page overflow, replacement glyphs, or text outside PDF page bounds. Both tables retain their expected column counts. A separate [package audit](package-audit.json) checked all 64 local HTML links, verified navigation from the seven-card reading index, and confirmed that the historical snapshot is unchanged. Artifact validation checked 98 local Markdown links.

The seven PDFs contain 32 pages in total: 3, 4, 4, 4, 5, 5, and 7 pages for versions 1–7. Every page was rasterized and reviewed through contact sheets; equations, the two tables, and the landscape figure received additional full-page inspection. The pipeline PDF page contains vector artwork rather than a raster screenshot. Page previews and browser screenshots are retained in `qa/`.

| Version | Visual record |
|---|---|
| 1 | [All pages](qa/v01-contact-sheet.png) |
| 2 | [All pages](qa/v02-contact-sheet.png) |
| 3 | [All pages](qa/v03-contact-sheet.png) |
| 4 | [All pages](qa/v04-contact-sheet.png) |
| 5 | [All pages](qa/v05-contact-sheet.png) |
| 6 | [All pages](qa/v06-contact-sheet.png) |
| 7 | [All pages](qa/v07-contact-sheet.png), [vector figure page](qa/v07-page-03.png) |

Use HTML in a current browser or PDF for reliable mathematical formatting. Markdown math support varies by viewer. Local supporting-document links require the folder structure to accompany the PDFs; external literature links still require internet access. No claim is made that every Markdown editor or PDF viewer was tested.

## Preservation and reproduction

The [pre-repair archive](pre-rendering-repair.tar.gz) and [SHA-256 manifest](pre-repair-manifest.json) preserve the prior files. The historical review snapshot was left unchanged, including its old paths. Review-era hashes refer to the reviewed scientific text; current hashes appear in the render audit and [artifact validation](../artifact-validation.json).

`build_reading_copies.py` builds and checks the editions from the canonical Markdown sources. It requires Pandoc, Python with `playwright`, `pymupdf`, and `pillow`, Chrome, and the macOS STIX Two fonts. The executable and font locations are explicit in the script. No user browser profile is used. `reader.css` controls screen and print typography. `normalize_math.py` records the one-time initial typography conversion; ongoing builds do not run it.

From the repository root, with those dependencies installed:

```sh
python output/research-codex/rendering/build_reading_copies.py
python output/research-codex/checks/validate_artifacts.py
```

The repair was verified with Pandoc 3.10.2, Playwright 1.64.1, PyMuPDF 1.28.2, and Pillow 12.3.0. The isolated Python environment used for this session was `/tmp/chirality-render-venv`; it is not required when the dependencies are installed elsewhere.
