# extractors/html_dynamic.py

from playwright.sync_api import sync_playwright

def extract(url):
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        raise ImportError(
            "Playwright is not installed. "
            "Install it using: pip install playwright && playwright install"
        )

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url)
        content = page.content()
        browser.close()

    return [{"html": content}]

