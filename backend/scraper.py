import requests
from bs4 import BeautifulSoup

def scrape_url(url: str) -> str:
    print(f"DEBUG: Scraping URL: {url}")
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Remove scripts, styles, nav, footer, etc.
        for element in soup(["script", "style", "nav", "header", "footer", "aside"]):
            element.decompose()
            
        # Extract meaningful textual content
        text = " ".join(soup.stripped_strings)
        print(f"DEBUG: Scraped {len(text)} characters from {url}")
        return text
    except Exception as e:
        print(f"DEBUG: Error scraping {url}: {e}")
        return ""
