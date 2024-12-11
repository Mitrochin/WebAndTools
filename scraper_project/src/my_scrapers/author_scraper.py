import requests
from bs4 import BeautifulSoup
from src.models.author import Author


class AuthorScraper:
    def scrape_authors(self):
        base_url = "http://quotes.toscrape.com"
        authors = []

        response = requests.get(base_url)
        soup = BeautifulSoup(response.text, 'html.parser')

        for author_tag in soup.select('.author'):
            name = author_tag.text.strip()
            authors.append(Author(fullname=name, born_date="", born_location="", description=""))

        return authors

