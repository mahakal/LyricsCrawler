import requests
from bs4 import BeautifulSoup

import random
import time

user_a_file = open('user_agent','r')
headers = [x for x in user_a_file.read().split('\n') ]
random.shuffle(headers)

def give_soup(url, p=None):
    try:
        r = requests.get(url,headers={'Connection' : 'close', 'User-Agent': random.choice(headers)},timeout=30, proxies=p)
    except:
        print(url)
        return None

    soup = BeautifulSoup(r.content,'lxml')
    return soup

def get_lyrics_link(url,prox):
    artist_song_links = []
    
    soup = give_soup(url,prox)

    a_tags = soup.find_all('a')
    for a_tag in a_tags:
        href = a_tag.get('href')
        if href != None and '/lyrics/' in href:
            href = href.replace('..','')
            artist_song_links.append(href)

    return artist_song_links

def get_lyrics_file(f_str):
    l = []
    with open(f_str,'r') as f:
        for x in f:
            l.append(x.replace('\n',''))
    return l

def get_proxydb():
    soup = give_soup('http://proxydb.net/?protocol=https&anonlvl=2&anonlvl=3&anonlvl=4')
    a = soup.find_all('tbody')[0].find_all('a')
    a = [{'https':'https://'+x.text} for x in a]
    prox = []
    '''for x in a:
        try:
            if x['https'].replace('https://','')[:-5] in requests.get('https://api.ipify.org',proxies=x,timeout=5).content.decode():
                prox.append(x)
        except:
            continue
    '''
    return a

proxy = get_proxydb()
random.shuffle(proxy)
#songs = get_lyrics_link('http://www.azlyrics.com/e/eminem.html',random.choice(proxy))
songs = get_lyrics_file('./link')

base_url = 'http://www.azlyrics.com'
count = 0

for song in songs:
    soup = give_soup(song, random.choice(proxy))
    if soup == None:
        continue
    
    divs = soup.find_all('div',attrs={'class':None}) 
    for div in divs:
        if len(div.text) and 'Verse' in div.text:
            lyrics = div.text
            lyrics = lyrics.replace('\n', ' ')
            lyrics = lyrics.replace('\r', ' ')
            lyrics = lyrics.replace(',', ' ')
            lyrics = lyrics.replace('[Verse 1:]',' ' )
            lyrics = lyrics.replace('[Verse 2:]',' ')
            lyrics = lyrics.replace('[Verse 3:]',' ')
            lyrics = lyrics.replace('[Chorus:]',' ')
            lyrics = lyrics.replace('...',' ')
            with open('lyrics','a') as file:
                file.write(lyrics+'\n')
            count += 1
            break
    #time.sleep(5)

print(count)
