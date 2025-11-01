import requests
from bs4 import BeautifulSoup

import json

url = 'http://quotes.toscrape.com' 

def parse_quotes(html_doc: requests.Response):
    soup: BeautifulSoup = BeautifulSoup(html_doc.content, 'html.parser')
    quotes = []
    quotes_el = soup.select('[class*="quote"]')

    for el in quotes_el: # type: ignore

        quote_obj = {} # type: ignore

        tags_el = el.find_all('a', class_='tag')# type: ignore
        tags = []
        
        for t in tags_el:
            tag = t.get_text(strip=True) 
            tags.append(tag) # type: ignore
            quote_obj['tags'] = tags
        
        author = el.find('small', class_='author').get_text(strip=True) # type: ignore
        quote_obj['author'] = author
        
        quote = el.find('span', class_='text').get_text(strip=True) # type: ignore
        quote_obj['quote'] = quote # type: ignore

        quotes.append(quote_obj) # type: ignore
    
    with open("quotes.json", "w", encoding="utf-8") as f:
        json.dump(quotes, f, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    url = 'http://quotes.toscrape.com'
    html_doc = requests.get(url)
    if html_doc.status_code == 200:

        
        parse_quotes(html_doc)



# {
#     "tags": [
#       "humor",
#       "obvious",
#       "simile"
#     ],
#     "author": "Steve Martin",
#     "quote": "“A day without sunshine is like, you know, night.”"
#   }
# ]

# with open("data.json", "w", encoding="utf-8") as f:
#     json.dump(data, f, ensure_ascii=False, indent=4)
