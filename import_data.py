from mongo_connection import db # type: ignore
import json

if __name__ == '__main__':

    quotes_collection = db['quotes'] # type: ignore
    authors_collection = db['authors'] # type: ignore

    with open('quotes.json', 'r') as f:
        quotes = json.load(f)

    quotes_collection.insert_many(quotes) # type: ignore

    with open('authors.json', 'r') as f:
        authors = json.load(f)

    authors_collection.insert_many(authors) # type: ignore



