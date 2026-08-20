# Lecturer transcripts in revealjs decks

A transcript is what the lecturer *says* about one tab or one slide, written out
in full. It is hidden behind a small pill in the slide's top-right corner and
expands into a panel down the right-hand side when a student clicks it.

Audience and purpose, as specified by the instructor: **students reviewing after
class**. Not presenter notes — students see these. (reveal's own `.notes` blocks
are the presenter-only mechanism, and `02-2` uses one as a teaching demo.)

## Adding transcripts to a deck

**1. Include the shared support file** from the deck's YAML header. The path is
relative to the `.qmd`:

```yaml
format:
  revealjs:
    include-in-header: ../transcript-support.html
```

**2. Write transcripts** inside the slide, or inside a single tab of a tabset,
which is the usual case:

```markdown
### YAML

<details class="transcript">
<summary>Transcript</summary>

The very first thing you need, when you want slides instead of a document, is to
tell Quarto which format to produce...

</details>

To create a presentation with Quarto, the first thing to do is...
```

Blank lines around the prose matter — without them Pandoc will not render the
markdown inside the `<details>`.

That is the whole interface. Do **not** paste the CSS into a deck: raw `<style>`
above the first `##` becomes a blank slide (see `CLAUDE.md`).

## Conventions

- One transcript per **tab**, not per slide. A tabbed slide gets one in each tab;
  an untabbed slide gets one at the top of its content.
- Place it at the **top** of the tab's content. Position in the source barely
  matters visually (the panel is absolutely positioned), but keeping it first
  makes the source easy to scan.
- `<summary>` text is always exactly `Transcript`.
- Only ever the class `transcript`. The CSS keys off it.

## Writing style

These are spoken words, not prose. Match the existing 31 in `02-2`:

- **Second person, addressing the class.** "So you've rendered your slides and
  you've got an HTML file. Now what?"
- **90–130 words.** Long enough to be a real explanation, short enough that the
  panel does not need scrolling.
- **Refer to what is on screen.** "Look at the Code tab to see the syntax"; "the
  callout warns"; "flip between the two and note the relationship."
- **Say why, not just what.** The transcript should carry the motivation the
  slide has no room for — the reason a feature exists, the mistake it prevents.
- **Spell out code in prose.** Write "bar-one-bar-two-bar-three" rather than
  `"|1|2|3"`; it is being read as speech.
- **Hand off between tabs.** End a tab by pointing at the next one where the
  lecture actually flows that way.

## Why an overlay, and not in the flow

The first implementation put transcripts in normal flow at the top of each tab.
Measured against reveal's 700px logical slide height:

| Slide | In flow, collapsed | In flow, open | Overlay (either) |
|---|---|---|---|
| Get Started | **705px — overflowed** | 776px | 662px |
| Useful Tools | 831px | 887px | 793px |
| Presenting and navigating | 340px | 411px | 297px |
| Figure | 382px | 468px | 344px |

The collapsed bar cost ~54px on *every* tab whether or not anyone opened it, and
that alone pushed "Get Started" past the slide edge. Expanding was never the
problem — five of seven slides had 230–400px of headroom even fully open.

Absolute positioning drops the cost to **0px in both states**. That is the
reason for the design; keep it if you touch the CSS.

("Useful Tools" still exceeds 700px. It did so before transcripts existed — it
is one of the `.scrollable` slides.)

## Layout constants, and what they are pinned to

In `lectures/transcript-support.html`. Each was measured, not guessed:

| Value | Why |
|---|---|
| `top: 17%` (open panel) | The tab bar ends at 11.8% on most slides and 16.4% on "Useful Tools", which has nested tabsets. 17% clears both, so tab names stay clickable while a panel is open |
| `width: 36%` | A narrow right-hand column; slide content rarely reaches there |
| `max-height: 79%` | Runs from 17% down to 96%, just above the footer, scrolling internally past that |
| `top: 0` (collapsed pill) | Sits beside the slide title, clear of everything |
| `border: none; padding: 0` | Opts out of the `// Answer box` rule in `custom.scss` |
| `margin: 0` on summary | Undoes the negative margin the bare `summary` rule applies |
| `.slide-logo { left: 56px }` | The logo defaults to bottom-right, where the panel runs. Moved bottom-left; 56px clears reveal's menu button at x 8–43px |

