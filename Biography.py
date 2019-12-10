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
wiki = "https://en.wikipedia.org/wiki/Justin_Timberlake_discography"
# Query the website and return the html to the variable 'page'
page = urlopen(wiki)
# Parse the html in the 'page' variable, and store it in Beautiful Soup format
actorSoup = BeautifulSoup(page, 'lxml')

right_table = actorSoup.find('table', class_='wikitable plainrowheaders sortable')


#get birthdate
def getSingerBirthDate(actorSoup):
    try:
        right_table = actorSoup.find('table', class_='infobox biography vcard')
        return right_table.find('span', class_='bday').string[0:4]
    except:
        return "not available"

#get spouces of actor- marrige date and divorce date
def getSingerSpouses(actorSoup):
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

def getSingerSingles(actorSoup):
    for caption in actorSoup.find_all('caption'):
        if 'singles as lead artist' in caption.get_text():
            table = caption.find_parent('table')
            break
    cells=[]
    for tr in table.find_all('tr'):
        cells.append(tr)
    cells.pop(0)
    cells.pop(0)
    print(cells)


getSingerSingles(actorSoup)
