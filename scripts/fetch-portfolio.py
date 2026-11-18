#!/usr/bin/env python3
"""Generate Jekyll data for public repositories with GitHub Pages enabled."""

import json
import os
from pathlib import Path
import sys
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import Request, urlopen


API_URL = os.environ.get("GITHUB_API_URL", "https://api.github.com").rstrip("/")
REPOSITORY = os.environ.get("GITHUB_REPOSITORY", "bendwarn/bendwarn.github.io")
OWNER = REPOSITORY.split("/", 1)[0]
OUTPUT = Path("_data/portfolio.json")


def get_json(url):
    headers = {"Accept": "application/vnd.github+json", "User-Agent": "jekyll-portfolio-builder"}
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    with urlopen(Request(url, headers=headers), timeout=30) as response:
        return json.load(response)


def collect_portfolio():
    projects = []
    page = 1
    while True:
        repos = get_json(f"{API_URL}/users/{quote(OWNER, safe='')}/repos?type=owner&per_page=100&page={page}")
        if not isinstance(repos, list):
            raise ValueError("GitHub repository response is not a list")
        for repo in repos:
            if not repo["has_pages"] or repo["private"] or repo["full_name"].lower() == REPOSITORY.lower():
                continue
            name = repo["name"]
            # The Pages API requires access to each repository. The workflow token
            # is scoped to this site, so use GitHub's standard URL when unavailable.
            try:
                pages = get_json(f"{API_URL}/repos/{quote(OWNER, safe='')}/{quote(name, safe='')}/pages")
                url = pages["html_url"]
            except HTTPError as error:
                if error.code not in (403, 404):
                    raise
                url = f"https://{OWNER}.github.io/{quote(name, safe='')}/"
            projects.append({"name": name, "description": repo["description"], "url": url, "repository_url": repo["html_url"]})
        if len(repos) < 100:
            break
        page += 1
    return sorted(projects, key=lambda project: project["name"].casefold())


def main():
    try:
        projects = collect_portfolio()
        OUTPUT.parent.mkdir(parents=True, exist_ok=True)
        OUTPUT.write_text(json.dumps(projects, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    except (HTTPError, URLError, OSError, ValueError, KeyError) as error:
        print(f"Failed to generate portfolio: {error}", file=sys.stderr)
        return 1
    print(f"Generated portfolio with {len(projects)} projects")
    return 0


if __name__ == "__main__":
    sys.exit(main())
