# Previewing and screenshotting revealjs decks

Notes from getting this to actually work. Every item here is a wall that was hit
and cleared — none of it is theoretical.

## Serve over HTTP, never `file://`

A rendered deck opened as `file:///.../02-2-Quarto-revealjs.html` renders **only
the footer, logo, and menu button**. The slides are blank. reveal.js loads as ES
modules, and CORS blocks module imports from `file://` origins.

```bash
cd docs && python3 -m http.server 8899
# then http://localhost:8899/lectures/Chapter-2-Quarto/02-2-Quarto-revealjs.html
```

This matters for the user too — tell them to use the URL, not to double-click the
file. `quarto preview` is the other option.

## Screenshotting in headless Chrome

Chrome is at `/Applications/Google Chrome.app/Contents/MacOS/Google Chrome`.

### The slides rasterize blank by default

With plain `--headless=new --disable-gpu`, captures come out blank even though
the DOM is correct — `Reveal.isReady()` is true, sections are present, the `<h1>`
has a sane bounding rect and dark text on white. reveal's transformed
`.reveal .slides` layer simply is not rasterized. These flags fix it:

```
--headless=new
--use-gl=swiftshader --enable-unsafe-swiftshader
--run-all-compositor-stages-before-draw
--disable-new-content-rendering-timeout
--force-color-profile=srgb
```

Note `--disable-gpu` is **removed** — it is part of the problem.

Also call `Emulation.setDeviceMetricsOverride` before navigating, or the viewport
is wrong.

### Prefer `?print-pdf` for per-slide shots

Even with the flags above, navigating with `Reveal.slide()` and capturing the
live view is fragile: the incoming slide's transform layer may not paint.

Appending `?print-pdf` to the URL puts reveal in print view, where every slide is
a static page in normal document flow with no transforms. Then enumerate
sections, take their bounding boxes, and use `Page.captureScreenshot` with a
`clip`. This is reliable, and it is the same layout path the deck's own
"export to PDF" tab teaches.

```js
// after navigating to `${url}?print-pdf` and waiting ~9s
const boxes = await evaluate(`[...document.querySelectorAll('.reveal .slides section')]
  .map(s => { const r = s.getBoundingClientRect();
              return {x: r.x + scrollX, y: r.y + scrollY, w: r.width, h: r.height}; })`);
await send('Page.captureScreenshot', {
  format: 'png', captureBeyondViewport: true,
  clip: {x: b.x, y: b.y, width: b.w, height: b.h, scale: 2},
});
```

In print view slide 0 is the title slide, and **`02-2` has a blank slide at
index 1** from its change-log comments, so content starts at index 2. Do not
assume index == slide number; match on `section.id` instead.

### Testing behaviour needs the live view

reveal's `slidechanged` only fires in normal mode, so functional tests must use
the live view (not `?print-pdf`). JavaScript evaluation works fine there even
when screenshots do not. Navigate by id rather than index:

```js
const secs = [...document.querySelectorAll('.reveal .slides > section')];
Reveal.slide(secs.findIndex(s => s.id === 'get-started'), 0);
```

When measuring an element inside a tabset, only the **active** tab's panel is
rendered; elements in hidden tabs report a 0×0 rect at position 0. Filter with
`offsetParent !== null` or you will measure a hidden one and misread the result.

## Useful measurements

Worth re-running rather than assuming, since they pin the transcript CSS:

- reveal's logical slide is **700px** tall; in print view sections measure
  1050×769.
- Tab bar bottom: **11.8%** of slide height on most slides, **16.4%** on "Useful
  Tools" (nested tabsets).
- Logo (`.slide-logo`): `position: fixed`, 100×100px, default `right: 12px;
  bottom: 0`.
- Menu button (`.slide-menu-button`): x 0.7–3.6% of viewport width.

## Finding which rule is doing something

Do not guess at CSS provenance. `CSS.getMatchedStylesForNode` over CDP gives the
exact selector and origin. That is how the mystery grey box around the transcript
pill was traced to the `// Answer box` rule in `lectures/custom.scss` rather than
a browser default.
