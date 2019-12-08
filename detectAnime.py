import re
import youtube_dl
from jikanpy import Jikan
import string
import time
import logging
import enchant
import sqlite3
from sqlite3 import Error

logging.basicConfig(filename='detectAnime-latest.log', filemode='w',format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S', level=logging.INFO)

def isAnimeKeyword(text):
    keywords = []
    with open('./assets/animekeywords.txt') as f:
        data = f.read().splitlines()
        for word in data:
            keywords.append(word)
    for word in keywords:
        for msgword in text.lower().split(' '):
            if word == msgword.lower():
                    logging.info(f'[DetectAnime] {msgword} includes anime because {word} is within it.')
                    return True
            if word == re.sub(r'[^\w]|[ ]', '', msgword.lower()).strip():
                logging.info(f'[DetectAnime] {msgword} includes anime because {word} was found in the text after removing all symbols.')
                return True
        for msgword in text.lower().split(' '):
            if not len(msgword) == len(word):
                continue
            for char in re.findall('[!@#$%^&*()_\-+=\\/|{}`~0-9]', msgword):
                for letter in list(string.ascii_lowercase):
                    newword = re.sub('[!@#$%^&*()_\-+=\\/|{}`~0-9]', letter, msgword)
                    if newword in keywords:
                        logging.info(f"[DetectAnime] {text} includes anime because {msgword} was changed to {newword} to become a keyword.")
                        return True
    for anime in topAnimes:
        if anime.casefold() in text.casefold():
            logging.info(f'[DetectAnime] {text} includes anime because {anime} is within it.')
            return True
    return isAnimeVid(text)

def isAnimeVid(text):
    try:
        url = re.search("(?P<url>https?://[^\s]+)", text).group("url")
    except AttributeError:
        return False
    if not 'youtu' in url: #not 'youtube' because of youtu.be urls
        return False
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': './assets/sounds/' + url.split('=')[1] + '.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }]
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        result = ydl.extract_info(url, download=False)
        with open('./assets/animekeywords.txt') as f:
            data = f.read().splitlines()
            for word in data:
                if f' {word} ' in result['title'].lower():
                    logging.info(f'[DetectAnime] The YouTube video {result["title"]} (URL: {url}) includes anime because {word} is within the title.')
                    return True
                elif f' word ' in result['description'].lower():
                    logging.info(f'[DetectAnime] The YouTube video {result["title"]} (URL: {url}) includes anime because {word} is within the description.')
                    return True
        for anime in topAnimes:
            if f' {anime.casefold()} ' in result['title'].casefold():
                logging.info(f'[DetectAnime] The YouTube video {result["title"]} (URL: {url}) includes anime because {anime} is within the title.')
                return True
            elif anime.casefold() in result['description'].casefold():
                logging.info(f'[DetectAnime] The YouTube video {result["title"]} (URL: {url}) includes anime because {anime} is within the description.')
                return True
    return False

