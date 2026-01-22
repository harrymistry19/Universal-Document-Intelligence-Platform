import requests
from bs4 import BeautifulSoup


def extract(url):
    response = requests.get(
        url,
        timeout=15,
        headers={"User-Agent": "Mozilla/5.0"}
    )
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    for tag in soup(["script", "style", "nav", "footer", "aside", "noscript"]):
        tag.decompose()

    title = soup.title.text.strip() if soup.title else ""

    headings = []
    for tag in soup.find_all(["h1", "h2", "h3"]):
        text = tag.get_text(strip=True)
        if text:
            headings.append(text)

    paragraphs = []
    container = soup.find("article") or soup.find("main") or soup.body
    for p in container.find_all("p"):
        text = p.get_text(strip=True)
        if len(text) > 40:
            paragraphs.append(text)

    return [{
        "title": title,
        "headings": headings,
        "paragraphs": paragraphs
    }]
