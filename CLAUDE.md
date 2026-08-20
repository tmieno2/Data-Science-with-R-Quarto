# CLAUDE.md

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
quarto render                                              # whole site, 41 files, several minutes
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

## Code blocks have one fixed width

**Generic rule, all code blocks, every deck.** A code block's width is a
property of the slide, not of its content or its state. It must not change
because a cell was run, because output arrived, because the cell went side by
side, or because the code in it is short. Every code block on a slide is the
same width as every other one — `$nb-code-w`, currently 90%, which is what
`custom.scss` gives `.qwebr-interactive-area` and what `notebook.scss` gives
`div.cell-output > pre`.

Going side by side changes how a cell is **divided**, never how wide it is. Two
violations have already been fixed and must not come back:

- `notebook.scss` set `.side-out .qwebr-interactive-area` to `width: 100%`,
  overriding the 90% cap, so a promoted cell grew wider than its neighbours the
  moment it was promoted.
- `webr-layout.html` re-split the tracks proportionally once output arrived, so
  the editor jumped to a new width on the student's first Run.

When adding any rule that sets a width on a code block, ask what it looks like
next to an unrun cell of the same deck. If the answer is "different", it is
wrong.

## WebR code/output layout in lecture slides

**Permanent rule. This governs every lecture deck, now and in future.**

Lecture decks use an *adaptive* side-by-side layout for suitable WebR cells. The
shared implementation lives in two files:

| File | Role |
|---|---|
| `lectures/webr-layout.html` | Measures code and output and selects the layout |
| `lectures/notebook.scss` | Defines the side-by-side grid and the visual styling |

### Every WebR deck must include the script

Every lecture deck containing a `{webr-r}` block must include
`../webr-layout.html` under revealjs `include-in-header`. If the deck also uses
`transcript-support.html`, use a YAML list containing both files:

```yaml
format:
  revealjs:
    include-in-header:
      - ../transcript-support.html
      - ../webr-layout.html
```

Without the script the SCSS still renders, but its custom properties fall back
to their static defaults (`5fr`/`7fr`, banner offset `41.667%`) and nothing
adapts. A deck that gains its first `{webr-r}` cell gains this include in the
same edit.

### No fixed 50/50 split

Do not assign a fixed 50/50 code/output split. The adaptive script measures the
code using its actual rendered font, reserves the remaining width for output,
and remeasures console output after execution. The output column may receive up
to **82%** of the available width. Its `Output` banner and output body must fill
the same grid track and therefore have exactly the same width.

The split is carried by three custom properties that `webr-layout.html` sets on
the host element and `notebook.scss` consumes: `--webr-code-track`,
`--webr-output-track`, `--webr-code-share`, and `--webr-gutter-centre` (an exact
pixel that centres the caret in the 1rem gutter — the percentage above resolves
against a different box than the grid tracks do and lands ~7px off). Code share
is clamped to 18–58%, so output lands between 42% and 82%. The 18% floor exists
only to keep the editor usable: a one-line call such as `class(mtcars)` measures
160px including Monaco's gutter, and the old 30% floor padded it to 329px,
charging the difference to the output for nothing.

**The code column is set once and never moves.** Its width comes from measuring
the code — the editor's rendered glyphs, plus Monaco's chrome, plus slack — and
nothing after that changes it. The output then gets whatever is left, and the
only decision made once output exists is binary: it either fits in the remaining
space or the cell stacks. The code column is never narrowed to make room.

This is invariants 1 and 2, and it is also a hard usability rule: **a code block
on a lecture slide must not change width when the student presses Run.** An
earlier version re-split the tracks proportionally between the measured code and
the measured output once output arrived, which made the editor visibly jump on
every first run. Do not reintroduce any post-run `setTracks()`.

**A too-narrow code column is self-reinforcing, so the fallbacks must err wide.**
Monaco wraps a line it cannot fit, and a wrapped line measures narrower still —
nothing downstream can recover the true width once that happens. Two guards:
the rendered-code measurement retries for 10s (2s was not enough on a ~70-cell
deck, and giving up left every cell on the fallback), and the fallback itself is
pixels against the cell's real width (`maxChars * 10 + 90`) rather than the old
`(maxChars + 10) / 145`, which assumed ~145 characters span the full width when
the real figure is ~109 and so under-sized every editor by a third. Always
measure the SOURCE text, never the rendered `.view-line` elements — once wrapped
those hold fragments, and measuring them confirms the mistake instead of
correcting it. This bites manual `::: {.side-out}` cells hardest: they open side
by side immediately and never reach the measured split until they are run.