def fetchAllAnimes():
    #jikan.season_later()
    #jikan.schedule()
    #top_anime = jikan.top(type='anime')
    #winter_2018 = jikan.season(year=2018, season='winter')
    animes = []
    jikan = Jikan()
    archive = jikan.season_archive()
    year = int(archive['archive'][0]['year'])
    d = enchant.Dict("en_US")
    while year >= 1975:
        for seasonname in archive['archive'][0]['seasons']:
            while True:
                try:
                    season = jikan.season(year=year, season=seasonname)
                    break
                except Exception as error:
                    if '429' in str(error):
                        print('[DetectAnime] Rate limited. Sleeping for 30secs...')
                        time.sleep(30)
                    else:
                        print(error)
                    pass

            for animesmall in season['anime']:
                id = animesmall['mal_id']
                while True:
                    try:
                        anime = jikan.anime(int(id))
                        break
                    except Exception as error:
                        if '429' in str(error):
                            print('[DetectAnime] Rate limited. Sleeping for 30secs...')
                            time.sleep(30)
                    else:
                        logging.error(error)
                    pass
                
                title = anime['title']
                engtitle = anime['title_english']
                japtitle = anime['title_japanese']
                synonym = anime['title_synonyms']
                try:
                    isValidTitle = len(title) > 4 and not d.check(title) and not d.check(re.sub('[^A-Za-z ]+', '', title))
                except Exception as e:
                    print('[DetectAnime] Error determining validity of title: ' + str(e) + '. Defaulting to False.')
                    isValidTitle = False
                if isValidTitle:
                    print(f'[DetectAnime] Appending "{title}" with id {id}. List size is now {len(animes)}.')
                    animes.append(title)
                    spacedreg = re.sub(r'[^\w]|[ ]', ' ', title)
                    if len(spacedreg) > 4:
                        animes.append(spacedreg)
                    blankedreg = re.sub(r'[^\w]|[ ]', '', title)
                    if len(blankedreg) > 4:
                        animes.append(spacedreg)
                try:
                    isValidTitle = len(engtitle) > 4 and not d.check(engtitle) and not d.check(re.sub('[^A-Za-z ]+', '', engtitle))
                except Exception as e:
                    print('[DetectAnime] Error determining validity of title: ' + str(e) + '. Defaulting to False.')
                    isValidTitle = False
                if isValidTitle:
                    print(f'[DetectAnime] Appending "{engtitle}" with id {id}. List size is now {len(animes)}.')
                    animes.append(engtitle)
                    spacedreg = re.sub(r'[^\w]|[ ]', ' ', engtitle)
                    if len(spacedreg) > 4:
                        animes.append(spacedreg)
                    blankedreg = re.sub(r'[^\w]|[ ]', '', engtitle)
                    if len(blankedreg) > 4:
                        animes.append(spacedreg)
                if not japtitle == None and len(japtitle) > 5:
                    print(f'[DetectAnime] Appending "{japtitle}" with id {id}. List size is now {len(animes)}.')
                    animes.append(japtitle)
                for syn in synonym:
                    if len(syn) > 4:
                        print(f'[DetectAnime] Appending synonym "{syn}" for "{title}". List size is now {len(animes)}.')
                        animes.append(syn)
                        spacedreg = re.sub(r'[^\w]|[ ]', ' ', syn)
                        if len(spacedreg) > 4:
                            animes.append(spacedreg)
                        blankedreg = re.sub(r'[^\w]|[ ]', '', syn)
                        if len(blankedreg) > 4:
                            animes.append(spacedreg)
                
        year -= 1
    animes = list(dict.fromkeys(animes))
    animes = removeDupStrings(animes)
    return animes

def removeDupStrings(myList):
    result=[]

    marker = set()
    for l in myList:
        ll = l.lower()
        if ll not in marker:   # test presence
            marker.add(ll)
            result.append(l)   # preserve order
    return result

def storeAnimesOnDisk(animes):
    if not topAnimes == None:
        animes += topAnimes
    animes = list(dict.fromkeys(animes)) #Remove duplicates
    conn = sqlite3.connect('./assets/animes.db', timeout=10)
    cursor = conn.cursor()
    for anime in animes:
        cursor.execute('SELECT id FROM animes ORDER BY id DESC LIMIT 1')
        highestid = [x[0] for x in cursor.fetchall()]
        if highestid != []:
            print(highestid[0])
            cursor.execute('INSERT INTO animes VALUES(?,?)', (int(highestid[0]) + 1, anime))
        else:
            cursor.execute('INSERT INTO animes VALUES(?,?)', (1, anime))
    conn.commit()
    conn.close()
        


def getAnimesFromDisk():
    
    conn = sqlite3.connect("./assets/animes.db", timeout=10)
    cursor = conn.cursor()
    cursor.execute('SELECT name FROM animes')
    fetchall = cursor.fetchall()
    conn.close()
    return [x[0] for x in fetchall]

topAnimes = getAnimesFromDisk()
if __name__ == '__main__':
    refresh = input('Refresh all animes? (Y/N):\n>')
    if refresh.lower() == 'y':
        confirm = input('THIS WILL DELETE ALL PRE-EXISTING ANIME TITLES IN THE DATABASE. ARE YOU SURE? (1/0):\n>')
        if confirm == str(1):
            conn = sqlite3.connect("./assets/animes.db", timeout=10)
            cursor = conn.cursor()
            cursor.execute('DELETE FROM animes')
            storeAnimesOnDisk(fetchAllAnimes())
    else:
        displayTopAnimes = input("Display entirety of topAnimes list? (Y/N):\n>")
        if displayTopAnimes.lower() == 'y':
            print(f'{str(topAnimes)}, length: {str(len(topAnimes))}')
        checkinarray = input("Go through entire isAnimeKeyword process or just check if in topAnimes list? (Y to go through entire function):\n?")
        if checkinarray.lower() == 'y':
            word = input("Enter keyword to be tested for anime:\n>")
            print(isAnimeKeyword(word))
        else:
            word = input("Enter keyword to be tested for anime:\n>")
            for anime in topAnimes:
                if anime.casefold() in word.casefold():
                    print('True')
                    break
        
    