If you re-theme a deck or add slides with deeper tab nesting, re-measure the tab
bar before trusting `17%`.

### Measuring whether a tab still fits

Adding a callout to a tab can push it past the 700px slide. Getting a trustworthy
number is harder than it looks, and two obvious approaches both produce garbage:

- **Measuring the `section`.** Only the active pane of each tabset is displayed;
  the rest are `display: none` and contribute nothing. So a clean result proves
  the *first* tab of each tabset fits and says nothing about the others.
- **Toggling `display` on panes yourself.** Tempting, and wrong unless you also
  hide every pane of every nested tabset and restore afterwards. Get it slightly
  wrong and you measure the sum of several panes. The tell is duplicate labels
  reporting identical heights, or a pane of 11,000px. Both happened.

What works: navigate reveal to the slide with `Reveal.slide(i)`, click the tab
link, then measure the pane the link's `href` points at.

```js
a.click();
const pane = document.querySelector(a.getAttribute('href'));
pane.scrollHeight;              // compare against sec.clientHeight (700)
```

`scratchpad/shotTab.mjs` does this and screenshots the result, which is the real
check — a number can be right while the slide still looks wrong.

Note that **700px is not a hard bar on every deck.** Chapter 9's decks set
`scrollable: true`, and a single WebR cell is a code editor plus a Run button plus
an output area, so tabs holding three of them are inherently taller than the slide
and scroll by design. On those decks, only compare a tab against what it was
before your edit.

## Behaviour

The CSS alone is fully functional — `<details>` is a native element, so
collapse/expand needs no JavaScript and survives in `embed-resources` output.

The script adds one thing: **an open panel collapses when the reader moves on**,
so it never reappears over unrelated content. It hooks reveal's `slidechanged`
and `overviewshown`, and captures clicks on `[role="tab"]`. Without the script
everything still works; panels just keep their open state.

Verified behaviour (re-run these if you change the script):

```
transcript opens on the current slide
slide change collapses it
transcript re-opens after returning
tab click collapses it
panel is a narrow right-side column   (37.9% wide, top 17%)
logo moved to the left half           (x 56–156px)
logo clears the menu button           (menu ends x 43px)
logo does not overlap the panel       (panel starts x 731px)
```

## Rollout status

**Chapters 1-9 are complete: 706 transcripts across 24 decks**, all rendering
clean.

| Deck | Transcripts |
|---|---|
| `01-Introduction.qmd` | 52 |
| `02-0-Github-sublime-merge.qmd` | 5 |
| `02-1-Quarto-introduction.qmd` | 38 |
| `02-2-Quarto-revealjs.qmd` | 31 |
| `02-3-Quarto-website.qmd` | 5 |
| `02-4-Quarto-article.qmd` | 16 |
| `03-1-input-output.qmd` | 29 |
| `03-2-data-wrangling-dplyr.qmd` | 49 |
| `03-3-reshape-merge.qmd` | 30 |
| `04-1-data-visualization-basics.qmd` | 29 |
| `04-2-more-information.qmd` | 18 |
| `04-3-fine-tuning.qmd` | 55 |
| `05-1-function-loop-parallel.qmd` | 59 |
| `06-1-code_project_RStudio.qmd` | 24 |
| `07-1-date-string.qmd` | 19 |
| `08-1-make_table_flextable.qmd` | 32 |
| `08-2-modelsummary.qmd` | 25 |
| `L01_vector_basics.qmd` | 57 |
| `L02_raster_basics.qmd` | 18 |
| `L03_create_map.qmd` | 29 |
| `L04_1_vector_interactions.qmd` | 16 |
| `L04_2_vector_spatial_join.qmd` | 33 |
| `L05_vector_raster_interaction.qmd` | 15 |
| `L06_get_spatial_data.qmd` | 22 |

