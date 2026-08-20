#!/usr/bin/env python3
"""Find nested code fences that knitr will execute by mistake.

knitr decides what is a code chunk by scanning lines, one at a time, for
```{...}. It has no idea that a fence can sit inside another fence. So a
```{r} block shown as an EXAMPLE inside a wider ```` fence is still executed,
unless the outer fence tells knitr to leave its contents alone:

    ````{verbatim}          <- outer fence, 4 backticks, verbatim engine
    ```{r}                  <- shown to the reader, NOT executed
    plot(x)
    ```
    ````

Written with a plain ```` outer fence, or ````markdown, the inner chunk runs.
It usually then fails, because example code refers to objects and packages the
document never loads.

Usage:
    python3 .claude/scripts/check-verbatim-fences.py [paths...]

Defaults to every tracked .qmd/.rmd outside docs/ and rendered *_files/.
Exits 1 if anything is found, so it works as a pre-render gate.
"""

import re
import sys
from pathlib import Path

FENCE = re.compile(r"^(\s*)(`{3,})(.*)$")

# knitr's own chunk.begin pattern, near enough: ```+ then {engine...}
CHUNK_HEADER = re.compile(r"^\{[a-zA-Z0-9_]+.*\}?\s*$")

SKIP_DIRS = {"docs", ".quarto", ".Rproj.user", "renv", ".git", "node_modules"}

# Outer-fence info strings that make knitr skip the contents.
SAFE_ENGINES = {"{verbatim}", "{embed}", "{=html}"}


def is_safe_outer(info: str) -> bool:
    info = info.strip()
    if not info:
        return False
    # ````{verbatim} or ````{verbatim lang="r"}
    if info.startswith("{"):
        engine = info.split()[0].rstrip("}") + "}"
        return engine in SAFE_ENGINES or info.split()[0] == "{verbatim"
    return False


def scan(path: Path):
    """Yield (line_no, outer_info, inner_info) for each nested chunk at risk."""
    findings = []
    stack = []  # list of (backtick_count, info)

    for n, raw in enumerate(path.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
        m = FENCE.match(raw)
        if not m:
            continue
        ticks, info = len(m.group(2)), m.group(3).strip()

        if stack:
            outer_ticks, outer_info = stack[-1]
            # A closing fence: at least as many backticks, nothing after them.
            if ticks >= outer_ticks and not info:
                stack.pop()
                continue
            # A nested opener. Only chunk-shaped ones are a problem.
            if CHUNK_HEADER.match(info) and not is_safe_outer(outer_info):
                findings.append((n, outer_info or "(none)", info))
        else:
            if not info and ticks >= 3:
                # A bare ``` with no open fence opens a plain block.
                stack.append((ticks, ""))
            else:
                stack.append((ticks, info))

    return findings


def main(argv):
    if argv:
        targets = [Path(a) for a in argv]
    else:
        root = Path(__file__).resolve().parents[2]
        targets = [
            p
            for p in list(root.rglob("*.qmd")) + list(root.rglob("*.rmd"))
            if not any(part in SKIP_DIRS or part.endswith("_files") for part in p.parts)
        ]

    total = 0
    for path in sorted(targets):
        for line_no, outer, inner in scan(path):
            total += 1
            try:
                shown = path.relative_to(Path.cwd())
            except ValueError:
                shown = path
            print(f"{shown}:{line_no}: {inner} nested in ``` fence '{outer}' -- will be executed")

    if total:
        print(f"\n{total} nested chunk(s) at risk. Change the OUTER fence to ````{{verbatim}}.")
        return 1

    print(f"No nested-fence problems in {len(targets)} file(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
