#imports
from bs4 import BeautifulSoup
from urllib.request import urlopen
import urllib
import re
import numpy as np
import pandas as pd
from PIL import Image
import requests
from io import BytesIO

header = {'User-Agent': 'Mozilla/5.0'}


events_Pic_Dic = {}  # add pictures for each index
Actors_event = []  # {event year, event name , (optional) Description}



###this class gets biography for singers using the url of them###
class BiograpyGetter():

    def __init__(self,url,discography_url):
        # Query the website and return the html to the variable 'page'
        page = urlopen(url)
        discograph_page=urlopen(discography_url)
        # Parse the html in the 'page' variable, and store it in Beautiful Soup format
        self.singerSoup = BeautifulSoup(page, 'lxml')
        self.discograpySoup=BeautifulSoup(discograph_page, 'lxml')
        #add dictionary of events and their index 
        self.events_Dic = {"Born": 1, "Death": 2, "Marrige": 3, "Divorce": 4, "Single": 5,
                      "Album": 6}  # event-index


    #get picture
    def getSingerPicture(self):
        images = self.singerSoup.select('table.infobox a.image img[src]')
        return images[0]['src']


    #get birthdate
    def getSingerBirthDate(self):
        try:
            right_table = self.singerSoup.find('table', class_='infobox biography vcard')
            return [right_table.find('span', class_='bday').string[0:4],self.events_Dic['Born'],"Born"]
        except:
            return []


    #get spouces of actor- marrige date and divorce date
    def getSingerSpouses(self):
        try:
            listSpouses = []
            right_table = self.singerSoup.find('table', class_='infobox biography vcard')
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
                        listSpouses.append([marrige_year, self.events_Dic["Marrige"], name])
                        if flag:  # divorced
                            div_year = str[str.index('div.')+5:str.index(')')]
                            listSpouses.append([div_year, self.events_Dic["Divorce"], name])
                    break
            return listSpouses
        except:
            return []


    #get main singles og actor
    def getSingerSingles(self):
        for caption in self.discograpySoup.find_all('caption'):
            if 'singles as lead artist' in caption.get_text() or 'List of singles' in caption.get_text():
                table = caption.find_parent('table')
                break
        cells=[]
        for tr in table.find_all('tr'):
            cells.append(tr)
        singles_dic=[] #year-5(singles)-name
        #remove the headlines
        cells.pop(0)
        cells.pop(0)
        i=0
        while i< len(cells):
            year=(cells[i].find('td').getText())
            # remove /n
            year=year[0:len(year)-1]
            #get number of singles in the same year
            if "span" in str(cells[i].find('td')):
                index=int(str(cells[i].find('td'))[13:14])
            else:
                index=1
            for j in range(0,index):
                if cells[i].find('th')!=None:
                    name=cells[i].find('th').getText()
                    #remove /n
                    name = name[0:len(name) - 1]
                    if "(" in name:
                        name=name[1:name.index("(")-1]+name[name.index("("):len((name))]
                        if 'featuring' in name[name.index("("):len(name)] or 'with' in name[name.index("("):len(name)]:#need to remove all ()
                            name=name[0:name.index("(")]

                    elif "[" in name:
                        name = name[1:name.index("[") - 1] + name[name.index("["):len((name))]
                        if 'Z' in name[name.index("["):len(name)] or 'Q' in name[name.index("["):len(name)] or 'T' in name[name.index("["):len(name)] or 'R' in name[name.index("["):len(name)]:
                            name=name[0:name.index("[")]
                    else:
                        name=name[1:len(name)-1]
                    singles_dic.append([year,self.events_Dic["Single"],name])
                    i+=1
                else:
                    i+=1
        return singles_dic


    #get albums of singer
    def getSingerStudioAlbums(self):
        for caption in self.discograpySoup.find_all('caption'):
            if 'List of studio albums' in caption.get_text():
                table = caption.find_parent('table')
                break
        cells=[]
        for tr in table.find_all('tr'):
            cells.append(tr)
        albums_dic=[]
        cells.pop(0)
        cells.pop(0)
        i=0
        while i< len(cells):
            year=(cells[i].find('td').getText())
            year=year.split('\n')[1].split(' ')
            if 'Released' in year[0]:
                year=year[3]
            else:
                break
            #make sure there is no other chars
            if (len(year) > 4):
                year = year[0:4]

            if cells[i].find('th')!=None:
                name=cells[i].find('th').getText()
                name = name[0:len(name) - 1]
                albums_dic.append([year,self.events_Dic["Album"],name])
                i+=1
            else:
                i+=1
        return albums_dic


