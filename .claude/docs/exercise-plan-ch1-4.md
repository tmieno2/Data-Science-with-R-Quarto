# Exercise plan, Chapters 1–4

Where student exercises are missing across the Chapter 1–4 decks, what each one
should look like, and in what order they are worth writing.

Companion to [lecture-transcripts.md](lecture-transcripts.md). Same premise: the
decks are the deliverable, the additions go inline, and the in-repo idiom is
already established — the job is to extend it, not invent a new one.

## 0. Status

**Done.** The offline decks — the ones webr cannot serve — are covered by four
handouts in `exercises/`, written and rendered:

| File | Title | Ex | Covers |
|---|---|---:|---|
| `2-1-quarto-basics.qmd` | Ex-2-1: Quarto Basics | 10 | `02-1` |
| `2-2-quarto-revealjs-website.qmd` | Ex-2-2: Revealjs Slides and Websites | 11 | `02-2`, `02-3` |
| `2-3-quarto-article.qmd` | Ex-2-3: Writing an Article in Quarto | 10 | `02-4` |
| `3-1-input-output.qmd` | Ex-3-1: Importing and Exporting Files | 12 | `03-1` |

These are **handouts, not in-deck exercises**, because every task is
"do this on your machine, then check X" and none of it fits on a 700px slide.
Answer keys for `3-1` were verified by running them against the real files in
`data-science-course-supplementary-datasets`.

## 0b. Exercise numbering

`exercises/` used a topic-based scheme that did not track the lecture chapters
(`Ex-2-x` was Data Visualization, i.e. Chapter 4 material). Every file has been
renumbered so that **`Ex-N-M` means lecture Chapter N**:

| Was | Now | Chapter |
|---|---|---|
| `ex-2-1-ggplot2` | `4-1-ggplot2` | 4 |
| `ex-2-2-ggplot2-fine-tune` | `4-2-ggplot2-fine-tune` | 4 |
| `ex-2-3-practice_theme` | `4-3-practice-theme` | 4 |
| `1-1-data_wrangling_dplyr` | `3-2-data-wrangling-dplyr` | 3 |
| `1-2-data_merging` | `3-4-data-merging` | 3 |
| `1-3-data-reshaping` | `3-3-data-reshaping` | 3 |
| `date` | `7-1-date` | 7 |
| `8-1-flextable` | unchanged | 8 |

Within Chapter 3 the order follows the decks: `03-1` input/output, `03-2`
dplyr, `03-3` reshaping then merging. `7-1-date.qmd` was excluded from the
render list in `_quarto.yml` because it was broken; it has been fixed and the
exclusion removed, so it now renders.

Two files had no `abstract:`, which left the Topic column of the exercises
listing blank; `7-1-date` and `8-1-flextable` now have one.

Stale `.html` and `.rmd` files under the old names are still sitting in
`exercises/`. They are build output and superseded drafts, not sources, and
nothing references them. Left in place because this repository is not under
version control.

### Chapters 5-9

Six more handouts, written and rendered:

| File | Title | Ex | Covers | Runs |
|---|---|---:|---|---|
| `5-1-loops-and-parallel.qmd` | Ex-5-1: Functions, Loops, and Parallelization | 8 | `05-1` | RStudio |
| `6-1-project-organization.qmd` | Ex-6-1: Organizing a Reproducible Project | 8 | `06-1` | RStudio |
| `7-1-date.qmd` | Ex-7-1: Working with Dates | 8 | `07-1` date half | webr |
| `7-2-strings.qmd` | Ex-7-2: Manipulating Strings | 8 | `07-1` string half | webr |
| `8-2-modelsummary.qmd` | Ex-8-2: Regression and Summary Tables | 9 | `08-2` | RStudio |
| `9-1-create-maps.qmd` | Ex-9-1: Creating Maps with `ggplot2` | 7 | `L03_create_map` | webr |

