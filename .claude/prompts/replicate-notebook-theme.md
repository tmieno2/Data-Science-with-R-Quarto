I want to apply the "Notebook" slide theme to the Quarto revealjs lecture decks in this project. It is already built and working in another course of mine. Your job is to port it here, verify it actually took effect, and report what you changed.

## Reference files — read before writing anything

These live outside this project. Read them; do not edit them. If you cannot reach this path, stop and ask me to copy the files over.

- `/Users/taromieno/Library/CloudStorage/Dropbox/TeachingUNL/Data-Science-with-R-Quarto/lectures/notebook.scss` — THE THEME. 615 lines, and roughly half of it is comments explaining why each constant is what it is. Read it in full before you copy it. Do not strip the comments.
- `/Users/taromieno/Library/CloudStorage/Dropbox/TeachingUNL/Data-Science-with-R-Quarto/lectures/custom.scss` — the base theme it layers on top of. You need lines ~195 (answer boxes) and ~217-330 (WebR side-by-side) to understand the two couplings described below.
- `/Users/taromieno/Library/CloudStorage/Dropbox/TeachingUNL/Data-Science-with-R-Quarto/lectures/Chapter-3-DataWrangling/03-2-data-wrangling-dplyr.qmd` — a deck running the finished theme. Use it as the reference for a correct YAML header.
- `/Users/taromieno/Library/CloudStorage/Dropbox/TeachingUNL/Data-Science-with-R-Quarto/CLAUDE.md` — trap list. Items 1, 3, 4 and 5 apply to any Quarto revealjs project.

## What the theme is

One SCSS file, `notebook.scss`, containing nothing but a `/*-- scss:rules --*/` block. No variables layer, no imports, no dependency on any other file being present. It is added as the LAST entry in a deck's `theme:` list, so it overrides whatever came before it.

Because it is purely additive, removing it from a deck's `theme:` list returns that deck to exactly its previous appearance. There is no migration and no rollback procedure. That property is worth preserving — keep any project-specific changes in your own scss file rather than editing `notebook.scss`.

What it changes:

- **Surface.** Warm paper background (`#fbf9f3`) instead of white, near-black ink (`#22201b`).
- **Headings.** `h2` becomes ink with a hairline rule under it, at `2rem` instead of `2.2rem`. The rule replaces the colour that used to carry the structure. This gives back about 4px of vertical space on every content slide.
- **Contrast fixes.** Several base colours in the original theme failed WCAG at the size they were used: `h2` orange at 2.13:1, `p > strong` pink at 4.05:1, active tab white-on-green at 2.71:1. The palette tokens at the top of the file carry their measured ratios in comments. If you re-brand, keep the floors: 4.5:1 for body text, 3:1 for large text.
- **Code and output.** Code blocks get a warm ground, R output gets a cool blue ground plus a 3px accent left edge. The two are separated by colour temperature rather than lightness, because a 2% lightness difference merges into one slab on a projector.
- **Tabsets.** Tabs become index cards sitting on a box that encloses the panel, so the strip and the content it selects read as one object. Nested tabsets drop the card and keep only a coloured top edge, so the two levels never look like the same control at two strengths.
- **Callouts.** Icons are off in these decks, so callout type was carried by 3px of colour alone. Roles are remapped to weight: `note` becomes the quietest block, `important`/`warning`/`caution` get a 5px sienna rule and a warm ground, `tip` gets an ink-blue rule.
- **`.side-out`.** An opt-in two-column layout, code left and printed output right. See below.

## Prerequisites

1. **Quarto revealjs.** The whole file is scoped to `.reveal`. It does nothing to `format: html` output.
2. **A `theme:` list that accepts a custom scss file.** If a deck uses `theme: default` alone, it becomes `theme: [default, notebook.scss]`.
3. **WebR is optional.** Roughly 150 lines target the `quarto-webr` extension's runtime DOM (`.qwebr-interactive-area` and friends). If this project does not use WebR, those rules match nothing and cost nothing. Leave them in; do not spend time deleting them.

## Install

1. Copy `notebook.scss` into this project's shared lecture directory — the same directory that holds the existing custom scss, so the relative paths in the decks stay parallel.

2. Add it as the last entry of every deck's `theme:` list:

       format:
         revealjs:
           theme: [default, ../custom.scss, ../notebook.scss]

   Two cautions here:

   - **Lecture decks that teach Quarto contain sample YAML in verbatim blocks that looks exactly like a real header.** Before editing by script, count matches per file (`grep -c` on the pattern) and confirm each file has exactly one. Where a file has more than one, edit the real header by hand.
   - Path prefixes vary between decks (`../custom.scss` vs `./../custom.scss`). Match whatever prefix that file already uses.

3. Render. Render single decks while iterating; a full site render is far more expensive.

