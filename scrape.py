import requests
from bs4 import BeautifulSoup

import json

url = 'http://quotes.toscrape.com' 

def parse_quotes(html_doc: requests.Response): # type: ignore
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
    
    return page_quotes # type: ignore



def parse_next_page_link(html_doc: requests.Response, mssg: str): # type: ignore
    soup: BeautifulSoup = BeautifulSoup(html_doc.content, 'html.parser')

    try:
        next_page_href = soup.find('li', class_='next').find('a')['href'] # type: ignore
        return(next_page_href) # type: ignore
        
    except AttributeError:
        print(f'All {mssg} were parsed')


def parse_authors_links(html_doc: requests.Response): # type: ignore
    soup = BeautifulSoup(html_doc.content, 'html.parser')
    authors_links_elements = soup.find_all('div', class_='quote')

    authors_links = []
    for el in authors_links_elements:
        href = el.find('a')['href'] # type: ignore
        authors_links.append(href) # type: ignore

    return authors_links # type: ignore


def parse_authors_info(author_url: str): # type: ignore
    author_info = {}
    html_doc = requests.get(author_url) # type: ignore
    soup = BeautifulSoup(html_doc.content, 'html.parser') # type: ignore

    fullname = soup.find('h3', class_='author-title').get_text(strip=True) # type: ignore
    author_info['fullname'] = fullname

    born_date = soup.find('span', class_='author-born-date').get_text(strip=True) # type: ignore
    author_info['born_date'] = born_date

    born_location = soup.find('span', class_='author-born-location').get_text(strip=True) # type: ignore
    author_info['born_location'] = born_location

    description = soup.find('div', class_='author-description').get_text(strip=True) # type: ignore
    author_info['description'] = description

    return author_info # type: ignore

    

if __name__ == '__main__':

    root_url = 'http://quotes.toscrape.com'
    url = root_url
    next_url = ''
    quotes = []
    
    while True:
        url = root_url + next_url # type: ignore
        html_doc = requests.get(url) # type: ignore
        if html_doc.status_code == 200:
            page_quotes = parse_quotes(html_doc) # type: ignore
            [quotes.append(q) for q in page_quotes] # type: ignore
            next_url = parse_next_page_link(html_doc, 'quotes') # type: ignore
        
        if not next_url:
            print('writing quotes')
            break
    
    

    with open("quotes.json", "w", encoding="utf-8") as f:
        json.dump(quotes, f, ensure_ascii=False, indent=4)

    next_page_url = ''
    authors_links = set() # type: ignore
    authors = []

    while True:
        url = root_url + next_page_url # type: ignore
        html_doc = requests.get(url) # type: ignore

        authors_links_from_one_page = parse_authors_links(html_doc) # type: ignore

        [authors_links.add(link) for link in authors_links_from_one_page] # type: ignore

        next_page_url = parse_next_page_link(html_doc, 'authors') # type: ignore
        if not next_page_url:
            print('writing authors')
            break

    for author_link in authors_links: # type: ignore
        author_info = parse_authors_info(root_url + author_link) # type: ignore
        authors.append(author_info) # type: ignore
    
    
    
    with open("authors.json", "w", encoding="utf-8") as f:
        json.dump(authors, f, ensure_ascii=False, indent=4)
    
    



# [
#     {
#         "fullname": "Steve Martin",
#         "born_date": "August 14, 1945",
#         "born_location": "in Waco, Texas, The United States",
#         "description": "Stephen Glenn \\"Steve\\" Martin is an American actor, comedian, writer, playwright, producer, musician, and composer. He was raised in Southern California in a Baptist family, where his early influences were working at Disneyland and Knott's Berry Farm and working magic and comedy acts at these and other smaller venues in the area. His ascent to fame picked up when he became a writer for the Smothers Brothers Comedy Hour, and later became a frequent guest on the Tonight Show.In the 1970s, Martin performed his offbeat, absurdist comedy routines before packed houses on national tours. In the 1980s, having branched away from stand-up comedy, he became a successful actor, playwright, and juggler, and eventually earned Emmy, Grammy, and American Comedy awards."
#     }
# ]

# with open("data.json", "w", encoding="utf-8") as f:
#     json.dump(data, f, ensure_ascii=False, indent=4)