`7-1-date.qmd` is a **rewrite**. The previous version was a solutions sheet with
no student-facing cells, it called `month()` and `ymd()` without loading
`lubridate`, so every answer chunk errored at render, and it was therefore
excluded from the render list in `_quarto.yml` — invisible on the site. Its
Exercise 5 answer (`ymd("2021-11-30") + months(3)`) also returns `NA`. The
exclusion has been removed and the file now renders.

Choice of medium: Chapter 5's remaining topics are timing comparisons and
parallel processing, neither of which is meaningful in a browser, so that one is
a RStudio handout. Chapter 6 has no code to speak of. Chapter 8's deliverable is
a Word file or a png on disk. Chapters 7 and 9 are webr, and Chapter 9 installs
`r.spatial.workshop.datasets` from `https://tmieno2.github.io/rwasm-package/repo`
exactly as `L03_create_map.qmd` does.

**Still to do:** the in-deck webr exercises for `01`, `03-2`, `03-3`, `04-1`,
`04-2`, `04-3`, `04-4`, per §4 and §5 below. In Chapters 5-9, still uncovered:
`08-1` flextable beyond the four existing exercises, and Chapter 9's
`L04_1`/`L04_2` (vector interactions and spatial joins, 1 exercise each),
`L05` (vector-raster), and `L06` (getting spatial data).

### Data problems found while writing these

1. **`quarto-examples/data/data-for-loop-demo/`** — all 60 files carry
   `field_id = 1`, so binding them loses which experiment each row came from.
   Ex-5-1 turns this into the lesson, but it may not be intentional.
2. **The 30 `soy_experiment_*.rds` files have a column named `corn_yield`.**
   It holds soybean yields. Ex-5-1 flags it; worth fixing at source.
3. **`03-1-input-output.qmd:602`** shows `sheet = "2008"`; the real sheet names
   are `corn_yields_08` and `corn_yields_09`. `eval: false`, so it never errors
   during render.
4. **`02-4-Quarto-article.qmd:275`** labels a table chunk `fig-sample-label`
   while giving it a `tbl-cap`.
5. **`02-4-Quarto-article.qmd:754-805`** tells students to render
   `sample_qmd_article.qmd` from `quarto-examples/templates/`; no such file
   exists there.
6. **`02-0-Github-sublime-merge.qmd:180`** says `data/` in `quarto-examples`
   holds the datasets for later exercises; it holds only
   `data-for-loop-demo/*.rds`, which is Chapter 5 material.

### Recurring authoring trap

