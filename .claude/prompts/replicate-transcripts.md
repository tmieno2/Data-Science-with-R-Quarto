I want to add collapsible "Transcript" panels to the revealjs lecture decks in this project, and match the tabset styling, from a system already built and working in another course of mine.

## Reference implementation — read before writing anything

These files live outside this project. Read them; do not edit them.

- `/Users/tmieno2/Dropbox/TeachingUNL/Data-Science-with-R-Quarto/.claude/docs/lecture-transcripts.md` — the design, conventions, writing style, and the measurements behind every layout constant. READ THIS IN FULL FIRST.
- `/Users/tmieno2/Dropbox/TeachingUNL/Data-Science-with-R-Quarto/.claude/docs/revealjs-preview.md` — how to preview and screenshot revealjs decks. Saves an hour of blank captures.
- `/Users/tmieno2/Dropbox/TeachingUNL/Data-Science-with-R-Quarto/CLAUDE.md` — trap list. Items 1-3 apply to any Quarto revealjs project.
- `/Users/tmieno2/Dropbox/TeachingUNL/Data-Science-with-R-Quarto/lectures/transcript-support.html` — the shared CSS + JS to copy.
- `/Users/tmieno2/Dropbox/TeachingUNL/Data-Science-with-R-Quarto/lectures/Chapter-2-Quarto/02-2-Quarto-revealjs.qmd` — a finished deck with 31 transcripts. The model for tone and placement.
- `/Users/tmieno2/Dropbox/TeachingUNL/Data-Science-with-R-Quarto/lectures/custom.scss` — theme. Lines ~129-180 are the tabset styling; line ~195 is a trap (see below).

## What to build here

1. Transcript support file. Copy `transcript-support.html` into this project's shared lecture directory and wire it into each deck's YAML header:

       format:
         revealjs:
           include-in-header: ../transcript-support.html   # path relative to the .qmd

   Do NOT paste the CSS into a .qmd. Raw <style>/<script> above the first "##" becomes its own blank slide.

2. Transcripts. One `<details class="transcript">` per tab (or per slide if untabbed), placed at the top of that tab's content:

       ### Tab name

       <details class="transcript">
       <summary>Transcript</summary>

       What the lecturer says about this tab...

       </details>

       ...the slide content...

   Blank lines around the prose are required or Pandoc will not render the markdown inside the <details>.

   Follow the writing style section of lecture-transcripts.md exactly: second person addressing the class, 90-130 words, refer to what is on screen, say WHY not just WHAT, spell code out as speech ("bar-one-bar-two" not "|1|2"). Read several transcripts in 02-2-Quarto-revealjs.qmd before writing your own — matching the voice matters more than covering every detail.

3. Tabset styling, if this project's tabs do not already look like the reference. Copy custom.scss lines ~129-180: green #06a666 underline, filled accent on the active tab, smaller pale-green #cfe9dd nested tabs. Adapt the colours to this project's accent if it differs — and if you do, change the transcript pill colour to match, since it was picked to agree with the tabs.

## Re-measure; do not copy the constants blind

The layout numbers in transcript-support.html were measured against that project's theme and tab nesting. At minimum re-check, in THIS project:

- `top: 17%` on the open panel. It clears the tab bar, which ended at 11.8% of slide height on most slides and 16.4% on the one with nested tabsets. A different theme or deeper nesting moves this. If the panel covers tab names, this is why.
- `.slide-logo { left: 56px }`. The logo is moved bottom-left so the panel can use the right-hand column. 56px clears reveal's menu button at x 8-43px. Check where the logo and menu button actually sit here; if this project has no logo, drop the rule.
- Whether the details/summary opt-out is needed. In the reference project custom.scss styles EVERY bare <details> as an "answer box" (grey border, padding, negative summary margin), which silently wrapped the transcript pill in a grey rectangle. Check this project's scss for bare details/summary rules. Keeping the opt-out is harmless either way.

Verify with real measurements rather than by eye — revealjs-preview.md explains how. In particular, confirm the collapsed pill costs 0px of slide height; that property is the entire reason for the design, and it is easy to lose.

## Traps

1. Raw HTML above the first "##" becomes a blank slide. Includes long HTML comments, not just <style>.
2. Opening a rendered deck via file:// shows blank slides — reveal.js loads as ES modules and CORS blocks them. Serve over HTTP or use `quarto preview`.
3. reveal's logical slide is 700px tall and decks often already sit near it. Anything in normal flow costs that space on every slide, used or not.
4. Lecture decks that teach Quarto contain sample YAML that looks exactly like the real header. Match on a unique line when editing the real one.

## Before you start

Confirm with me:

- Which decks to do. Start with one, show me the result, then roll out.
- Who reads them and when. The reference project chose "students reviewing after class", which is what the overlay design serves. If the answer here is "presenter only", reveal's native `.notes` blocks are the right mechanism instead and none of this applies.

When the first deck is done, show me a screenshot of one slide with a transcript collapsed and the same slide with it open.