Do not measure the output with `pre.scrollWidth`. `notebook.scss` gives that
`pre` `width: 100%`, so its scrollWidth reports the track it is sitting in
rather than the text inside it. Reading it back is a feedback loop: every cell
claims the maximum output share however short its output is, the code column is
starved to the floor, and a one-line call wraps across three lines in the
editor. The same trap makes `pre.scrollWidth > pre.clientWidth` dead as an
overflow test — it can never be true.

### Eligibility, and automatic fallback to vertical

Keep the original vertical WebR stack when a cell is unsuitable for a compact
side-by-side presentation. The current automatic eligibility limits are:

- exclude setup and empty cells;
- exclude code with more than 12 substantive lines;
- exclude code whose longest source line exceeds 88 characters;
- after execution, revert to vertical if code and output cannot fit together;
- revert if console output still overflows horizontally;
- revert if the code block's height is under 40% of the cell's stacked height —
  a tall output makes the split pointless (see below);
- revert if the code cannot fit its widest allowed column without wrapping;
- plots may remain side by side because their canvas scales to its grid track;
- **never inside a reveal `.columns` block.** Such a cell already has half a
  slide; splitting it again leaves the code a quarter of the width, where even
  `mtcars[2:8, c(3, 5)]` wraps. `custom.scss` excludes these from its own
  automatic two-column rule with `:not(.column *)` — the script matches that,
  and undoes a manual `::: {.side-out}` wrapper found there too, since the
  class alone would drive the notebook.scss grid regardless.

**Prefer the vertical stack.** Side by side is a bonus, not a goal. Each measured
need carries slack (code ×1.15, output ×1.08) before the fit test, so anything
that only fits by cramming stays stacked. Widen that slack rather than tightening
it if cells start looking pinched.

**Never trust a predicted width — read back what Monaco actually rendered.**
Widths here are predicted by measuring source text in what we believe is the
editor's font, and predictions travel badly across browsers, fonts, and device
pixel ratios: a column that the arithmetic says fits can still wrap. After
laying a cell out, compare the `.view-line` count against the source line count
and widen until they match, falling back to stacked at `MAX_CODE_SHARE`. That
check cannot be wrong about wrapping, because it *is* the wrapping.

**Height is not a fit test, but it is a worthwhileness test.** The decks are
`scrollable: true`, so a tall slide scrolls in either layout — height never
decides whether the output *fits*. What it decides is whether splitting the
slide is worth anything. Side by side saves exactly one thing: the height of the
code block, which stops sitting above the output. Against a tall output that is
almost nothing — a 3-line editor beside a 34-line print of `mtcars` takes 679px
where stacked takes 755px, a tenth of the height, in exchange for halving the
slide. So the code block's height must be at least 40% of the cell's stacked
height (`MIN_VERTICAL_SAVING`) — the output may be at most about 1.5x the height
of the code beside it — or the cell stays vertical.

**Calibrate that number against real cells, do not pick it.** One line of code
beside a 10-line tibble scores 0.31 and has to be rejected; the 5-line piping
example beside its 2 lines of output scores 0.81 and has to be kept. A first
attempt at 0.25 sat below the first of those and shipped the exact layout the
rule exists to prevent.

Note this is *not* the old line-count cap. That one rejected output over 16 lines
or 62% of the viewport height as though it would not fit; it threw away
perfectly good layouts on short-code/short-output cells. The test is the ratio,
never an absolute count.

**A side-by-side code block must never wrap a line.** If the code cannot fit in
the widest column it is allowed (`MAX_CODE_SHARE`), there is no acceptable
side-by-side layout for that cell — stack it rather than settling for a narrower
column. This is checked twice: predicted, before promoting, and again by reading
back Monaco's rendered line count afterwards.

**The decision is a promotion, not a demotion.** A cell opens as the ordinary
vertical stack (`data-webr-layout="pending"`) and is moved to two columns only
after its output exists and has been measured. Never guess from the code alone
and lay the cell out side by side up front: output width is not knowable before
a run, so an optimistic guess makes every cell open in two columns with an empty
`Output` banner and then snap back to one column the moment the student clicks
Run — the slide moves under the reader, and the wide-output cells that most need
the full width are exactly the ones that jump.

A cell that runs and prints nothing (an assignment, `library()`, anything called
for its side effect) is never promoted, so it keeps the full width instead of
facing an empty `Output` panel.

A **manual** `::: {.side-out}` wrapper is marked `data-webr-layout-manual="true"`,
opens side by side immediately, and is never torn down — an explicit authorial
choice outranks the measurement.

