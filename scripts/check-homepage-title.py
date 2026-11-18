#!/usr/bin/env python3
"""Check that homepage post titles and comment links remain distinct."""

from html.parser import HTMLParser
from pathlib import Path
import sys


class HomepageTitleParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.open_elements = []
        self.title_links = []
        self.comment_links = []

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        classes = set(attributes.get("class", "").split())
        element = {
            "tag": tag,
            "attrs": attributes,
            "classes": classes,
            "text": [],
            "kind": None,
        }

        if tag == "a":
            in_post_title = any(
                item["tag"] in {"h1", "h2"} and "post-title" in item["classes"]
                for item in self.open_elements
            )
            if in_post_title:
                element["kind"] = "title"
            elif "post-comments" in classes:
                element["kind"] = "comment"

        self.open_elements.append(element)

    def handle_data(self, data):
        for element in self.open_elements:
            if element["tag"] == "a":
                element["text"].append(data)

    def handle_endtag(self, tag):
        for index in range(len(self.open_elements) - 1, -1, -1):
            if self.open_elements[index]["tag"] == tag:
                element = self.open_elements.pop(index)
                if element["kind"] == "title":
                    self.title_links.append(element)
                elif element["kind"] == "comment":
                    self.comment_links.append(element)
                return


def fail(message):
    print(f"FAIL: {message}", file=sys.stderr)
    raise SystemExit(1)


site_path = Path(sys.argv[1] if len(sys.argv) > 1 else "_site/index.html")
if not site_path.is_file():
    fail(f"homepage not found: {site_path}")

parser = HomepageTitleParser()
parser.feed(site_path.read_text(encoding="utf-8"))

if not parser.title_links:
    fail("homepage post title link not found")

for title_link in parser.title_links:
    title = "".join(title_link["text"]).strip()
    if not title:
        fail("homepage post title is empty")
    if "data-disqus-identifier" in title_link["attrs"]:
        fail(
            "Disqus target is attached to the post title link "
            f"(title={title!r}, href={title_link['attrs'].get('href')!r})"
        )

for comment_link in parser.comment_links:
    if not comment_link["attrs"].get("href", "").endswith("#comments"):
        fail("post-comments link must target #comments")
    if "data-disqus-identifier" in comment_link["attrs"]:
        fail("post-comments link still contains a Disqus identifier")

print("PASS: homepage post titles and comment links are separate")
