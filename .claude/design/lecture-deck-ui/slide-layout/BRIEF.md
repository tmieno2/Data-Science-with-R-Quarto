# BRIEF — slide layout, revealjs lecture decks

**Course:** AECN 896-05, *Data Science with R*. Graduate students in agricultural
economics, most of whom have never programmed. Decks are projected in a classroom
and also read alone afterwards, on a laptop, as notes. Both audiences matter; the
second one is why the transcript panels exist.

## What a slide has to hold

Nearly every content slide is one of five shapes:

1. **Title slide** — lecture number, title, chapter, instructor.
2. **Section divider** — one line, marks a new topic inside the deck.
3. **Concept slide** — a heading and three to six bullets, sometimes a callout.
4. **Code + output slide** — an R chunk and its printed result. The single most
   common slide in the course, and the tightest for space.
5. **Two-column slide** — code left, plot right; or before/after.

Most of these live *inside* a tabset (see `../tabs/`), so the layout must survive
having a tab strip above it and a transcript pill in the top-right corner.

## Hard constraints

- **Logical slide is 1050 × 700 px.** Not negotiable — it is reveal's canvas for
  these decks. Measured, not assumed.
- **Slides are already at the ceiling.** In `03-1-input-output.qmd`, multiple
  sections measure a `scrollHeight` of exactly 700px. `scrollable: true` is on,
  so they scroll instead of visibly breaking, and the overflow is invisible to
  the author. Anything a layout adds to normal flow is paid on every slide.
- **Type scale ships in `custom.scss`** at 16px root: h1 40, h2 35.2, h3 25.6,
  body 19.2, code block 16, output 14.4, callout title 22.4, footer 18.
- **Footer and logo are fixed furniture.** Footer is a centred 18px link at the
  bottom; the logo is 100 × 100 and has already been moved to the bottom-**left**
  by `transcript-support.html` so the right column stays free for transcripts.
- The `%>%` pipe is the course standard. Never show `|>` in a mockup.
- Body copy sits on white today. Any change of surface must keep code-block and
  output backgrounds distinguishable from it.

## What is wrong with the current version (see `current.html`)

- **The slide title fails contrast.** `h2` is `#f59219` on white — **2.13:1**,
  against a 3:1 minimum for large text. It is the most important text on the
  slide and the least readable, and it is the one thing a student at the back of
  a bright room has to be able to read.
- **Six accent hues with no system**: orange `#f59219` headings, green `#06a666`
  tabs, purple `#760dd8` inline code, magenta `#d60da1` bold, orange `#da792a`
  rules, red `#ec4343` editor chrome. Nothing tells a student that any of them
  mean anything, because they don't.
- **No vertical budget is expressed anywhere.** There is no visual signal, at
  authoring time, that a slide is about to overrun. The measured 700px slides
  prove that the author cannot currently tell.
- **19.2px body on a 1050px canvas is small for projection**, and the long
  full-width measure that comes with it (roughly 110 characters) is hard to read
  at the back of a room.
- **Nothing distinguishes the five slide shapes.** A section divider and a dense
  code slide are built from the same undifferentiated stack, so the deck reads as
  one long undifferentiated run.

## The question for the designer

How should a slide be laid out so that:

- the **title is legible from the back of a room** and passes AA;
- **code and its output read as one unit**, clearly separated from prose;
- there is a **visible vertical budget** — the author can see the ceiling coming;
- a **section divider looks nothing like a content slide**, so the deck has
  structure when read alone;
- and it still leaves the **top-right corner free** for the transcript pill and
  the **space above the content** for a tab strip?

## The three directions

- **`option-1-chalkline`** — smallest possible change. Keeps the current
  structure, fixes the palette to one ink plus one accent, replaces the orange
  heading with an ink heading over an accent rule. Lowest risk to 41 existing
  files.
- **`option-2-ledger`** — a title band across the head of the slide. The band
  replaces the h1/h2 stack, so it *buys back* vertical space rather than spending
  it, and gives the tab strip a defined place to sit.
- **`option-3-notebook`** — warm paper, 22px body, and a fixed margin column on
  the right for asides. Pays for larger type with a shorter measure. Also solves
  the transcript problem structurally: the panel has a column of its own instead
  of overlaying content.
