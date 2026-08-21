# CLAUDE.md

> **Lecture styling is not defined here.** The WebR side-by-side layout, code
> block width and size, the figure canvas and theme, the KaTeX pinning and the
> transcript panels are shared by every course and are documented once in
> [`../_lecture-shared/RULES.md`](../_lecture-shared/RULES.md). The files
> themselves live in `_lecture-shared/` and are copied in by
> `../sync-lecture-shared.sh`; the copies under `lectures/` are generated, so
> edit the shared originals and run the sync. `./sync-lecture-shared.sh --check`
> reports drift.

Course website for **AECN 896-05, Data Science with R**, built with Quarto and
published to GitHub Pages.

## Layout

| Path | What it is |
|---|---|
| `_quarto.yml` | Website config. `output-dir: docs`, render list is `*.qmd` only |
| `lectures/Chapter-N-*/` | Lecture decks, `NN-N-topic.qmd`, `format: revealjs` |
| `lectures/custom.scss` | Shared theme for every deck. Read it before styling anything |
| `lectures/transcript-support.html` | Shared CSS+JS for lecturer transcripts |
| `exercises/`, `assignments/`, `syllabus/` | Course material |
| `docs/` | **Generated output. Never edit or store files here** |

`docs/` is rebuilt from scratch by a full render. Anything you write there is
destroyed. Put notes and docs anywhere else.

## Rendering

```bash
quarto render                                              # whole site, 51 files, several minutes
quarto render lectures/Chapter-2-Quarto/02-2-Quarto-revealjs.qmd   # one deck, much faster
```

Render a single deck while iterating. Only do a full render when you need it.

## Previewing a revealjs deck

Opening a rendered deck through `file://` shows a **blank deck with only the
footer and logo**. reveal.js loads as ES modules and CORS blocks module imports
from `file://` origins. Serve it over HTTP instead:

```bash
cd docs && python3 -m http.server 8899
# http://localhost:8899/lectures/Chapter-2-Quarto/02-2-Quarto-revealjs.html
```

`quarto preview <file>.qmd` also works. For screenshotting decks in headless
Chrome, which has its own traps, see
[.claude/docs/revealjs-preview.md](.claude/docs/revealjs-preview.md).

## Decks that run code in the browser (WebR)

Some decks (e.g. `03-3-reshape-merge.qmd`) declare a `webr:` block and use
`{webr-r}` cells, which students execute in the browser. **Those cells do not use
the local R library.** WebR v0.4.0 pulls its own wasm builds from
`repo.r-wasm.org`, so "it works on my machine" proves nothing about what a
student sees. Check the version students actually get:

```bash
curl -s https://repo.r-wasm.org/bin/emscripten/contrib/4.4/PACKAGES \
  | awk '/^Package: dplyr$/{f=1} f&&/^Version:/{print $2; f=0}'
```

Adding a package to a deck means adding it to that deck's `webr: packages:` list,
and every package is downloaded in the student's browser on first run — a WebR
cell can take **minutes** to become interactive. Budget for that when testing
headlessly; a 9-second wait is not enough.

**Never put a credential in a `#| context: setup` webR chunk.** Its source is
embedded in the rendered HTML so the browser can execute it, which means anything
in it is published. `L06` carried a live USDA-NASS API key there and it reached the
public course website. An `{r}` chunk with `include: false` really does stay out of
the output; a webR `context: setup` chunk does not, and the two look alike. Read
keys from `Sys.getenv()` or `keyring::key_get()` instead.

**`r.spatial.workshop.datasets` is `LazyData: true`, so a missing `data()` call
is not a bug.** Every dataset in it resolves by name the moment the package is
attached — `terra::rast(prism_saunders)` works with no `data(prism_saunders)`
anywhere. This holds **in WebR too**, verified in the browser by evaluating
`dim(prism_us)` on a deck that never loads `prism_us`: it returned `281x125`.

Worth stating because the opposite is easy to assume. Several Chapter 9 decks use
a dataset "before" its `data()` call, which looks exactly like the load-order bug
it is not. If you think you have found one, check `DESCRIPTION` for `LazyData`
before writing it up.

What *does* still deserve a look in a `#| context: setup` chunk: all cells share
one R session, so anything setup genuinely fails to create is missing everywhere,
and the deck still renders perfectly — that class of failure exists only in the
browser.

## Traps that have already cost time

1. **Raw HTML above the first `##` becomes its own untitled slide.** A `<style>`
   block, a `<script>`, or even a long HTML comment placed between the YAML
   header and the first heading is emitted as slide content, producing a blank
   slide students page through. Put deck-level CSS/JS in a file referenced by
   `include-in-header:` instead.

   *Known instance:* `02-2-Quarto-revealjs.qmd` has such a blank slide, caused by
   its "REVISED VERSION" change-log comments. Removing those comments removes the
   slide.

