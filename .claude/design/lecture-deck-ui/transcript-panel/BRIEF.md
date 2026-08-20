# BRIEF — lecturer transcript panel

A collapsible panel holding **what the lecturer says** about the slide, written
out in full. Collapsed it is a small pill in the slide's top-right corner;
clicked, it opens a panel over the slide. It is native `<details>`/`<summary>`,
so it works with no JavaScript, including in a self-contained export.

**Scale: 348 transcripts across 12 decks, Chapters 1–4.** Chapters 5–9 are not
started. Whatever is chosen here gets applied 348 times, so the CSS must stay in
one shared include (`lectures/transcript-support.html`) and the markup in the
`.qmd` must not change:

```html
<details class="transcript">
<summary>Lecturer transcript</summary>
…what the lecturer says…
</details>
```

## Who it is for

Two readers, with opposite needs:

- **The lecturer, live.** Reading from a projected or laptop screen while
  talking. Needs it *legible* and needs to find it fast.
- **The student, afterwards.** Reading the deck alone as notes. The transcript is
  the thing that turns a slide of bullets back into a lecture.

Nobody needs it visible while a slide is merely being presented, which is why it
collapses.

## Hard constraints

- **Collapsed, it must cost the slide zero vertical space.** This is why it is
  `position: absolute` today, and it is not negotiable — slides already measure
  700px of content.
- **It must not cover the tab row.** Transcripts usually live *inside* a tab, and
  the reader has to be able to switch tabs with the panel open. Today's panel
  starts at `top: 17%` precisely to clear the tab strip on the busiest slide.
- **It must dodge `custom.scss`.** That file styles *every* bare `<details>` with
  a grey `1px solid #aaa` border and padding, and pulls every `<summary>` with a
  negative margin, for Quarto's folded-code blocks. It is live and must not
  change. Any transcript CSS has to opt out explicitly — today's does, with a
  comment saying so.
- **The logo has already been moved** from bottom-right to `left: 56px` to keep
  the right-hand column clear. 56px clears reveal's menu button (x 8–43px).
- Open panels must close on slide change and on tab click, or a panel left open
  reappears over unrelated content. The existing script does this; keep it.

## What is wrong with the current version (see `current.html`)

- **10.56px type.** `0.55em` of a 19.2px base. On the projected slide that is
  ~12px of rendered height — the lecturer is reading their own script at a size
  chosen to make it unobtrusive for students, which is the wrong trade for the
  only person who reads it live.
- **The pill fails contrast.** `#06a666` text on white is **2.71:1**.
- **The pill looks like a tab.** Same green, same corner region, sitting a few
  pixels from a row of green tabs. It is a different kind of control and reads as
  one more tab.
- **Open, it covers the content it is about.** 36% of the slide width, overlaid
  on the right-hand column, with a shadow. On a two-column code/plot slide it
  lands directly on the plot.
- **The 17% top offset is a magic number** derived from one slide in `02-2`. Any
  slide with a taller tab row loses its tabs behind the panel.

## The question for the designer

How should the panel behave so that:

- the lecturer can **read it comfortably** while talking;
- it still costs **zero space** when closed;
- open, it **does not obscure the material it is describing**;
- the **tab row stays reachable** without a hard-coded offset;
- and the pill reads as a **different kind of object from a tab**?

## The directions

- **`option-1-chalkline`** — the pill becomes a small ink marker, and the open
  panel becomes a right rail that *pushes* nothing but sits on an opaque paper
  card with a scrim, at 13px. Anchored below the tab row by flow, not by a
  percentage.
- **`option-2-ledger`** — the control docks into the title band, and the panel
  opens as a **bottom drawer** across the full slide width. A drawer cannot
  collide with the tab row by construction, and the full width lets the type go
  up to 15px while staying under a third of the slide's height.
- **Notebook needs no panel at all.** In `../slide-layout/option-3-notebook.html`
  the slide already has a 232px margin column. The transcript becomes ordinary
  content in that column — always visible to whoever is reading, never overlaying
  anything, no absolute positioning, no magic offsets, and no fight with
  `custom.scss`. The cost is that the margin is then spoken for, and students see
  the transcript by default rather than on demand. If that trade is acceptable,
  it is by far the simplest of the three.
