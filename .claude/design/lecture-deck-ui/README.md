# Lecture Deck UI

Design work for the revealjs lecture decks of **AECN 896-05, Data Science with R**.

Source repo: `/Users/tmieno2/Dropbox/TeachingUNL/Data-Science-with-R-Quarto`
Live theme: `lectures/custom.scss` + `lectures/transcript-support.html`

## Convention

Same as Black Type UI:

| File | Meaning |
|---|---|
| `BRIEF.md` | What the component is, what is wrong with it today, hard constraints, the question |
| `current.html` | Faithful reproduction of what ships today. No annotations, no improvements |
| `option-N-name.html` | A proposal |
| `option-N-name-ADOPTED.html` | Renamed once chosen |

Every mockup renders inside a `.stage` that is **exactly 1050 × 700 px** — reveal's
logical slide for these decks. If a proposal overflows, it visibly clips, which is
the point. `_deck.css` also draws an optional 640px "safe line" so you can see how
much room a layout actually leaves.

## The three directions

Each group offers the same three systems, so picking once gives a coherent whole
rather than four unrelated decisions.

- **Chalkline** — one ink, one accent, rules instead of fills. Quietest; smallest
  change to the existing decks.
- **Ledger** — a title band across the head of the slide, high contrast, solid
  folder tabs evolved from today's green ones. Most structured.
- **Notebook** — warm paper surface, larger type, a margin column for asides.
  Most "lecture notes"; largest departure.

Transcript and callout groups carry two options each (Chalkline and Ledger
treatments); the Notebook margin column changes the transcript problem so
fundamentally that it is described in the brief rather than mocked.

## Measured baseline

Taken from the rendered `03-1-input-output.html` in headless Chrome, not guessed.

| Element | Today | Selector |
|---|---|---|
| logical slide | 1050 × 700 px, screen scale 1.157× | `.reveal .slides` |
| h1 | 40px `#222` | `.reveal h1` |
| h2 | 35.2px **`#f59219`** | `.reveal h2` |
| h3 | 25.6px | `.reveal h3` |
| body / list | 19.2px, line-height 1.3 | `.reveal section li` |
| inline code | 19.2px `#760dd8` | `.reveal code` |
| code block | 16px on `#F7FDFF` | `code.sourceCode.r` |
| output | 14.4px on `#f8f2f6` | `.cell-output-stdout` |
| tab | 16.32px, padding 2.4 × 9px | `[role="tab"]` |
| active tab | white on `#06a666` | `[role="tab"][aria-selected]` |
| callout title / body | 22.4px / 19.2px | `.callout-title` |
| footer | 18px `#6f6f6f` | `.footer` |
| transcript | 10.56px, absolute top-right | `details.transcript` |

Root `rem` is 16px, so every `rem` in `custom.scss` is `value × 16`.
