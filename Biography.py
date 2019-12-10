#imports
from bs4 import BeautifulSoup
from urllib.request import urlopen
import urllib
import re
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
header = {'User-Agent': 'Mozilla/5.0'}

events_Dic = {"Born": 1, "Death": 2, "Marrige": 3, "Divorce": 4, "Film": 5, "Television": 6,
              "Music Video": 7}  # event-index
events_Pic_Dic = {}  # add pictures for each index
Actors_event = []  # {event year, event name , (optional) Description}

#links that works:
#https://en.wikipedia.org/wiki/Channing_Tatum
#https://en.wikipedia.org/wiki/Emma_Roberts
#https://en.wikipedia.org/wiki/Wentworth_Miller
#https://en.wikipedia.org/wiki/Alexander_Skarsg%C3%A5rd



# specify the url-todo in function
wiki = "https://en.wikipedia.org/wiki/Channing_Tatum"
# Query the website and return the html to the variable 'page'
page = urlopen(wiki)
# Parse the html in the 'page' variable, and store it in Beautiful Soup format
actorSoup = BeautifulSoup(page, 'lxml')

right_table = actorSoup.find('table', class_='wikitable plainrowheaders sortable')


#get birthdate
def getActorBirthDate(actorSoup):
    try:
        right_table = actorSoup.find('table', class_='infobox biography vcard')
        return right_table.find('span', class_='bday').string[0:4]
    except:
        return "not available"

#get spouces of actor- marrige date and divorce date
def getActorSpouses(actorSoup):
    try:
        listSpouses = []
        right_table = actorSoup.find('table', class_='infobox biography vcard')
        listCells = (right_table.find_all('td'))
        for i in range(0, len(listCells)):
            if listCells[i].find_all("abbr"):
                lst = listCells[i].find_all("div")
                for marrige in lst:
                    str = marrige.text
                    name = str[0:str.index('(')]
                    stop_index = 0  # for get married year
                    flag = False
                    if 'div' in str:
                        flag = True
                        stop_index = str.index(';')
                    else:
                        stop_index = str.index(')')
                    start_index=str.index('m.')
                    marrige_year = str[start_index+3: stop_index]
                    listSpouses.append([marrige_year, events_Dic["Marrige"], name])
                    if flag:  # divorced
                        div_year = str[str.index('div.')+5:str.index(')')]
                        listSpouses.append([div_year, events_Dic["Divorce"], name])
                break
        return listSpouses
    except:
        return "not available"


#find filmography/music/television table
def findTable(actorSoup,table_name):
    divs=actorSoup.find_all('div',class_="hatnote navigation-not-searchable")
    link=""
    for div in divs:
        link_temp=div.find('a').get('href')
        if "film" in link_temp or "Film" in link_temp:
            link=link_temp
            break
        if "video" in link_temp or "Video" in link_temp:
            link=link_temp
            break
    page = urlopen(urllib.request.Request('https://en.wikipedia.org' +link, headers=header))
    actor_film_soup=BeautifulSoup(page, 'lxml')
    return actor_film_soup.find('table',class_=table_name)




def getActorFilms(actorSoup):
    films=[]#each film: year,5,name of film
    #try:
    #if actorSoup.find('div',class_="hatnote navigation-not-searchable"):
        #filmograpy_table=findTable(actorSoup,"wikitable sortable")#movies table
    #else:
    filmograpy_tables=actorSoup.find_all('table', class_='wikitable sortable')
    if filmograpy_tables==None:
        filmograpy_tables = actorSoup.find_all('table', class_='wikitable sortable plainrowheaders')
    filmograpy_table=filmograpy_tables[0]
    for table in filmograpy_tables:
        if table.find(caption='Film'):
            filmograpy_table = table
            break
    filmograpy_lines=filmograpy_table.find_all('tr')
    filmograpy_lines.pop(0)
    for line in filmograpy_lines:
        cols=line.find_all('td')
        year=cols[0].text
        name=cols[1].text
        if '\n' in year:
            year=year[0:year.index('\n')]
        if '\n' in name:
            name=name[0:name.index('\n')]
        films.append([year,events_Dic["Film"],name])
    return films
    #except:
     #   return "Nan"

def getActorTV(actorSoup):
    series=[]#each film: year,5,name of film
    #try:
    #if actorSoup.find('div',class_="hatnote navigation-not-searchable"):
        #filmograpy_table=findTable(actorSoup,"wikitable sortable")#movies table
    #else:

    #tv_tables=actorSoup.find_all('table', class_='wikitable sortable')
    #if tv_tables==None:
     #   tv_tables = actorSoup.find_all('table', class_='wikitable sortable plainrowheaders')
    #tv_table=tv_tables[0]
    #for table in tv_tables:
        #if table.find(caption='Television'):
            #tv_table=table
            #break
    tv_table=None
    all_captions=actorSoup.find_all('caption')
    for caption in all_captions :
        cap_text=caption.get_text()
        if 'television' in cap_text.lower():
            tv_table = caption.find_parent('table')

    tv_lines=tv_table.find_all('tr')
    tv_lines.pop(0)
    for line in tv_lines:
        cols=line.find_all('td')
        year=cols[0].text
        name=cols[1].text
        if '\n' in year:
            year=year[0:year.index('\n')]
        if '\n' in name:
            name=name[0:name.index('\n')]
        series.append([year,events_Dic["Television"],name])
    return series
    #except:
     #   return "Nan"
print(getActorTV(actorSoup))
print(getActorFilms(actorSoup))