### Counting them, without a false positive

The usual check is that source and rendered counts agree:

```bash
grep -c 'details class="transcript"' <deck>.qmd
grep -o 'details class="transcript"' docs/.../<deck>.html | wc -l
```

The rendered count comes out **one higher than the source count in every deck**.
That extra hit is not a transcript. `transcript-support.html` documents its own
interface in an HTML comment, and that comment contains a literal
`<details class="transcript">` example. It lands in `<head>`, inert. Subtract one,
or grep the body only. Do not go looking for a stray transcript — there isn't one.

Deliberately skipped:

- `04-4-Misc.qmd` and `Chapter-0/logistics.qmd` are both excluded from the render
  list in `_quarto.yml`, so transcripts there would never reach the website.
- Nested `#### Code` / `#### Output` and `### Work here` / `### Answer` tabs
  inside exercises get no transcript. One per **outer** tab, plus one per
  untabbed content slide.

## Review the deck before transcribing it

Chapters 1-3 carry `REVISED VERSION` change-log comments; Chapter 4 did not, and
transcribing it first surfaced four real defects that would have been narrated as
if correct. **Review an unrevised deck before writing its transcripts**, and
verify claims by running them rather than reasoning about them. What that pass
found in Chapter 4, all since fixed:

- `scale_color_viridis_c(option = 2)` silently gave magma, not the inferno the
  slide's own A-H list implies. A bare number does not index that list.
- `scale_color_gradientn()` had four colours against five `values`, with prose
  describing colours as owning intervals. They mark positions and are blended
  between; the lengths must match.
- `shape` on `geom_histogram` and `fill` on `geom_line` emit
  `Ignoring unknown parameters` warnings that were never explained. Note that
  `shape` on `geom_boxplot` is **fine** — `GeomBoxplot` really does use it, for
  outlier points — so it is not the same defect.
- `facet_wrap(state_name ~ .)` ran without complaint but was explained using
  `facet_grid` grammar, blurring the distinction a later tab teaches.

The same pass over `05-1-function-loop-parallel.qmd` found six substantive
errors, all since fixed. The pattern repeats: the code runs, so nothing looks
wrong, but the *claims about it* are false.

- `plan(multicore, ...)` was used with the claim that R "automatically redirects"
  to `multisession` when forking is unavailable. It does not — that was
  `multiprocess`, removed from `future` years ago. When forking is unavailable it
  runs **sequentially in the parent process, silently**. Proved by PID: 4 distinct
  PIDs with forking, 1 (= parent) without. Forking is off on Windows *and* inside
  RStudio, so much of the class got no parallelism while the static rendered
  timings still showed a speed-up. Now `plan(multisession, ...)`.
- An exercise answer looped corn prices into a function's **nitrogen** argument
  and returned yield where revenue was asked for.
- "This method is faster" about `arrange() %>% slice(n())` vs `filter(max)` —
  measured 3x *slower*, and must be: O(n log n) against O(n).
- A for-loop answer with no `print()`, so the official answer produced no output.
- A tab asserting `multiplier` "is provided as an argument" when the whole tab
  exists to show it is not.
- Instruction said `by = 0.01`, answer used `by = 0.02`.

Two structural hazards worth checking in any deck: an object assigned twice
under one name with different shapes where only the later one is `autorun`
(students clicking the earlier section silently get the wrong data), and
`future_lapply()` in a `{webr-r}` cell — WebR is single-threaded and `plan()`
only ever runs in host `{r}` chunks, so "parallel" cells run serially for every
student unless you say so.

