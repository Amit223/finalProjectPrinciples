from matplotlib.offsetbox import OffsetImage, AnnotationBbox

from Biography import BiograpyGetter
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import matplotlib.dates as mdates
from datetime import datetime
from PIL import Image
import requests
from io import BytesIO


events_Dic = {1:"Born" , 2:"Died",  3:"Married",  4:"Divorced",  5:"Single",
                       6:"Album"}  # event-index


#this function opens gui and show singer's life
def main():
    list_of_singers=['Lady Gaga','Ariana Grande','Selena Gomez','Justin Timberlake','Rihanna']
    singer_name='Justin Timberlake'
    sorted_list_of_dates = get_dates(singer_name)
    sorted_list_of_dates=arrange_array(sorted_list_of_dates)
    visualization(sorted_list_of_dates,singer_name)


def get_dates(singer_name):
    if ' ' in singer_name:
        names=singer_name.split()
        full_name=names[0]+"_"+names[1]
    else:
        full_name=singer_name
    url = "https://en.wikipedia.org/wiki/" + full_name
    discography_url = "https://en.wikipedia.org/wiki/" + full_name + "_discography"
    bio = BiograpyGetter(url, discography_url)
    #get all info about singer
    #singer_picture=bio.getSingerPicture()
    birthdate=bio.getSingerBirthDate()
    spouses=bio.getSingerSpouses()
    singles=bio.getSingerSingles()
    albums=bio.getSingerStudioAlbums()
    list=[]
    if len(birthdate)>0:
        list.append(birthdate)
    if len(spouses) > 0:
        list.extend(spouses)
    if len(singles) > 0:
        list.extend(singles)
    if len(albums) > 0:
        list.extend(albums)
    list.sort(key=lambda x: x[0])
    return list
#this function takes the events kind and put it in the title
def arrange_array(events):
    new_events=[]
    for event in events:
        index=event[1]
        if index==1:
            event_name=event[2]#do nothing
        elif index==2 or index==5 or index==6:
            event_name=event[2]+"("+events_Dic[index]+")"
        else:#3 or 4
            event_name=events_Dic[index]+" "+event[2]
        new_event=[event[0],index,event_name]
        new_events.append(new_event)
    return new_events


def visualization(list_,name):
    dates=[x[0]for x in list_]
    dates = [datetime.strptime(d, "%Y") for d in dates]
    names=[x[2]for x in list_]
    levels = np.array([-10,10,-9,9,-8,8,-7, 7,-6,6,-5,5, -4, 4,-3,3,-2,2, -1, 1])
    #levels=np.array(range(-10,11))
    fig, ax = plt.subplots(figsize=(20, 10))

    # Create the base line
    start = min(dates)
    stop = max(dates)
    num_of_years=stop.year-start.year+2
    ax.plot((start, stop), (0, 0), 'k', alpha=.5)

    #get x levels for the years
    hefresh=float(20)/float(num_of_years)
    all_years=list(range(start.year-1,stop.year+1))
    x_values=[]
    max_x=20
    for date in dates:
        year=date.year
        this_x=max_x-all_years.index(year)*hefresh#get the relative x position to thhe year
        x_values.append(this_x)

    # Iterate through releases annotating each one
    i=0
    for ii, (iname, idate) in enumerate(zip(names, dates)):
        level = levels[ii % 20]
        x_level=x_values[i]
        i+=1
        vert = 'top' if level < 0 else 'bottom'
        ax.scatter(idate, 0, s=100, facecolor='w', edgecolor='k', zorder=9999)
        # Plot a line up to the text
        ax.plot((idate, idate), (0, level), c='r', alpha=.7)
        # Give the text a faint background and align it properly
        ax.text(idate, level, iname,
                horizontalalignment='right', verticalalignment=vert, fontsize=10,
                backgroundcolor=(1., 1., 1., .3))
        #show pic
        #plt.figure()
        #ab = AnnotationBbox(im, (x_level, level), xycoords='data', frameon=False)
        #artists.append(ax.add_artist(ab))
        #ax.update_datalim(np.column_stack([x_level, level]))
        #ax.autoscale()
        #ab = AnnotationBbox(baby_img, (x_level, level), frameon=False)
        #ab = AnnotationBbox(im, (x_level, level), frameon=False)
        #ax.add_artist(ab)
        #ax.update_datalim(np.column_stack([x_level, level]))
        #ax.autoscale()

    ax.set(title=name)
    # Set the xticks formatting
    ax.get_xaxis().set_major_locator(mdates.MonthLocator(interval=12))
    ax.get_xaxis().set_major_formatter(mdates.DateFormatter("%Y"))
    fig.autofmt_xdate()

    # Remove components for a cleaner look
    plt.setp((ax.get_yticklabels() + ax.get_yticklines() +list(ax.spines.values())), visible=False)
    plt.draw()
    plt.show()


main()


