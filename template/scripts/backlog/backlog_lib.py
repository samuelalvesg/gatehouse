"""Shared format rules for a file-per-item backlog. Standard library only.

Layout (see the backlog-items skill):
  docs/BACKLOG.md                  index: one table row per open item
  docs/backlog/<epic>/<slug>.md    one file per item, metadata line at the top

Edit ALLOWED_STATUSES and the paths below if your project uses other names.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

ALLOWED_STATUSES = [
    "📝 Registered",
    "🟡 In progress",
    "🟡 Partial",
    "✅ Done",
    "⛔ Dropped",
]
DONE_PREFIX = "✅"

INDEX_PATH = Path("docs/BACKLOG.md")
ITEMS_DIR = Path("docs/backlog")
DONE_PATH = Path("docs/DONE.md")

RE_META = re.compile(
    r"^> \*\*Epic:\*\* `([^`]+)` · \*\*ID:\*\* `([^`]+)` · \*\*Status:\*\* "
    r"(.+?)(?: · \*\*Registered:\*\* (\d{4}-\d{2}-\d{2}))?\s*$",
    re.M,
)
RE_INDEX_ROW = re.compile(
    r"^\| `([^`]*)` \| ([\w-]+) \| (.*?) \| (.*?) \| \[open\]\(([^)]*)\) \|\s*$"
)
RE_OPEN_BOX = re.compile(r"^\s*- \[ \]", re.M)
RE_DONE_BOX = re.compile(r"^\s*- \[x\]", re.I | re.M)


@dataclass
class Item:
    path: Path
    epic: str
    item_id: str
    status: str
    body: str
    title: str

    @property
    def is_done(self) -> bool:
        return self.status.startswith(DONE_PREFIX)

    @property
    def open_boxes(self) -> int:
        return len(RE_OPEN_BOX.findall(self.body))


def parse_item(path: Path, items_dir: Path) -> Item | None:
    """Return the parsed item, or None when the metadata line is missing."""
    text = path.read_text(encoding="utf-8")
    m = RE_META.search(text)
    if not m:
        return None
    title_m = re.search(r"^# (.+)$", text, re.M)
    return Item(
        path=path,
        epic=m.group(1),
        item_id=m.group(2),
        status=m.group(3).strip(),
        body=text[m.end():],
        title=title_m.group(1).strip() if title_m else path.stem,
    )


def load_items(root: Path) -> tuple[list[Item], list[Path]]:
    """Parse every item file. Returns (items, files without a metadata line)."""
    items_dir = root / ITEMS_DIR
    items: list[Item] = []
    broken: list[Path] = []
    for path in sorted(items_dir.rglob("*.md")):
        item = parse_item(path, items_dir)
        (items if item else broken).append(item or path)
    return items, broken


def index_rows(root: Path) -> list[tuple[str, str, str, str, str]]:
    """Return (id, epic, title, status, link) for each row of the index table."""
    rows = []
    for line in (root / INDEX_PATH).read_text(encoding="utf-8").splitlines():
        m = RE_INDEX_ROW.match(line)
        if m:
            rows.append(m.groups())
    return rows


def status_is_allowed(status: str) -> bool:
    return any(status == s for s in ALLOWED_STATUSES)
