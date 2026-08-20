# BRIEF — tabsets (`::: {.panel-tabset}`)

Tabsets are the main organising device in these decks. A single slide holds four
or five tabs — *Objectives*, *Syntax*, *Example*, *Your turn* — and the lecturer
walks left to right through them. Almost every lecturer transcript in the course
lives inside a tab rather than on a bare slide.

## What the design has to handle

1. **A normal row** — three to five short labels.
2. **A long row** — real rows in `02-2` include *Creating a new slide*,
   *Include R codes and results*, *Exporting to PDF*. Five such labels is a live
   case, not a hypothetical.
3. **Labels containing inline code** — e.g. `` `read.csv()` ``, or
   "`echo` and `eval`".
4. **Nested tabsets** — a tabset inside a tab. Two rows, and the student must be
   able to tell which row they are looking at.
5. **A transcript pill in the top-right corner**, which the row must not collide
   with.

## Hard constraints

- **The row must never wrap.** A wrapped tab strip pushes every slide's content
  down by a whole row and silently costs ~26px on a canvas that is already full.
  Usable width is 1050 − 84 = **966px**. At 16.32px Source Sans Pro, that is
  roughly **120 characters of label** across the row once padding is counted.
  Every proposal below states its own budget.
- **Padding is already tight on purpose**: `.25em .7em` is Quarto's default, and
  `custom.scss` cuts it to `.15em .55em` (measured: 2.4 × 9px) specifically to
  keep long rows on one line. A proposal that grows padding must show the long
  row still fitting.
- **Do not put a `.fragment` or `.incremental` demo inside a tab.** Fragment
  content needs an arrow-key press to appear; inside a tab it renders blank and
  looks broken. This constrains what tabs are *used* for, and is worth stating on
  the slide-authoring side.
- Inline `code` inside a label must inherit the label's size and colour.
  `custom.scss` already patches this — without it, `.reveal code`'s absolute
  1.2rem and purple made "`echo` and `eval`" read as three separate things.
- The nested row must be visibly subordinate, not merely different.

## What is wrong with the current version (see `current.html`)

- **The active tab fails contrast.** White on `#06a666` is **2.71:1**, under the
  4.5:1 floor for text this size. The active tab is the one label that must be
  unambiguous, and it is the least readable one in the row.
- **The inactive tabs are `#52616b` on white (6.4:1) — more readable than the
  active one.** The hierarchy is inverted: the state that matters least is the
  easiest to read.
- **A solid green fill is a heavy way to say "selected".** On a slide whose
  content is otherwise white and quiet, the tab row is the loudest object,
  competing with the title for first attention.
- **The nested row repeats the same shape in a pale tint** (`#cfe9dd`), which
  reads as "disabled" rather than "one level down" — pale is the conventional
  signal for unavailable.
- The green is unrelated to every other hue in the theme, so a student has no
  reason to read it as meaning anything.

## The question for the designer

How should the tab row show **which tab is active** so that:

- the active label is the **most** readable thing in the row, not the least;
- the row is **quieter than the slide title**, since it is navigation, not content;
- a **nested row is obviously subordinate** without looking disabled;
- a five-label row of real course headings still fits on **one line**;
- and it survives a label that contains inline code?

## The three directions

- **`option-1-chalkline`** — the fill goes away entirely. Active is ink-weight
  plus a 2px accent underline. Cheapest row in vertical space, quietest on the
  slide, and the active label becomes the darkest text in the row.
- **`option-2-ledger`** — keeps the folder-tab metaphor but inverts the fix: the
  active tab is *paper-coloured* against a filled strip, so the selected tab is
  black-on-white and the unselected ones recede. This is the direction that pairs
  with the Ledger title band, where the strip lives inside the band.
- **`option-3-notebook`** — index-card tabs on the warm paper surface; active is
  a raised card with a solid accent edge on top.