Also: never list a **base R** package (`parallel`, `stats`, `utils`) in
`webr: packages:`. Base packages ship with R, are absent from the wasm repo, and
cannot be installed.

**The worst defect found in any deck was in `08-2`**, and it is the template for
what to hunt for. Its "Swapping VCOV" section used `statistic_override` to apply
robust standard errors. modelsummary renamed that argument to `vcov`, and
`msummary()` takes `...`, so the old name is **silently swallowed** — no error,
no warning. The slide placed a default table and a "VCOV swapped" table side by
side and they were byte-identical: it demonstrated nothing while looking correct.
A student carrying the pattern into their own work would believe they had robust
standard errors when they did not. After the fix the SEs genuinely move
(0.690 → 0.635). The general rule: **an argument absorbed by `...` fails
silently, so any "before and after" demonstration must be checked for actually
differing.**

`07-1` turned up the same class from the other direction: **code that was
correct when written and is now broken by a package update**. Two cells relied on
`str_c()` recycling vectors of unequal length. stringr 1.5.0 adopted vctrs
recycling, under which only a length-1 vector recycles, so both cells now raise
`Can't recycle ..1 (size 5) to match ..2 (size 3).` The wasm repo serves stringr
1.5.1, so they failed for every student, and the surrounding bullets explained
recycling behaviour that no longer happens. **When a deck demonstrates a
package's edge-case behaviour, re-run it — the deck does not rot visibly.**

Two more from the same deck, both of the "runs fine, wrong answer" kind:
`str_replace(date_text, "20", "")` to strip century digits mangles the 20th of
every month (`01/20/2015` becomes `01//2015`, 12 of 358 dates), because the first
"20" is the day; and a loop advertised as reading only the soy files looped over
`all_files` rather than `all_files[is_soy]`, reading 60,000 rows instead of
30,000 and discarding the `str_detect()` work the tab had just taught.

`L01` (Chapter 9) produced a finding that I got **wrong** and later corrected, so
it is recorded here as the mistake it was. Its Projection exercises refer to
`fairway_grid` ~500 lines before the only `data(fairway_grid)` call, which looks
exactly like a load-order bug. It is not one: `r.spatial.workshop.datasets` is
`LazyData: true`, so every dataset resolves by name as soon as the package is
attached. Confirmed **in the WebR runtime**, not just locally, by evaluating
`dim(prism_us)` on a deck that never loads `prism_us` — it returned `281x125`.

The lesson is about method rather than about spatial data: I reported three decks
as broken on the strength of reading the code, without ever running the failing
case. Check `DESCRIPTION` for `LazyData` before writing up a missing `data()`
call, and prefer a browser check to an argument.

It also projected North Carolina into UTM zones **14N and 15N**; NC spans
84.3W-75.5W, which is zones 17N/18N. The numeric effect on the buffer example was
small (1465 vs 1431 km2), so this is a conceptual fix rather than a dramatic one —
but "project into the zone your data is in" is the lesson the slide was breaking.
Three of its claims that *looked* wrong turned out correct and were left alone:
`dist = 2000` on unprojected data really is metres (s2), `st_distance` on
unprojected data really returns metres, and the stated EPSG 4267 is right.

`L06` turned up the most serious find of the whole pass, and it was not a teaching
error. **A live USDA-NASS API key was hard-coded in the deck**, in two places: a
local `{r}` chunk, and the `#| context: setup` webR chunk. The second matters,
because a webR setup chunk's source is embedded in the rendered HTML so the browser
can run it. The key was therefore published — confirmed by fetching the live page
from the course website and finding it there.

Every `getQuickstat()` call in the deck is `eval = F`, and no webR cell referenced
the variable, so the key was doing nothing at all. Removed from both places,
replaced with `Sys.getenv("NASS_API_KEY")`, and the deck now carries a callout on
keeping credentials out of documents. The key still needs rotating — that is the
instructor's to do.

