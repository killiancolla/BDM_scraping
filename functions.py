import requests
from bs4 import BeautifulSoup

def scraping_bdm(url:str='https://www.blogdumoderateur.com/') -> dict:
    response_bdm = requests.get(url)
    soup_bdm = BeautifulSoup(response_bdm.text)
    artilces = soup_bdm.find_all('article')

    data = {}

    for artilce in artilces:
        
        try:image_link = artilce.find('img')['data-lazy-src'] # Image
        except:
            try:image_link = artilce.find('img')['src']
            except: None
        
        title = artilce.h3.text                                 # Title

        try:link = artilce.find('a')['href']                    # Link
        except:link = artilce.parent['href']

        time = artilce.time['datetime'].split('T')[0]           # Time
       
        try:label = artilce.find('span', 'favtag color-b').text  # label
        except:
            try:label = artilce.parent.parent.parent.parent.h2.text
            except:label = None

        data[artilce['id']] = {
            'title' : title,
            'image' : image_link,
            'link'  : link,
            'label':  label,
            'time'  : time
        }
    return data