A four-backtick fence containing a ```` ```{r} ```` block **still gets executed**
by knitr unless the outer fence is `{verbatim}`. This bit three of these files
during writing, and it is the same failure that took `7-1-date.qmd` off the site.
Use ` ````{verbatim} ` for any block showing chunk syntax, and always render
before committing.

## 1. Current state

`Ex` counts self-contained exercises (a prompt the student answers), not
demonstration chunks.

| Deck | Lines | Ex | Verdict |
|---|---:|---:|---|
| `01-Introduction` | 1408 | 2 | Thin. The two live in one section; the conceptual core has none |
| `02-0-Github-sublime-merge` | 189 | 1 | Clone only. Nothing on the commit/push cycle |
| `02-1-Quarto-introduction` | 1243 | **0** | **Worst gap in the course** |
| `02-2-Quarto-revealjs` | 1068 | **0** | None |
| `02-3-Quarto-website` | 138 | **0** | Short deck; one task would finish it |
| `02-4-Quarto-article` | 805 | **0** | None, and the material is error-prone |
| `03-1-input-output` | 948 | **0** | **Second-worst gap** |
| `03-2-data-wrangling-dplyr` | 1943 | 10 | Best-covered deck. Verbs are drilled; piping and `across()` are not |
| `03-3-reshape-merge` | 1279 | 5 | Reshaping covered. Join-key diagnosis is not |
| `04-1-visualization-basics` | 980 | 2 | Good pattern, too few. Supplementary geoms untouched |
| `04-2-more-information` | 878 | 4 | Reasonable. Data-prep and multi-dataset sections untouched |
| `04-3-fine-tuning` | 1851 | 2 | Both in the first quarter. Theme and all of colour have none |
| `04-4-Misc` | 1688 | **0** | webr is configured and never used |

Roughly 5,000 of 14,400 lines sit in sections with no practice attached.

## 2. Constraints that shape the design

1. **webr cannot touch the filesystem.** `03-1` is entirely about reading and
   writing files, so its exercises cannot be "run this". They must be
   predict-the-error, reason-about-the-path, or do-it-on-your-machine. `03-1`
   also has no `filters: [webr]` in its YAML at all.
2. **Chapter 2 is not runnable either.** Quarto and Git exercises happen in the
   student's own RStudio. In-deck they can only be a task plus a
   "what you should see" check.
3. **`04-4` already declares webr** (`dplyr`, `ggplot2`, `nycflights13`) and
   uses zero webr chunks. Free capacity.
4. **Slide space is tight** (CLAUDE.md trap 3). Every exercise must sit inside a
   `::: {.panel-tabset}` so an N-part exercise costs one slide, not N.
5. **Answers must be `{r} eval: false` + `code-fold: true`**, never `webr-r` —
   a webr answer block renders as an editable box that reads as another task.
6. **New packages must be added to the deck's `webr: packages:` list**, and each
   one costs load time on first run. Prefer datasets already loaded.

## 3. The five patterns

Patterns A and B already exist in the repo; use them unchanged. C is used once
(`01`, `?rep`). D and E are new and are what the Chapter 2 and `03-1` gaps need.

### A. Work-here / Answer (default for anything runnable)

````markdown
##### Exercise 1

Find the observations in June and July.

::: {.panel-tabset}
### Work here

```{webr-r}

```

### Answer
```{r, eval = FALSE}
#| code-fold: true
dplyr::filter(flights_mini, month %in% c(6, 7))
```

:::
<!--end of panel-->
````

### B. Reproduce-the-target (default for ggplot2)

The target renders from a webr chunk with `context: output`, so the student sees
the figure but not the code.

````markdown
Using `carat` and `price` from `premium`, generate the figure below:

```{webr-r}
#| context: output
ggplot(data = premium) +
  geom_point(aes(x = carat, y = price), color = "red")
```

::: {.panel-tabset}
### Work here
```{webr-r}

```

### Answer
```{r}
#| code-fold: true
#| eval: false
ggplot(data = premium) +
  geom_point(aes(x = carat, y = price), color = "red")