4. Verify — see below. Do not skip this step and do not substitute exit codes for it.

## Verification: the only reliable check

A `quarto render` exit code of 0 tells you the deck rendered. It does not tell you the theme was applied, because a deck whose header never referenced the file renders perfectly happily without it.

Quarto compiles the whole `theme:` list into ONE hashed stylesheet at `docs/site_libs/revealjs/dist/theme/quarto-<hash>.css`, and different decks get different hashes depending on their other format options. So: read the hash out of the rendered HTML, then grep that stylesheet for a value only `notebook.scss` produces.

    cd docs
    for f in $(find lectures -name '*.html' -not -path '*_files*' | sort); do
      css=$(grep -o 'site_libs/revealjs/dist/theme/quarto-[a-f0-9]*\.css' "$f" | head -1)
      [ -z "$css" ] && { echo "n/a  $f"; continue; }
      grep -q 'f6efe6' "$css" && echo "NEW  $f" || echo "OLD  $f"
    done

`#f6efe6` is `$nb-tint-warm`, which appears only in this theme. Two things that will waste your time if you do not know them:

- **Do not grep the rendered HTML for CSS selectors.** The decks may contain JavaScript that mentions the same selector strings for unrelated reasons, so every deck reads as a match and the check silently passes for decks that do not have the theme at all. I lost a round to exactly this.
- **Do not grep the compiled CSS for a comment.** SCSS compilation strips `//` comments, so searching for a phrase from the source reads as a miss on every deck, including the ones that are correct.

## Opt-in features authors use per slide

Neither is global, on purpose.

**`.side-out`** — code left, printed output right:

    ::: {.side-out}
    ```{r}
    class(corn_yields_df)
    ```
    :::

Right when the output is narrow (a `class()`, a `dim()`, a short vector). Wrong when the output is a wide printed tibble, where half a slide is not enough columns. The same wrapper drives both knitr `{r}` cells and WebR `{webr-r}` cells, so an author does not have to remember which kind of cell is inside.

**`.side-out.tight`** — same, but the code column hugs its longest line and the output takes the rest. Use when the code is much shorter than the output, which is the common case for a one-line call.

## What the theme deliberately does not do

Do not "fix" these. Each was tried and reverted for a stated reason.

1. **Body type stays at the deck's existing size.** The design mockups run larger, but that is paid for by a margin column with a shorter line length, and the margin column needs per-slide markup. Raising type here, where nothing pays for it, pushes slides that already measure exactly 700px over the edge.
2. **Answer boxes are untouched.** In these decks they are bare `<details>`, which is the same element Quarto emits for folded code, so CSS cannot tell them apart. Restyling them means adding an opt-in class (`details.answer`) to every instance first.
3. **The transcript panel is untouched.** Its CSS lives in an inline `<style>` injected via `include-in-header`, which lands AFTER the theme stylesheet. At equal specificity the inline block wins, so rules written in the theme lose. A first attempt at this produced a collapsed pill SMALLER than the one it replaced.

## Two couplings to check against this project's own scss

1. **Code block width.** `$nb-code-w` is pinned to `90%` because the base theme gives WebR cells `.qwebr-interactive-area { width: 90% }`. The point is that a static `{r}` block and an interactive `{webr-r}` cell end up the same length. If this project uses a different width, or none, set `$nb-code-w` to match it.

2. **Any existing automatic side-by-side rule.** If this project's own scss already lays WebR cells out in two columns automatically — the source theme does this for cells that draw a plot, via `:has(.qwebr-output-graph-area canvas)` — that selector will out-rank `notebook.scss`'s `.side-out` version and install a grid with no `outbar` area. The visible symptom is the "Output" banner landing off the bottom-right corner and the gutter caret pointing at nothing. Fix by appending `:not(.side-out *)` to the existing selectors, exactly as the source project does at `custom.scss:269-270` and `:323-324`.

## Render discipline

- **Never pipe `quarto render`.** `quarto render 2>&1 | tail -6` reports `tail`'s exit code, not quarto's, so a render that halted partway looks like a success. Redirect to a log, then read the code:

      quarto render <file>.qmd > /tmp/render.log 2>&1; echo "EXIT: $?"

- A render can also fail for reasons that have nothing to do with the theme — a missing R package in a deck's first chunk, for instance. Read the log rather than assuming your edit caused it, and report such failures separately from theme work.

- Serving a rendered deck over `file://` shows a blank deck with only the footer. reveal.js loads as ES modules and CORS blocks module imports from `file://` origins. Serve over HTTP to look at it: `cd docs && python3 -m http.server 8899`.

## Report back

When done, tell me:

- Which decks now carry the theme, verified by the compiled-CSS check above rather than by exit code.
- Which decks you skipped or could not render, and why.
- Any place where this project's own scss conflicted with the theme, and what you did about it.
