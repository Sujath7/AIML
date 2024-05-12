#Sujath Hussain Mohammed Student ID 101551899

import os
import requests
import re
from bs4 import BeautifulSoup

def get_page():
    global url
    url = input("Enter the URL of a Medium article: ")  # Ask the user to input the URL
    
    # Define a custom User-Agent header
    headers = {
        'User-Agent': 'Your_User_Agent_String_Here'
    }
    
    res = requests.get(url, headers=headers)  # Pass headers parameter

    if not re.match(r'https?://medium.com/', url):
        print('Please enter a valid website, or make sure it is a medium article')
        sys.exit(1)
    
    res.raise_for_status()
    soup = BeautifulSoup(res.text, 'html.parser')
    return soup

def clean(text):
    rep = {"<br>": "\n", "<br/>": "\n", "<li>":  "\n"}
    rep = dict((re.escape(k), v) for k, v in rep) 
    pattern = re.compile("|".join(rep.keys()))
    text = pattern.sub(lambda m: rep[re.escape(m.group(0))], text)
    text = re.sub('\<(.*?)\>', '', text)
    return text

def collect_text(soup):
    text = f'url: {url}\n\n'
    para_text = soup.find_all('p')
    for para in para_text:
        text += f"{para.text}\n\n"
    return text

def save_file(text):
    if not os.path.exists('./scraped_articles'):
        os.mkdir('./scraped_articles')
    name = url.split("/")[-1]
    fname = f'scraped_articles/{name}.txt'
    
    with open(fname, 'w', encoding='utf-8') as file:
        file.write(text)
        
    print(f'File saved in directory {fname}')

if __name__ == '__main__':
    soup = get_page()
    text = collect_text(soup)
    save_file(text)