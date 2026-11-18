#!/usr/bin/env python3
"""Exercise repository pagination, filtering and Pages URL selection."""

import importlib.util
from pathlib import Path
import unittest
from unittest.mock import patch
from urllib.error import HTTPError

spec = importlib.util.spec_from_file_location("fetch_portfolio", Path(__file__).with_name("fetch-portfolio.py"))
portfolio = importlib.util.module_from_spec(spec)
spec.loader.exec_module(portfolio)


def repo(name, *, pages=True, private=False):
    return {"name": name, "full_name": f"bendwarn/{name}", "has_pages": pages,
            "private": private, "description": None, "html_url": f"https://github.com/bendwarn/{name}"}


class PortfolioTest(unittest.TestCase):
    def test_pagination_filtering_and_pages_fallback(self):
        first_page = [repo("bendwarn.github.io"), repo("private", private=True), repo("no-pages", pages=False)]
        first_page.extend(repo(f"unused-{i}", pages=False) for i in range(97))

        def fetch(url):
            if url.endswith("&page=1"):
                return first_page
            if url.endswith("&page=2"):
                return [repo("Custom"), repo("Standard")]
            if "/Custom/pages" in url:
                return {"html_url": "https://example.com/"}
            if "/Standard/pages" in url:
                raise HTTPError(url, 404, "Not Found", {}, None)
            self.fail(f"Unexpected URL: {url}")

        with patch.object(portfolio, "OWNER", "bendwarn"), patch.object(portfolio, "REPOSITORY", "bendwarn/bendwarn.github.io"), patch.object(portfolio, "get_json", side_effect=fetch):
            projects = portfolio.collect_portfolio()
        self.assertEqual([project["name"] for project in projects], ["Custom", "Standard"])
        self.assertEqual(projects[0]["url"], "https://example.com/")
        self.assertEqual(projects[1]["url"], "https://bendwarn.github.io/Standard/")

    def test_repository_api_errors_are_not_silently_ignored(self):
        with patch.object(portfolio, "get_json", side_effect=HTTPError("url", 403, "rate limited", {}, None)):
            with self.assertRaises(HTTPError):
                portfolio.collect_portfolio()


if __name__ == "__main__":
    unittest.main()
