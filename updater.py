import requests
from bs4 import BeautifulSoup
import json
import time
import threading

def scrape_hsbc_loans(keywords=None):
    """Scrape HSBC UK loans page and filter by keywords if provided."""
    url = "https://www.hsbc.co.uk/loans/"
    try:
        resp = requests.get(url, timeout=10)
        soup = BeautifulSoup(resp.text, "html.parser")
        products = []
        for section in soup.find_all("section"):
            title = section.find("h2")
            desc = section.find("p")
            if title and desc:
                text = f"{title.text.strip()} {desc.text.strip()}"
                if not keywords or any(kw.lower() in text.lower() for kw in keywords):
                    products.append({
                        "text": text,
                        "source": url,
                        "date": ""
                    })
        return products
    except Exception as e:
        print(f"Error scraping HSBC loans: {e}")
        return []

def scrape_hsbc_news():
    # Example: Scrape HSBC news page
    url = "https://www.hsbc.com/news-and-media"
    try:
        resp = requests.get(url, timeout=10)
        soup = BeautifulSoup(resp.text, "html.parser")
        news_items = []
        for article in soup.find_all("article"):  # Example selector
            headline = article.find("h2")
            summary = article.find("p")
            if headline and summary:
                news_items.append({"headline": headline.text.strip(), "summary": summary.text.strip()})
        return news_items
    except Exception as e:
        print(f"Error scraping HSBC news: {e}")
        return []

def update_knowledge_base():
    # Load current knowledge base
    try:
        with open("hsbc_loan_knowledge.json", "r") as f:
            kb = json.load(f)
    except Exception:
        kb = {}
    # Scrape new data
    products = scrape_hsbc_loans()
    news = scrape_hsbc_news()
    # Update knowledge base
    if products:
        kb["scraped_loan_products"] = products
    if news:
        kb["latest_news"] = news
    # Save updated knowledge base
    with open("hsbc_loan_knowledge.json", "w") as f:
        json.dump(kb, f, indent=2)
    print("Knowledge base updated.")

def periodic_update(interval_hours=24):
    def run():
        while True:
            update_knowledge_base()
            time.sleep(interval_hours * 3600)
    thread = threading.Thread(target=run, daemon=True)
    thread.start()

# To start periodic updates, call periodic_update() from app.py
