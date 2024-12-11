import json
import sys
import os
from src.my_scrapers.author_scraper import  AuthorScraper
from src.my_scrapers.quote_scraper import QuoteScraper

sys.path.append(os.path.dirname(os.path.abspath(__file__)))


def save_json(data, file_path):
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


def main():
    author_scraper = AuthorScraper()
    quote_scraper = QuoteScraper()

    authors = author_scraper.scrape_authors()
    quotes = quote_scraper.scrape_quotes(authors)

    save_json([author.__dict__ for author in authors], 'data/authors.json')
    save_json([quote.__dict__ for quote in quotes], 'data/quotes.json')


if __name__ == '__main__':
    main()





