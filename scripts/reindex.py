"""
Deterministic index.md sync — runs after the LLM compile pass.

The LLM prompt asks the agent to maintain knowledge/index.md, but that is
unreliable: updated articles keep stale dates and new articles are sometimes
missing from the table (observed: 24 stale rows + 2 missing articles out of 90).
This script fixes the table from the filesystem, so the index never depends
on agent discipline:

- refreshes Updated date from the article file's mtime
- refreshes Compiled From from the article's frontmatter `sources:`
- appends rows for articles missing from the table (summary = first sentence)
- drops rows whose article file no longer exists

Existing summaries and row order are preserved.

Usage:
    uv run python scripts/reindex.py            # sync index.md
    uv run python scripts/reindex.py --dry-run  # report only
"""

from __future__ import annotations

import argparse
import datetime
import re
from pathlib import Path

KNOWLEDGE_DIR = Path(__file__).resolve().parent.parent / "knowledge"
INDEX_FILE = KNOWLEDGE_DIR / "index.md"
ARTICLE_DIRS = ("concepts", "connections")

ROW_RE = re.compile(
    r"^\|\s*\[\[([a-z0-9/_-]+)\]\]\s*\|\s*(.*?)\s*\|\s*(.*?)\s*\|\s*([0-9-]*)\s*\|\s*$"
)

HEADER = (
    "# Knowledge Base Index\n\n"
    "| Article | Summary | Compiled From | Updated |\n"
    "|---------|---------|---------------|---------|\n"
)


def _frontmatter_sources(text: str) -> str:
    """Extract `sources:` list from YAML frontmatter as a comma-joined string."""
    m = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
    if not m:
        return ""
    sources = re.findall(r'^\s*-\s*"?([^"\n]+)"?\s*$', m.group(1), re.MULTILINE)
    # keep only lines that came from the sources block (daily/… paths)
    return ", ".join(s.strip() for s in sources if s.strip().startswith("daily/"))


def _first_sentence(text: str) -> str:
    """First sentence of the article body (after frontmatter and title) for new rows."""
    body = re.sub(r"^---\n.*?\n---\n", "", text, flags=re.DOTALL)
    for line in body.splitlines():
        line = line.strip()
        if not line or line.startswith(("#", "|", ">", "-", "[[")):
            continue
        sentence = re.split(r"(?<=[.!?])\s", line)[0]
        return sentence[:110].replace("|", "/")
    return ""


def sync_index(dry_run: bool = False) -> dict:
    """Sync index.md with articles on disk. Returns change counters."""
    existing: dict[str, tuple[str, str, str]] = {}  # slug -> (summary, sources, date)
    order: list[str] = []
    if INDEX_FILE.exists():
        for line in INDEX_FILE.read_text(encoding="utf-8").splitlines():
            m = ROW_RE.match(line)
            if m:
                slug, summary, sources, date = m.groups()
                existing[slug] = (summary, sources, date)
                order.append(slug)

    on_disk: dict[str, Path] = {}
    for d in ARTICLE_DIRS:
        for f in sorted((KNOWLEDGE_DIR / d).glob("*.md")):
            on_disk[f"{d}/{f.stem}"] = f

    stats = {"refreshed": 0, "added": 0, "dropped": 0}
    rows: list[str] = []

    def build_row(slug: str, summary: str) -> str:
        f = on_disk[slug]
        text = f.read_text(encoding="utf-8")
        sources = _frontmatter_sources(text) or existing.get(slug, ("", "", ""))[1]
        date = datetime.date.fromtimestamp(f.stat().st_mtime).isoformat()
        return f"| [[{slug}]] | {summary} | {sources} | {date} |"

    for slug in order:
        if slug not in on_disk:
            stats["dropped"] += 1
            continue
        summary, _, old_date = existing[slug]
        row = build_row(slug, summary)
        if not row.endswith(f"| {old_date} |"):
            stats["refreshed"] += 1
        rows.append(row)

    for slug in on_disk:
        if slug not in existing:
            rows.append(build_row(slug, _first_sentence(on_disk[slug].read_text(encoding="utf-8"))))
            stats["added"] += 1

    if not dry_run:
        INDEX_FILE.write_text(HEADER + "\n".join(rows) + "\n", encoding="utf-8")
    return stats


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    s = sync_index(dry_run=args.dry_run)
    prefix = "[DRY RUN] " if args.dry_run else ""
    print(f"{prefix}index.md sync: refreshed={s['refreshed']} added={s['added']} dropped={s['dropped']}")
