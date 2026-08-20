#!/usr/bin/env python3
"""Recompute the mechanical fields of .claude/data/lecture-status.json.

Curated fields (title, chapter, on_website, every `status`, every `notes`) are
read from the existing JSON and written back untouched. Everything countable is
recounted from the .qmd sources, so the dataset cannot drift silently.

    python3 .claude/scripts/refresh-lecture-status.py           # rewrite the file
    python3 .claude/scripts/refresh-lecture-status.py --check    # exit 1 on drift

A deck that appears in lectures/ but not in the JSON is added with
status "unknown" for all three axes; a deck in the JSON whose file is gone is
reported and dropped.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / ".claude" / "data" / "lecture-status.json"
LECTURES = ROOT / "lectures"

CURATED = ("title", "chapter", "on_website", "status", "notes")

FENCE = re.compile(r"^(\s*)(`{3,})\s*\{([^}]*)\}\s*$")
CLOSE = re.compile(r"^\s*(`{3,})\s*$")
DIV_OPEN = re.compile(r"^:{3,}\s*(\{.*\}|\S+.*)$")
DIV_CLOSE = re.compile(r"^:{3,}\s*$")


def scan(path):
    """Count cells and .side-out regions, ignoring chunks nested in a fence."""
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()

    facts = {
        "knitr_cells": 0,
        "knitr_cells_side_out": 0,
        "webr_cells": 0,
        "webr_cells_side_out": 0,
        "side_out_regions": 0,
        "slides": sum(1 for ln in lines if ln.startswith("## ")),
        "tabsets": text.count("panel-tabset"),
        "transcripts": text.count('<details class="transcript">'),
        "transcript_support_included": "transcript-support.html" in text,
        "notebook_theme_applied": bool(
            re.search(r"^\s*theme:.*notebook\.scss", text, re.M)
        ),
    }

    open_ticks = None      # length of the fence we are inside, or None
    div_stack = []         # attribute strings of the open ::: divs

    for ln in lines:
        if open_ticks is not None:
            m = CLOSE.match(ln)
            if m and len(m.group(1)) >= open_ticks:
                open_ticks = None
            continue

        m = FENCE.match(ln)
        if m:
            open_ticks = len(m.group(2))
            engine = m.group(3).split(",")[0].strip().strip("=").lower()
            inside = any("side-out" in d for d in div_stack)
            if engine.startswith("webr"):
                facts["webr_cells"] += 1
                facts["webr_cells_side_out"] += inside
            elif engine == "r" or engine.startswith("r "):
                facts["knitr_cells"] += 1
                facts["knitr_cells_side_out"] += inside
            continue

        if DIV_CLOSE.match(ln):
            if div_stack:
                div_stack.pop()
        elif DIV_OPEN.match(ln):
            attrs = DIV_OPEN.match(ln).group(1)
            div_stack.append(attrs)
            if "side-out" in attrs:
                facts["side_out_regions"] += 1

    return facts


def build():
    old = json.loads(DATA.read_text(encoding="utf-8")) if DATA.exists() else {}
    by_path = {d["path"]: d for d in old.get("decks", [])}

    paths = sorted(
        p for p in LECTURES.rglob("*.qmd")
        if p.name not in ("index.qmd",)
    )

    decks, seen = [], set()
    for p in paths:
        rel = str(p.relative_to(ROOT))
        seen.add(rel)
        prev = by_path.get(rel, {})
        facts = scan(p)

        deck = {
            "path": rel,
            "title": prev.get("title", ""),
            "chapter": prev.get("chapter"),
            "on_website": prev.get("on_website"),
            "slides": facts["slides"],
            "tabsets": facts["tabsets"],
            "transcripts": {
                "status": prev.get("transcripts", {}).get("status", "unknown"),
                "count": facts["transcripts"],
                "support_included": facts["transcript_support_included"],
                "notes": prev.get("transcripts", {}).get("notes", ""),
            },
            "notebook_theme": {
                "status": prev.get("notebook_theme", {}).get("status", "unknown"),
                "in_theme_list": facts["notebook_theme_applied"],
                "notes": prev.get("notebook_theme", {}).get("notes", ""),
            },
            "side_by_side_output": {
                "status": prev.get("side_by_side_output", {}).get("status", "unknown"),
                "side_out_regions": facts["side_out_regions"],
                "webr_cells": facts["webr_cells"],
                "webr_cells_in_side_out": facts["webr_cells_side_out"],
                "knitr_cells": facts["knitr_cells"],
                "knitr_cells_in_side_out": facts["knitr_cells_side_out"],
                "notes": prev.get("side_by_side_output", {}).get("notes", ""),
            },
        }
        decks.append(deck)

    dropped = [p for p in by_path if p not in seen]
    new = dict(old)
    new["decks"] = decks
    return new, dropped, [d["path"] for d in decks if by_path.get(d["path"]) is None]


def main():
    check = "--check" in sys.argv
    new, dropped, added = build()

    for p in dropped:
        print(f"gone from disk, dropped from dataset: {p}", file=sys.stderr)
    for p in added:
        print(f"new deck, added with status 'unknown': {p}", file=sys.stderr)

    rendered = json.dumps(new, indent=2, ensure_ascii=False) + "\n"
    current = DATA.read_text(encoding="utf-8") if DATA.exists() else ""

    if rendered == current:
        print("lecture-status.json is up to date")
        return 0
    if check:
        print("DRIFT: counts in lecture-status.json no longer match the sources.",
              file=sys.stderr)
        print("Run: python3 .claude/scripts/refresh-lecture-status.py",
              file=sys.stderr)
        return 1
    DATA.write_text(rendered, encoding="utf-8")
    print(f"wrote {DATA.relative_to(ROOT)} ({len(new['decks'])} decks)")
    unknown = [
        f"{d['path']}: {axis}"
        for d in new["decks"]
        for axis in ("transcripts", "notebook_theme", "side_by_side_output")
        if d[axis]["status"] == "unknown"
    ]
    for u in unknown:
        print(f"  needs a curated status -> {u}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
