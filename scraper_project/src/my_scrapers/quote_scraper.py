import requests
from bs4 import BeautifulSoup
from src.models.quote import Quote


class QuoteScraper:
    def scrape_quotes(self, authors):
        base_url = "http://quotes.toscrape.com"
        quotes = []

        response = requests.get(base_url)
        soup = BeautifulSoup(response.text, 'html.parser')

        for quote_tag in soup.select('.quote'):
            text = quote_tag.select_one('.text').text.strip()
            author_name = quote_tag.select_one('.author').text.strip()
            tags = [tag.text for tag in quote_tag.select('.tags .tag')]

            author = next((author for author in authors if author.fullname == author_name), None)
            quotes.append(Quote(quote=text, author=author.fullname if author else "", tags=tags))

        return quotes

