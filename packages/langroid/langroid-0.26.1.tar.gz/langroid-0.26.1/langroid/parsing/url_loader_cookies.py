import logging
from typing import List, no_type_check

import trafilatura
from playwright.sync_api import sync_playwright

from langroid.mytypes import DocMetaData, Document

logging.getLogger("trafilatura").setLevel(logging.ERROR)


def accept_cookies_and_extract_content(url: str) -> str:
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        page.goto(url)

        # List of possible selectors or texts on the cookie consent buttons
        possible_selectors = [
            'text="Accept"',
            'text="Agree"',
            'text="OK"',
            'text="Continue"',
        ]

        # Try to click each possible consent button
        for selector in possible_selectors:
            try:
                page.click(selector)
                print(f"Clicked {selector}")
                break  # If click is successful, break out of the loop
            except Exception:
                print(f"Could not click {selector}")

        # Extract and return the page's text content
        content = page.content()

        context.close()
        browser.close()
        content_str: str = content if isinstance(content, str) else ""
        return content_str


class URLLoader:
    """
    Load a list of URLs and extract the text content.
    Alternative approaches could use `bs4` or `scrapy`.

    TODO - this currently does not handle cookie dialogs,
     i.e. if there is a cookie pop-up, most/all of the extracted
     content could be cookie policy text.
     We could use `playwright` to simulate a user clicking
     the "accept" button on the cookie dialog.
    """

    def __init__(self, urls: List[str]):
        self.urls = urls

    @no_type_check
    def load(self) -> List[Document]:
        docs = []
        # converted the input list to an internal format
        for url in self.urls:
            html_content = accept_cookies_and_extract_content(url)
            text = trafilatura.extract(
                html_content,
                no_fallback=False,
                favor_recall=True,
            )
            if text is not None and text != "":
                docs.append(Document(content=text, metadata=DocMetaData(source=url)))
        return docs