**Check for this on any deck that touches an API.** The webR setup chunk is the
dangerous spot precisely because it looks hidden: `include: false` on an `{r}`
chunk really does keep it out of the output, and it is easy to assume
`context: setup` behaves the same way. It does not.

Its other substantive defect was a repeat of the `L02` lesson in a worse place: the
final exercise aggregated **Cropland Data Layer** by a factor of ten with no `fun`
argument, so it averaged crop codes — 1 for corn, 5 for soybeans — into numbers
that are not any crop. Now `fun = "modal"`. It also set the PRISM download folder
with `options(prism.path = ...)`, which the package superseded with
`prism_set_dl_dir()` (confirmed from prism's own NEWS; `get_prism_dailys()` itself
is still current), described `lapply()` as a for loop, and pointed at Illinois in a
paragraph about Nebraska.

Its table of contents had one dead anchor of four — the mildest of the five broken
tables of contents in Chapter 9.

`L05` contributed the clearest example yet of the recurring theme, *a wrong thing
that produces no error*:

```r
avg_NDRE <- NDRE_extracted_tb %>% group_by(ID) %>% summarize(avg_NDRE = mean(NDRE))
treatment_blocks <- mutate(treatment_blocks, NDRE = avg_NDRE)   # a 2-column tibble
```

`dplyr` allows a data frame as a column on purpose, so this nests the whole summary
table inside `treatment_blocks` and the row count still matches. Nothing complains
until much later, when printing the object fails with `corrupt data frame: columns
will be truncated or padded with NAs`. **Whenever the right-hand side of a
`mutate()` came from `summarize()`, name the column.**

It also asserted a failure that does not happen. Having shown that
`terra::crop()` errors on a CRS mismatch, the deck ran `terra::extract()` on the
same mismatched pair and said "Oops, we did it again." `extract()` does not error —
it re-projects the vector data for you and warns. The two functions genuinely differ,
so that is now a callout rather than a false claim. (`crop()`'s message,
`[crop] extents do not overlap`, never mentions the CRS either, which is worth
telling students.)

Smaller: `terra::maske()` in an answer students copy; a mask objective that named
`corn_yield` where it meant `treatment_blocks`; and a `cbind()` that silently
produces a second `NDRE` column named `NDRE.1`.

Its table of contents was the **fourth** broken one in Chapter 9, and the worst
kind — besides two dead anchors it advertised a section, "Basic speed comparison",
that does not exist anywhere in the deck.

One claim was checked and held: the worked extraction example says three points
take the values 50, 4 and 54, and with `set.seed(378533)` they do.

`L04_2` was the worst of the Chapter 9 decks so far, and almost all of it was
wrong *numbers* rather than wrong code — the kind only running the deck exposes:

- It filtered `countyfp == "129"`, assigned the result to `adams_county`, and
  called it Adams county in the surrounding prose. 129 is **Nuckolls**. Adams is
  001, and it has 53 wells.
- "`countyfp` of 039 and 109 (first two rows), there are no wells inside them" —
  the first two rows are 115 (Loup, no wells) and 005 (Arthur, four wells).
- One HUC unit was said to intersect **seven** counties in one sentence and to
  have **four** rows two sentences later. It intersects **eight**.
- A cell was missing a `%>%` after `as.data.frame()`, so it errored with "object
  'HUC_CODE' not found" — and it also summarised `mean(acres)` when `ia_nitrogen`
  has no `acres` column at all.
- The syntax template for a custom join relation was `st_join(..., dist = 5)`,
  which is not merely stylistically off but an error: `unused argument (dist = 5)`.
  Extra arguments belong inside the lambda.
- It referred to a function called `spatial_join()`, which does not exist.

Two of its claims were checked and **held**, and were left alone: `identical()`
on two geometry rows of a one-to-many join really does return TRUE, and the first
soybean yield point really does match nothing while the second matches seed IDs
1 and 558.