2. **`custom.scss` styles bare `details` and `summary`.** The `// Answer box`
   block (`lectures/custom.scss`, ~line 195) applies a grey `1px solid #aaa`
   border plus padding to *every* `<details>`, and a negative margin to every
   `<summary>`. It is live — it styles Quarto's `<details class="code-fold">`
   blocks. Do not change it. Any new `<details>` must opt out explicitly.

3. **Slide space is tight.** reveal's logical slide is 700px tall. Several slides
   already sit near or over that. Anything added to normal flow costs that space
   on every slide, whether or not it is used. Measure before adding furniture.

4. **Two YAML-looking blocks per deck.** Lecture decks teach Quarto, so they
   contain sample YAML in verbatim blocks that looks exactly like the real
   header. When editing the real header, match on a unique line (e.g. `logo:`)
   so you do not edit the teaching example by mistake.

5. **Never pipe `quarto render`.** `quarto render 2>&1 | tail -6` reports
   `tail`'s exit code, not quarto's, so a render that halted partway looks like
   a success. This has already caused a partial build (28 of 41 files) to be
   reported as complete. Redirect instead, then read the code:

   ```bash
   quarto render > /tmp/render.log 2>&1; echo "EXIT: $?"
   find docs -name '*.html' | wc -l     # expect 52
   ```

6. **This repo lives in Dropbox, and Dropbox fights Quarto's cache.** There are
   `conflicted copy` files inside `.quarto/` — including of
   `project-cache/deno-kv-file-shm`, which is a live database Quarto writes
   during a project render. Symptoms are weird, non-reproducible, and *not* your
   edits: a traceback naming a file that has never existed in this repo, or
   `ERROR: NotFound ... rename '<file>.html' -> 'docs/<file>.html'` at the final
   move step. A single-file render of the same deck then succeeds.

   Before blaming a `.qmd`, check `find .quarto -name "*conflicted*"`, and
   confirm the deck renders alone. Excluding `.quarto/` from Dropbox sync would
   remove the whole class of failure — not done, as it changes the user's
   Dropbox setup.

7. **`webr::install(repos = ...)` searches only the repos you name.** It does
   not fall back to the main webR repo for *dependencies*. Ten decks installed
   `r.spatial.workshop.datasets` from the custom repo alone; that package
   declares `Imports: sf`, `sf` is not in the custom repo, and the install then
   hung forever. The failure is silent from the slide's point of view — the
   setup chunk never finishes, so `county_yield` never exists and **every**
   webr cell on the deck does nothing when a student clicks Run. Always pass
   both:

   ```r
   webr::install(
     "r.spatial.workshop.datasets",
     repos = c("https://tmieno2.github.io/rwasm-package/repo",
               "https://repo.r-wasm.org")
   )
   ```

   Two things that wasted time diagnosing this:

   - The webr status line reads `Evaluating hidden code cell...` and **never
     resets, even on success**. It is not an idle signal. Judge readiness by
     whether a cell actually produces output.
   - 404s on `<pkg>.data` / `<pkg>.js.metadata` are **normal**. webR probes an
     older layout before falling back to `.tgz`. The official repo returns the
     same 404s for `MASS`, `Matrix`, `mgcv` and friends, which install fine.
     Do not conclude from them that a repo is half-published.

   **Chapter 4 no longer needs this**, because it no longer needs `sf`. See
   below. Chapter 9 does, and its decks still pass both repos.

8. **A nested ```` ```{r} ```` runs unless the OUTER fence is `{verbatim}`.**
   knitr finds chunks by scanning for ` ```{...} ` line by line. It does not
   understand that a fence can sit inside another fence, so an example chunk
   shown to the reader is executed like any other. ` ````markdown ` does not
   help; only the `verbatim` engine does, and the outer fence needs more
   backticks than the inner one:

   `````markdown
   ````{verbatim}
   ```{r}
   plot(x)
   ```
   ````
   `````

   This matters because these decks *teach Quarto*, so they are full of example
   chunks. Two ways it has already bitten:

   - **The render dies.** The example refers to objects and packages the
     document never loads, so you get `could not find function "modelsummary"`
     pointing at a chunk you were only ever showing. This is why
     `exercises/7-1-date.qmd` sat in the `_quarto.yml` exclusion list, unseen by
     students, until 2026-08-17.
   - **Worse, the render succeeds.** If the example happens to be valid code, it
     runs, and the block you meant to display is *replaced by its output* or
     silently swallowed. `6-1-project-organization.qmd` shipped with an entire
     RStudio snippet definition missing from the page and no error anywhere.

   A checker exists. Run it before any render that touches a qmd containing
   example chunks:

   ```bash
   python3 .claude/scripts/check-verbatim-fences.py
   ```

   Exit code 1 means it found something. It scans every `.qmd`/`.rmd` outside
   `docs/`, so it is cheap enough to run every time.

