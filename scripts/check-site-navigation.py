#!/usr/bin/env python3
"""Check that the generated sidebar and article archive are reachable."""

from html.parser import HTMLParser
from pathlib import Path
import sys


class LinkParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.links = []
        self.headings = []
        self.open_link = None
        self.open_heading = None

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        if tag == "a":
            self.open_link = {"attrs": attributes, "text": []}
        elif tag in {"h1", "h2", "h3"}:
            self.open_heading = {"attrs": attributes, "text": []}

    def handle_data(self, data):
        if self.open_link is not None:
            self.open_link["text"].append(data)
        if self.open_heading is not None:
            self.open_heading["text"].append(data)

    def handle_endtag(self, tag):
        if tag == "a" and self.open_link is not None:
            self.links.append(self.open_link)
            self.open_link = None
        elif tag in {"h1", "h2", "h3"} and self.open_heading is not None:
            self.headings.append(self.open_heading)
            self.open_heading = None


def parse(path):
    if not path.is_file():
        print(f"FAIL: generated page not found: {path}", file=sys.stderr)
        raise SystemExit(1)
    parser = LinkParser()
    parser.feed(path.read_text(encoding="utf-8"))
    return parser


index_path = Path(sys.argv[1] if len(sys.argv) > 1 else "_site/index.html")
archive_path = Path(sys.argv[2] if len(sys.argv) > 2 else "_site/archive/index.html")
index = parse(index_path)
archive = parse(archive_path)

archive_link = next(
    (
        link
        for link in index.links
        if "".join(link["text"]).strip() == "Archive"
    ),
    None,
)
if archive_link is None:
    print("FAIL: sidebar Archive link not found", file=sys.stderr)
    raise SystemExit(1)
if not archive_link["attrs"].get("href", "").endswith("/archive/"):
    print(
        "FAIL: sidebar Archive link does not point to /archive/ "
        f"(href={archive_link['attrs'].get('href')!r})",
        file=sys.stderr,
    )
    raise SystemExit(1)

archive_heading = next(
    (
        heading
        for heading in archive.headings
        if "".join(heading["text"]).strip() == "Archive"
    ),
    None,
)
if archive_heading is None:
    print("FAIL: archive page heading not found", file=sys.stderr)
    raise SystemExit(1)

post_link = next(
    (
        link
        for link in archive.links
        if "archive-post-title" in link["attrs"].get("class", "").split()
    ),
    None,
)
if post_link is None or not "".join(post_link["text"]).strip():
    print("FAIL: archive page contains no post title link", file=sys.stderr)
    raise SystemExit(1)

print("PASS: sidebar Archive link reaches an archive page with post titles")