Its table of contents was not merely dead-linked but described `L04_1`'s content
— topological relations, subsetting, value extraction — none of which is in this
deck. That is now three of four Chapter 9 decks with a broken TOC, so **check the
table of contents against the actual `##` headings on every remaining deck.**

`L04_1`'s defects were mostly cross-referencing rather than code. Two "confirm
your visual inspection" sentences named **each other's** function: the one under
`st_is_within_distance()` told students to check it against `st_nearest_feature()`
and vice versa. Its syntax block for `st_is_within_distance()` omitted `dist`
entirely, which is required and has no default. And the railroads example flagged
its result as `in_hpa` when the subset was by Lancaster county — a copy-paste from
the wells example two tabs earlier. Both of its table-of-contents links were dead,
the same failure as `L03`.

Four of its claims were checked by running them and all four held, so they were
left alone: `st_intersects(points, polygons)` really does return 1, 2, 3 for the
first point; polygons 1 and 3 really do touch at a single point with zero shared
area (`st_relate` gives `FF2F01212`, intersection area 0); `st_crop(x, sf)` really
is identical to `st_crop(x, st_bbox(sf))`; and `size =` on `geom_sf` does **not**
emit a deprecation warning in ggplot2 4.0.1, which spared eight needless edits.

`L03` produced a new failure mode, and it is one to scan for repo-wide: **markdown
placed between `::: {.panel-tabset}` and the first tab heading is silently dropped
from the rendered deck.** Not turned into a stray slide, not warned about — gone.
Its "Specifying aesthetics" slide opened with a sentence explaining that maps are
ordinary `ggplot2` figures, and no student has ever seen it.

A scanner for the pattern (validate it on a synthetic file first — a checker that
reports nothing because it is broken is the trap it is meant to catch):

```bash
find lectures exercises -name '*.qmd' | xargs python3 scan_pretab.py
```

Run repo-wide it found **two more, in `03-2-data-wrangling-dplyr.qmd`**, a deck
already marked complete. One was the sentence naming the dataset for an entire
exercise set, so those exercises rendered with no data named. Both fixed and
re-rendered; the deck's 49 transcripts are intact.

`L03`'s setup called `data(wells_ne)`, a plain data.frame the deck never uses,
while every map in it uses `wells_ne_sf`. Changed for tidiness — but per the
`LazyData` note above, this was **not** the "object not found" failure I first
reported it as.

Three of its claims were wrong in ways only running the code reveals:
`facet_wrap(~lyr)` combined with `aes(fill = NIR)` yields **one** panel, not one
per layer, so the faceting demo demonstrated nothing; a PRISM legend read
"Precipitation (inches)" for values running 0-73.8, which are millimetres; and the
prose told students to try `coord_sf(32614)`, whose first argument is `xlim`, not
`crs`. A fourth was checked and turned out **correct** — `geom_spatraster()` really
does plot all layers of a multi-layer raster and warn about it.

Also worth noting for its own sake: `aes(fill = "red")` produces `#F8766D` and a
legend entry reading "red". The deck used it as though it filled red. That is a
general `ggplot2` trap, so it now has a callout.

Its factual error is a good example of a plausible-sounding default. The deck
listed `resample()`'s methods as `"near": nearest neighbor (Default)`. terra's
real default is **`bilinear`**, with `near` used only when the first layer is
categorical — confirmed from `?resample` and by checking that the no-argument
result is identical to `method = "bilinear"` and differs from `"near"`. Left
unfixed, a student resampling a land-cover raster gets interpolated codes like
1.4. `aggregate()` has the same shape of trap (`fun` defaults to `"mean"`), and
the deck documented `fact` with an **empty bullet**, so both are now spelled out.

Two claims the deck made about `[]` were wrong in a way worth checking for
elsewhere: `SpatRaster[]` returns a **matrix**, not a vector, and `r[cells]`
returns a **data.frame**. That also means the deck's own arithmetic check,
`c(a[i], b[i], log(c[i]))`, was building a *list of three data.frames* and
printing them as three blocks, two labelled `blue`. `unlist()` fixes it.