### Manual opt-in

For a deliberately chosen cell, `::: {.side-out}` remains the manual opt-in.
Use `::: {.side-out .tight}` only for genuinely short code. Do not wrap long
plots, model summaries, or wide tables merely to force side-by-side display.

The same wrapper drives both knitr `{r}` cells and WebR `{webr-r}` cells, so an
author does not have to remember which kind of cell is inside.

### Verification is browser-based, not render-based

When changing these rules, test representative **scalar**, **data-frame**,
**regression**, and **plot** outputs in a browser — not only the static Quarto
render. The layout is chosen by JavaScript at runtime after a cell executes, so
a clean `quarto render` proves nothing about it.

Serve over HTTP; `file://` shows a blank deck (see "Previewing a revealjs deck"),
and WebR cells need minutes to become interactive on first load, so budget for
that rather than concluding the script failed.

Preserve these invariants:

1. code width determines the split;
2. output gets the unused space;
3. the output banner and body have identical widths;
4. poorly formatted output falls back to the original vertical stack;
5. all affected lecture decks render without fenced-div or JavaScript errors.

### Two couplings specific to this repository

1. `custom.scss` caps WebR cells at `width: 90%` (`lectures/custom.scss`, ~line
   217). `notebook.scss` overrides this to `100%` inside `.side-out`, because a
   two-column cell needs the full slide.
2. `custom.scss` lays out plot-drawing WebR cells in two columns automatically
   via `:has(.qwebr-output-graph-area canvas)`, and both that selector and
   `.qwebr-side-by-side` carry `:not(.side-out *)` so the fuller `notebook.scss`
   layout wins inside the wrapper. Do not remove those exclusions — without
   them the `Output` banner lands off the bottom-right corner and the gutter
   caret points at nothing.

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
   find docs -name '*.html' | wc -l     # expect 41
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

## Math rendering: KaTeX, and the two traps in getting there

The site renders math with **KaTeX**, pinned to 0.18.4, set in `_quarto.yml`
for `html` and in every deck's `revealjs` block. It replaced MathJax 2.7.9 on
2026-08-20. Both engines load from jsDelivr, so neither works offline.

Two failures cost real time, and **neither produced a render error**. `quarto
render` exited 0, emitted all 52 files, and logged nothing in both cases. Only
a browser showed the breakage.

1. **The pinned `url:` must end with a trailing slash.** Quarto concatenates
   the filename onto it verbatim, so `.../dist` emits
   `.../distkatex.min.js`, which 404s. Both assets fail, `window.katex` is
   never defined, and every equation silently stays unrendered.

2. **quarto-webr's Monaco loader breaks KaTeX's UMD build.** Monaco ships
   `loader.js`, an AMD loader that defines `define.amd`. KaTeX's UMD wrapper
   tests AMD *before* the browser-global branch:

   ```js
   "function"==typeof define && define.amd ? define([],t) : e.katex=t()
   ```

   So on a WebR deck KaTeX registers as an anonymous AMD module and never sets
   `window.katex`. Quarto's inline renderer then throws `katex is not defined`
   and the math stays as raw `<span class="math">`. MathJax was immune, which
   is why this only appeared on the switch. Non-WebR decks were unaffected —
   the symptom looks random until you diff the script lists.

   The fix is `lectures/katex-amd-fix.html`, which imports the ESM build (ESM
   ignores AMD) and publishes the global before `DOMContentLoaded`. **Every
   deck that includes `webr-layout.html` must also include it**, right after:

   ```yaml
   include-in-header:
     - ../transcript-support.html
     - ../webr-layout.html
     - ../katex-amd-fix.html
   ```

   A deck that gains its first `{webr-r}` cell gains both includes together.

### `\mbox` is not KaTeX

KaTeX has no `\mbox`; use `\text`. With Quarto's `throwOnError: false` an
undefined command is not an error — it is printed literally in red, so
`\mbox{corn yield}` renders as `\mboxcornyield` on the slide with the spaces
collapsed. `05-1` carried 17 of these; all are now `\text`, and there is no
`\mbox` left in the repository. Do not reintroduce it.

### Verifying a math change

Counting `$...$` in the source over-reports badly — currency like `$3.0/bu`
and `$$` inside verbatim teaching examples both match. Count rendered
`class="math"` spans in `docs/` instead, then check in a browser that the
number of `.katex` nodes equals it, that `.katex-error` is zero, and that no
`.katex-html` contains a literal backslash-command. A correctly rendered
formula never contains a backslash; that check is what caught trap 2.

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

## Lecturer transcripts

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