## Two dataset packages, and which to use

| Package | Contents | Deps | Size | Used by |
|---|---|---|---|---|
| `r.spatial.workshop.datasets` | ~30 `sf`/`stars` datasets | `sf` | 9.5 MB | Chapter 9 |
| `r.workshop.datasets` | `county_yield` only, no geometry | none | 35 KB | Chapter 4 |

Both live in the same repo, `https://tmieno2.github.io/rwasm-package/repo`.
Because `r.workshop.datasets` has no dependencies, one repo is enough for it —
the trap above does not apply. Chapter 4 loads it as:

```r
webr::install("r.workshop.datasets", repos = "https://tmieno2.github.io/rwasm-package/repo")
data(county_yield, package = "r.workshop.datasets")
```

Use the spatial package only when a deck actually needs geometry. Pulling in
`sf` costs the student eleven extra downloads (`class`, `proxy`, `e1071`,
`KernSmooth`, `classInt`, `DBI`, `Rcpp`, `wk`, `s2`, `units`, `sf`) before any
cell can run.

Source of the small package: `~/Dropbox/R-Package/r.workshop.datasets`. Its
`data-raw/build-wasm.R` rebuilds the WebR binary **without Docker** — the
package is data only, so a local `R CMD INSTALL` produces an
architecture-independent tree and only `rwasm::add_tar_index(strip = 1)`, which
is pure R, is wasm-specific. A package with compiled code still needs the Docker
route in `rwasm-instruction.qmd`.

Note `county_yield` is also loaded from the **spatial** package by
`08-2-modelsummary.qmd` and `exercises/4-2-*.qmd`, but through r-universe rather
than WebR, so they are unaffected. `r.workshop.datasets` is not on r-universe.

## Deck status: check this before asking "is X done yet?"

[.claude/data/lecture-status.json](.claude/data/lecture-status.json) records, for
every deck in `lectures/`, where it stands on three axes:

| Axis | Means |
|---|---|
| `transcripts` | Collapsible lecturer transcript panels |
| `notebook_theme` | `notebook.scss` present in the deck's `theme:` list |
| `side_by_side_output` | Explicit `::: {.side-out}` code-left/output-right regions |

Each axis carries a `status` (`complete`, `partial`, `not_started`,
`not_applicable`) plus `notes` saying why, and countable evidence — transcript
count, cell counts, `.side-out` region counts.

**The counts are generated. The statuses are not.** After any substantial deck
edit, refresh it:

```bash
python3 .claude/scripts/refresh-lecture-status.py            # rewrite
python3 .claude/scripts/refresh-lecture-status.py --check     # exit 1 on drift
```

The script recounts from source and writes every mechanical field, while
preserving `title`, `chapter`, `on_website`, and every `status`/`notes` you
edited by hand. A deck new to `lectures/` is added with `status: unknown` on all
three axes and reported on stderr — set those by hand. Finishing a rollout on a
deck means editing its `status` in the same change that edits the deck; the
script cannot infer intent, only counts.

Two things the counts do **not** mean:

- `side_out_regions: 0` does not mean the deck has no side-by-side cells.
  `custom.scss` gives every WebR cell that draws a plot a two-column layout
  automatically. `.side-out` is the explicit opt-in for the rest.
- A cell count only counts cells that actually run. Chunks nested inside a
  `{verbatim}` fence are teaching examples and are excluded (see trap 8).

## Transcripts

Decks can carry collapsible "Transcript" panels — what the lecturer
says, written out, hidden behind a pill in the slide corner and revealed on
click. **All nine chapters are done: 706 transcripts across 24 decks.**

Full design, conventions, writing style, and rollout status:
[.claude/docs/lecture-transcripts.md](.claude/docs/lecture-transcripts.md)

To replicate this system in a **different** course project, hand that project's
agent [.claude/prompts/replicate-transcripts.md](.claude/prompts/replicate-transcripts.md).
Copy the whole file — it is nothing but the prompt. Its reference paths are
absolute and assume this repo stays at
`/Users/tmieno2/Dropbox/TeachingUNL/Data-Science-with-R-Quarto`; update them if
it moves.

## Rule: anything meant to be copied must be copiable

When producing a prompt, a config block, a command, or any other artifact whose
purpose is to be pasted somewhere else:

- **In chat**, put it in a single fenced code block, so it can be copied in one
  action. If the content itself contains fences, wrap it in a four-backtick
  fence. Do not render it as prose, tables, or nested formatting the user has to
  reassemble by hand.
- **On disk**, give it its own file containing nothing but the artifact. Keep
  commentary about it in `CLAUDE.md` or a doc, not in the file itself.

`.claude/prompts/` holds these. Everything in that directory is a pure,
copy-whole-file artifact.
