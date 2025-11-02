import requests
from bs4 import BeautifulSoup

import json

url = 'http://quotes.toscrape.com' 

def parse_quotes(html_doc: requests.Response):
    soup: BeautifulSoup = BeautifulSoup(html_doc.content, 'html.parser')
    quotes_el = soup.select('[class*="quote"]')
    page_quotes = []

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

        page_quotes.append(quote_obj) # type: ignore
    

    
    return page_quotes



def parse_next_html_link(html_doc: requests.Response): # type: ignore
    soup: BeautifulSoup = BeautifulSoup(html_doc.content, 'html.parser')

    try:
        next_page_href = soup.find('li', class_='next').find('a')['href'] # type: ignore
        return(next_page_href) # type: ignore
        
    except AttributeError:
        print('All pages were parsed')
    

if __name__ == '__main__':

    root_url = 'http://quotes.toscrape.com'
    url = root_url
    next_url = ''
    quotes = []
    
    while True:
        url = root_url + next_url # type: ignore
        print(url) # type: ignore
        html_doc = requests.get(url) # type: ignore
        if html_doc.status_code == 200:
            page_quotes = parse_quotes(html_doc) # type: ignore
            [quotes.append(q) for q in page_quotes] # type: ignore
            next_url = parse_next_html_link(html_doc) # type: ignore
        
        if not next_url:
            break

    with open("quotes.json", "w", encoding="utf-8") as f:
        json.dump(quotes, f, ensure_ascii=False, indent=4)


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