```

:::
````

### C. Predict-then-run

Student commits to an answer before executing. Best for anything where the
intuitive answer is wrong: coercion, `NA`, grouping that survives `summarize()`,
`fill` vs `color`.

````markdown
Write down what each line returns **before** running it.

```{webr-r}
c(1, 2, "3")
c(TRUE, 2)
sum(c(1, NA, 3))
```

::: {.callout-note collapse="true" title="Answers"}
...why, not just what...
:::
````

### D. Debug-it (new)

A prefilled webr chunk that is broken, plus the error message the student would
actually see. They fix it. This is the pattern that matches how students really
fail — they meet an error, not a blank editor.

````markdown
This chunk errors. Read the message, then fix the code.

```
Error in `dplyr::filter()`:
! Problem while computing `..1 = carrier = "US"`.
```

::: {.panel-tabset}
### Fix it
```{webr-r}
dplyr::filter(flights_slim, carrier = "US")
```

### Answer
```{r, eval = FALSE}
#| code-fold: true
# `=` assigns, `==` compares. filter() needs a comparison.
dplyr::filter(flights_slim, carrier == "US")
```
:::
````

### E. On-your-machine task (new; Chapters 2 and `03-1`)

A numbered task list, an explicit success check, and folded common failures. No
webr. Keep the checklist short enough to fit one slide.

````markdown
### Do it yourself

1. Create `practice.qmd` in your course project folder.
2. Add a chunk that reads `data/corn.csv` with `here()`.
3. Render it, then open the `.html` **from a different folder**.

**It worked if:** the figure still appears after you move the file.

::: {.callout-warning collapse="true" title="If the figure disappeared"}
You are missing `embed-resources: true`. See the "Submitting your html" section.
:::
````

## 4. Per-deck proposals

### 01-Introduction — add ~6

Existing two sit in §Functions. The 900 lines on object types have none.

1. **Coercion and `NA`** (after §`NA`, ~line 316). Pattern C.
   `c(1, 2, "3")`, `c(TRUE, 2)`, `sum(c(1, NA, 3))`, `NA == NA`,
   `mean(c(1, NA), na.rm = TRUE)`. The `NA == NA` line is the one that pays off
   later in `filter()`.
2. **Assignment and evaluation** (after §Object evaluation, ~line 393). Pattern C.
   `x <- 5; y <- x; x <- 10; y` — what is `y`? Kills the reference-semantics
   misconception before it forms.
3. **Class recognition** (after §Recognizing the class, ~line 672). Pattern A.
   Give four objects, ask for `class()` of each and *why*. Includes a
   `data.frame` column, so they see a `data.frame` is a list of vectors.
4. **Vector indexing** (after §Access elements, ~line 1177). Pattern A.
   Positive index, negative index, logical index, and one out-of-range index
   that returns `NA` rather than erroring.
5. **`[[` vs `$` vs `[` on a list** (after §Access elements using `$`, ~line 1345).
   Pattern C. `l[1]` vs `l[[1]]` — the single highest-yield prediction in the
   whole deck, and currently untested.
6. **Reading an error message** (in §Reading an error message, ~line 909).
   Pattern D. Three errors: `object 'x' not found`, `could not find function "fliter"`,
   `non-numeric argument to binary operator`. Ask what each *means* before fixing.

### 02-0-Github-sublime-merge — add 1

Extend the existing "Do it yourself" (Pattern E) past cloning: make a change,
stage it, commit with a message, push, confirm on github.com. Right now students
clone and never complete a cycle.

### 02-1-Quarto-introduction — add ~6 (highest priority)

1243 lines, zero exercises, and this deck is where submission failures come
from. All Pattern E except #3.

1. **First render** (after §Render, ~line 204). Create a qmd, add a chunk that
   makes a plot, render. Success check: an `.html` appears next to the `.qmd`.
2. **Chunk options** (after §Various options, ~line 649). Give a target output
   picture — code hidden, figure shown, warnings gone — and ask which of
   `echo`, `eval`, `include`, `warning`, `message` produces it. Pattern A-style
   answer without webr.
3. **Fresh R session** (after §Caveat, ~line 386). Pattern C/D. A qmd that uses
   an object defined only in the console. Predict what happens on render, then
   explain. This single misconception generates the most support requests.
4. **Diagnose a failed render** (in §When a render fails, ~line 745).
   Pattern D with a real Quarto error block. Three causes: a typo'd function, a
   missing package, a chunk-label collision.
5. **Paths and `here()`** (after §Option 3, ~line 1042). Pattern E. Read a csv
   from a subfolder using `here()`, then render from a different working
   directory and confirm it still works.
6. **`embed-resources`** (in §Check it worked, ~line 1114). Pattern E, as
   sketched in §3.E above. Given the deck already frames this as a submission
   requirement, it should be a required task, not a note.

### 02-2-Quarto-revealjs — add 3

All Pattern E; each maps to a slide the student will actually need.

1. Convert an existing report qmd to `format: revealjs` and split it into slides.
2. Build one slide with two columns and a fragment. Two features, one task.
3. Add a logo and footer, then export to PDF via `?print-pdf`.

### 02-3-Quarto-website — add 1

Pattern E: add a third page, register it in `_quarto.yml`'s navbar, rebuild,
confirm it appears. The deck currently stops before students edit `_quarto.yml`
themselves.

### 02-4-Quarto-article — add 4

Pattern E. This deck teaches exactly the mechanics that break silently — a
broken cross-reference renders as `?fig-yield` rather than erroring, so students
do not notice.

1. Place a figure with `#| label: fig-...` and `#| fig-cap:`, then cross-ref it.
   Success check: the text reads "Figure 1", not "?fig-yield".
2. Same for a table.
3. Typeset a two-line aligned equation, number it, and reference it.
4. Add a `.bib` entry, cite it twice, and switch the CSL style. Success check:
   the reference list changes format.

### 03-1-input-output — add ~5 (second priority)

Not runnable in webr. Two of these need no filesystem and could run in webr if
the YAML gained `filters: [webr]`; the rest are Pattern E.

1. **`read.csv()` vs `read_csv()`** (after §Compare, ~line 247). Pattern C.
   Predict the class, and predict what happens to a column of `"1"`, `"2"`,
   `"N/A"` under each.
2. **Path reasoning** (after §Relative paths, ~line 355). No code. Give a project
   tree and a working directory, ask which of four paths resolve. Purely
   diagnostic, and cheap to write.
3. **`here()` in practice** (after §`here()`, ~line 408). Pattern E. Same read
   from two different working directories.
4. **`File not found`** (in §File not found, ~line 518). Pattern D with the real
   message. Ask for the three things to check, in order.
5. **Round trip** (after §Export an R object, ~line 886). Pattern E. Write an
   rds and a csv from the same object, read both back, compare `class()` and
   `str()`. Shows what csv loses — factors, dates, list-columns.

### 03-2-data-wrangling-dplyr — add 4

Best-covered deck; the gaps are specific.

1. **Piping** (after §Chaining, ~line 659). Pattern A. Give a nested three-call
   expression, ask for the `%>%` version, then the `|>` version. Piping is the
   hardest idea in the deck and is currently untested.
2. **`arrange`** (after §`arrange`, ~line 1327). Pattern A. Two-key sort, one
   descending, with the `NA`-goes-last note.
3. **Grouping survives `summarize()`** (after §The group does not go away,
   ~line 1503). Pattern C. Predict the output of a chained double `summarize()`.
   The deck flags this as a trap and then does not test it.
4. **`across()`** (after §Compare, ~line 1763). Pattern A. Mean of every numeric
   column by group, using `where(is.numeric)`. The whole `across()` section —
   ~280 lines — currently has no practice.

### 03-3-reshape-merge — add 3

1. **Key diagnosis** (after §Match? 3, ~line 883). No code. Show two datasets and
   ask which columns form the key and what the relationship is. This is the part
   students get wrong in Assignment 1, and the "Match?" slides teach it without
   testing it.
2. **`left_join()` vs `inner_join()`** (after §demonstration: 1 to 1, ~line 1078).
   Pattern C. Predict the row count of each on the same pair of tables.
3. **Accidental many-to-many** (after §demonstration: m to m, ~line 1149).
   Pattern D. A join that silently produces a row explosion. Ask for the row
   count before and after, then for the fix.

### 04-1-visualization-basics — add 3

1. **Inside vs outside `aes()`** (after §`aes()`, ~line 285). Pattern C.
   `color = "blue"` inside `aes()` — predict the result, then explain the
   legend that says "blue". Ideal prediction exercise, and the deck's central
   distinction.
2. **Pick the geom** (after §Figure types, ~line 333). No code. Four questions,
   ask which geom answers each. Cheap, and forces intent before syntax.
3. **Supplementary geoms** (after §annotate, ~line 980). Pattern B. One target
   figure combining `geom_point`, `geom_smooth`, and `geom_hline` at the mean.
   250 lines of geoms with no practice at present.

### 04-2-more-information — add 2

Existing four are fine. Missing:

1. **Reshape before plotting** (after §Wide v.s. Long, ~line 788). Pattern B, and
   the best bridge in the course: give wide data and a target figure with two
   coloured series. They must `pivot_longer()` before `ggplot()` will work.
2. **Global vs local data** (after §Use multiple datasets, ~line 870). Pattern B.
   All points plus a highlighted subset in a second colour, from two data
   arguments.

### 04-3-fine-tuning — add ~5

Both existing exercises are in the first quarter. Everything after line 700 —
theme, custom themes, facet themes, and all of colour — has none.

1. **Theme naming rules** (after §Common functions, ~line 776). No code. Given
   "move the legend to the bottom" and "make axis text bigger", name the
   `theme()` argument and the `element_*()` type. Tests the naming *system*
   rather than one call.
2. **Build a theme** (after §Build on a pre-made theme, ~line 1156). Pattern B.
   Target figure = `theme_bw()` plus three modifications.
3. **Viridis** (after §Example 2, ~line 1575). Pattern B. Same figure twice,
   once continuous and once discrete, so `_c` vs `_d` is felt rather than read.
4. **Manual scale** (after §discrete, ~line 1771). Pattern B. Named vector of
   three HEX colours mapped to three groups.
5. **Fix the colour scale** (in §continuous, ~line 1810). Pattern D. A
   `scale_fill_*` applied to a `color` aesthetic — silently does nothing, which
   is precisely why it deserves an exercise.

### 04-4-Misc — add 3

webr is already configured and unused.

1. **patchwork** (after §Patchwork, ~line 177). Pattern B. Three figures in a
   2-row layout with `+`, `/`, and `plot_layout()`.
2. **Factor ordering** (after §Change the order, ~line 291). Pattern B. Bar chart
   sorted by value rather than alphabetically. Extremely common need, and it is
   really a factor-levels exercise wearing a ggplot2 costume.
3. **`ggsave()`** (after §Image resolution, ~line 1660). Pattern E. Export the
   same figure at two sizes and two dpi values, then compare file size and
   legibility. Assignments require submitted figures; this is currently taught
   and never practised.

## 5. Suggested order

Ranked by student pain per hour of authoring.

| # | Work | Why first |
|---|---|---|
| 1 | `02-1` (6, Pattern E) | Every failed submission traces here. No webr needed |
| 2 | `03-1` (5) | Causes the Assignment 1 support load |
| 3 | `04-3` theme + colour (5) | Largest untested block in Chapter 4 |
| 4 | `01` object types (6) | Conceptual core, and cheap — webr already configured |
| 5 | `02-4` (4) | Cross-refs and citations fail silently |
| 6 | `04-4` (3) | webr configured and idle; `ggsave` is assignment-critical |
| 7 | `03-2` piping + `across()` (4) | Deck is otherwise strong |
| 8 | `04-1`, `04-2`, `03-3` (8) | Filling in an already-working pattern |
| 9 | `02-2`, `02-3`, `02-0` (5) | Real gaps, lowest consequence |

Total ≈ 46 exercises. Items 1, 2, and 5 are text-only and need no rendering
checks beyond the deck itself.

## 6. Conventions for whoever writes these

- One exercise block per section, inside a `panel-tabset`. Never let an exercise
  span slides.
- Answers always `{r, eval = FALSE}` + `#| code-fold: true`. Never `webr-r`.
- Setup chunks get `#| autorun: true` so the student is not blocked by a step
  that is not the point of the exercise.
- **Run every answer before committing it.** The `03-2` revision log records an
  empty answer block, a wrong answer key, and an exercise naming a column its
  dataset did not have — all three shipped.
- Reuse datasets the deck already loaded. A new entry in `webr: packages:` costs
  every student load time.
- Add a `<details class="transcript">` block for each new exercise, matching the
  house voice — see [lecture-transcripts.md](lecture-transcripts.md). Chapters
  1–4 are fully transcribed, so an untranscribed exercise is visibly the odd one
  out.
