# BRIEF — callouts and answer boxes

Two components that end up doing the same job and currently look unrelated.

**Callouts** are Quarto's `::: {.callout-note}` blocks. The decks set
`callout-icon: false`, so a callout is a title, a body, and a thin coloured left
edge — nothing else distinguishes a note from a warning.

**Answer boxes** are bare `<details><summary>` blocks holding the solution to an
exercise. They are styled in `custom.scss` under the comment `// Answer box`.

## What they are for, pedagogically

Across the course these blocks carry four distinct meanings, and students need to
tell them apart at a glance from the back of a room:

1. **Context / aside** — "this is the same idea you saw in Chapter 2".
2. **Watch out** — the common error. "A path that works on your machine will not
   work on mine." These are the highest-value blocks in the course and are
   currently indistinguishable from asides.
3. **Try it** — an instruction to the student to do something now.
4. **Answer** — hidden until clicked, revealed after they have tried.

## Hard constraints

- **`custom.scss` styles every bare `<details>` and `<summary>`.** A grey
  `1px solid #aaa` border with padding, plus a negative margin on the summary. It
  is live — it also styles Quarto's `<details class="code-fold">` blocks — and it
  must not change. **Any new `<details>` component has to opt out explicitly**,
  the way `transcript-support.html` already does.
- Callout title is 22.4px, body 19.2px. Both come from `custom.scss` and both are
  already tuned for the slide.
- `callout-icon: false` is set per deck. A design that depends on icons would
  have to turn them back on in 12 files, and Quarto's icons are generic — prefer
  not to.
- A callout has to survive being inside a tab and beside a transcript pill.
- Space: a callout on a slide that is already at 700px is the thing that pushes it
  over. Vertical cost per block is a design constraint, not an afterthought.

## What is wrong with the current version (see `current.html`)

- **With icons off, type is carried by a 3px coloured edge alone** — and the four
  meanings above are not mapped to four treatments. A "watch out" and an "aside"
  look the same at a glance, which inverts their importance.
- **The answer box is grey `#aaa`** — the visual language of a disabled control.
  It is the one block in the course that a student is meant to *interact* with,
  and it looks the least interactive.
- **The answer box belongs to no family.** It shares nothing with the callouts
  even though it is doing the fourth job in the same list.
- **A collapsed answer box gives no sense of what is inside** — no indication
  whether it is one line or fifteen, so a student cannot tell whether opening it
  costs them the rest of the slide.
- Nothing in either component acknowledges the vertical budget: a default Quarto
  callout costs roughly 90px of flow on a canvas with none to spare.

## The question for the designer

How should these blocks be designed so that:

- the **four meanings are distinguishable at a glance**, without icons;
- **"watch out" outranks "aside"** visually, matching its teaching value;
- the **answer box reads as inviting and as part of the same family**;
- each block states its **vertical cost**, and the cheap variants are genuinely
  cheap;
- and every `<details>` **opts out of the global rule** rather than fighting it?

## The directions

- **`option-1-chalkline`** — rules and weight only, no fills. Four roles
  distinguished by rule weight and a small uppercase label. Cheapest in vertical
  space; ~52px for a one-line block against Quarto's ~90px.
- **`option-2-ledger`** — a label chip in the top-left of a bordered block,
  matching the Ledger title band. More structural, costs more, reads harder from
  the back of the room.