`08-1` adds a third flavour: **function names that do not exist**. Its syntax
reference listed `pr_c = fp_celll()` (three l's), its prose called `fp_par()`
"`fp_paragraph()`", and a callout recommended "`add_footer_rows`". None of the
three exist — checked against the installed `officer` and `flextable`
namespaces. It also stated that `part = "all"` covers "the body and the header",
which is wrong: applying `color(part = "all")` to a table with a footer row turns
the footer red too. Cheap check for any deck that documents an API:

```r
for (n in c("fp_cell","fp_par","add_footer_row"))
  cat(n, tryCatch({get(n, envir = asNamespace("officer")); "ok"},
                  error = function(e) "MISSING"), "\n")
```

`06-1` shows the same review pays off on decks with **no runnable code at all**.
It claimed that installing `styler` lets you press cmd/ctrl+shift+A to reformat
to tidyverse style. That shortcut is RStudio's own built-in "Reformat Code" — it
works without `styler` and does not follow the tidyverse guide — and `styler`'s
four addins declare no shortcut, because RStudio addins never get one by
default. Checked by reading `system.file("rstudio/addins.dcf", package="styler")`
rather than by running code. For interface and shortcut claims, the package's own
`addins.dcf`, and the RStudio keyboard-shortcut list, are the sources of truth.

## Open idea, not built

For after-class review, opening 31 panels one at a time is clumsy compared with
reading straight through. The transcripts are plain markdown in the `.qmd`, so a
**companion transcript page per lecture** could be generated from the same source
without rewriting any of them. Raised with the instructor, who chose the overlay
first; the two are not mutually exclusive.

## Chapter 9 additions (2026-08-18)

Three sections added after the review pass, all with worked examples verified in
the **WebR runtime** rather than only locally.

| Deck | Section | Tabs | Transcripts |
|---|---|---|---|
| `L01` | Sticky geometry | 5 | 5 |
| `L01` | When spatial operations fail | 4 (+7 nested) | 4 |
| `L05` | Going the other way: `rasterize()` and `zonal()` | 4 (+2 nested) | 4 |

Numbers quoted in the callouts, all measured:

- `summarize()` on an `sf` with geometry is **hundreds of times slower** than
  after `st_drop_geometry()`. Re-measured 2026-08-20 (see below); the figure
  first written here, ~40x, was measured on a *different* grouping than the one
  the slide actually runs.
- `left_join(df, sf)` returns a plain `data.frame` that *has* a geometry column but
  **is not an `sf`** — so it prints fine and `geom_sf()` refuses it.
- `write.csv()` on one county produces a **524-character** line of
  `list(list(c(-81.47...)))`.
- `dist = 2000` buffers a county to **1,431 km²** on UTM (metres) and **13,186 km²**
  on NC state plane (US survey feet). Same number, same code.
- `st_area()` on a self-intersecting bowtie returns **0**, silently — the two
  triangles cancel. `st_intersection()` on it raises `TopologyException`.
- `rasterize()` + `zonal()` and `extract()` + `group_by()` agree to three decimals
  (0.6044 vs 0.6045), differing because rasterize assigns cells by centroid while
  extract takes every intersecting cell.

Two things the WebR check caught that a local-only check would not have:

1. The invalidity message differs by engine. Locally with s2 (lon/lat) it reads
   `Edge 0 crosses edge 2`; under GEOS (projected) and in WebR it reads
   `Self-intersection[1 1]`. The slide had quoted the wrong one, and now lists the
   family rather than one string.
2. `rasterize()` in WebR emits
   `GDAL Error 1: PROJ: proj_crs_get_coordinate_system: Object is not a SingleCRS`.
   It is a warning despite the wording, the output is correct, and it does not occur
   in RStudio — so the slide says so, rather than leaving students to worry.

Both new L01 sections needed splitting into nested tabs to stay under 700px
(`Invalid geometry` was 1632px, `Units` 1015px). After splitting, every tab in both
sections measures 145-618px, and both tab strips still fit one row.

### Re-measuring the `summarize()` slowdown (2026-08-20)

The "~40x" figure originally recorded above was measured with `group_by(grp)` —
two groups — while the slide's cell runs `group_by(NAME)`, which is 100 groups.
Wrong grouping, wrong number. Re-measured both, locally and in the deck's own
WebR session (`nc`, 100 counties, 20 reps unless noted):

| grouping | local, sf 1.0.19 | WebR, sf 1.0.20 |
|---|---|---|
| `group_by(grp)`, 2 groups | 1.06s vs 0.033s = **32x** | 15.4s vs 0.047s = **327x** |
| `group_by(NAME)`, 100 groups | 5.47s vs 0.028s = **196x** | 26.1s vs 0.059s = **442x** |

So the effect is not merely still real, it is an order of magnitude larger than
the slide claimed, and largest in the browser where students meet it. It also
scales: at 10,000 features and 2,000 groups locally, `summarize()` takes 7.2s
against 0.007s without geometry — **1,031x**.

The **second** defect this turned up matters more than the number. The tab's lead
sentence read "ordinary `dplyr` verbs on an `sf` cost far more than on the same
data without it," which is false. Only verbs that rebuild geometry are expensive.
Measured on the same `nc`:

| verb | local ratio | WebR ratio | WebR absolute (20 reps) |
|---|---|---|---|
| `mutate()` | 1.6x | 1.0x | 0.015s vs 0.015s |
| `select()` | 1.8x | 1.5x | 0.021s vs 0.014s |
| `arrange()` | 1.3x | 5.1x | 0.113s vs 0.022s |
| `filter()` | 1.3x | 6.6x | 0.079s vs 0.012s |
| `summarize()` | 196x | 442x | 26.1s vs 0.059s |

A ratio of 5-6x on a verb that takes 4ms is not a cost; the absolute column is
the one that matters. Note the slide must therefore **not** say these verbs are
"not affected" — a student timing `filter()` in WebR gets 6.6x and catches the
slide out. It says they cost *milliseconds either way*, which is what is true. Telling students "dplyr on `sf` is slow" would have them
dropping geometry defensively before every `filter()`. The tab now names
`summarize()` specifically and says the other verbs are fine.

The cell was also cut from 20 reps to 5. At 20 the first `system.time()` took
**26 seconds** in the browser — too long to sit through in a lecture. At 5 it
takes about 6.5s and still reports a ratio in the hundreds. Clicking Run on the
shipped cell, as a student would, gave **6.515s vs 0.015s = 434x**; an injected
run of the same code gave 499x. The slide therefore says "400-500x in this
browser, roughly 200x in RStudio" rather than pinning one figure.

Final layout: the tab measures **556px** against a 700px slide, whole callout
visible, tab strip still one row.

Lesson worth carrying: **benchmark the code that is on the slide, not code like
it.** The original measurement was of a real thing, just not the thing the
student runs.

#### A measuring rig that lies, again

Two tab-height rigs gave nonsense here before the real number turned up, both in
the same way: **they clicked every tab in one `Runtime.evaluate` loop.** Monaco
never gets a chance to relayout between clicks, so the panes report the height
they had while hidden — the `It is slow` pane came back as **6037px** and
`Invalid geometry` as 9017px. The same rig also reported the tab strip wrapping
to two rows. Both false.

What works, and is the only method to use here: navigate with `Reveal.slide(idx)`,
**wait**, click the one tab, **wait**, then measure the link's `href` target. One
tab per evaluate. Measured that way the same pane is 556px and the strip is one
row — which a screenshot then confirms.

Also wait for webR to boot before measuring anything on a webR deck. Monaco has
no real height until then.
