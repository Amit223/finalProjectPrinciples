import urllib.request
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
import tkinter as tkr
from PIL import ImageTk, Image

currSingerName = "Lady Gaga"
events_Dic = {1:"Born" , 2:"Died",  3:"Married",  4:"Divorced",  5:"Single",
                       6:"Album"}  # event-index


#this function opens gui and show singer's life
def main():
    global currSingerName
    list_of_singers=sorted(['Lady Gaga','Ariana Grande','Selena Gomez','Justin Timberlake','Rihanna','Shawn Mendes','Billie Eilish',
                     'Camila Cabello','Post Malone','Beyonce','Dua Lipa'])
    gui(list_of_singers)



def singerVisualization():
    singer_name=currSingerName
    sorted_list_of_dates = get_dates(singer_name)
    sorted_list_of_dates=arrange_array(sorted_list_of_dates)
    visualization(sorted_list_of_dates,singer_name)



def gui(list_of_singers):
    master = tkr.Tk()
    master.geometry("650x350")
    master.title("Principles Project")
    master.configure(background='gold')

    set1 = tkr.Label(master, text ="Choose a singer you would like to know more about - ")
    set1.configure(font=("Arial",20))
    set1.grid(row=0, column=0)
    var=tkr.StringVar(master)
    set2=tkr.OptionMenu(master, var, *list_of_singers, command=callback)
    set2.configure(font=("Arial",20))
    set2.grid(row=1, column=0)
    set3 = tkr.Button(master, text="Submit name", command=singerVisualization)
    set3.configure(font=("Arial",16))
    set3.grid(row=2, column=0)

    path = "mic.jpg"
    img = ImageTk.PhotoImage(Image.open(path))
    tkr.Label(master, image=img).grid(row=3, column = 0)
    tkr.mainloop()


def close_window():
    tkr.destroy()

def callback(selection):
    global currSingerName
    currSingerName = selection

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
    singer_picture=bio.getSingerPicture()
    #image = urllib.URLopener()
    urllib.request.urlretrieve("https:"+singer_picture, "pic.jpg")
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

    #show pic
    im = Image.open('pic.jpg')
    height = im.size[1]

    # We need a float array between 0-1, rather than
    # a uint8 array between 0-255
    im = np.array(im).astype(np.float) / 255

    # With newer (1.0) versions of matplotlib, you can
    # use the "zorder" kwarg to make the image overlay
    # the plot, rather than hide behind it... (e.g. zorder=10)
    fig.figimage(im, 0, fig.bbox.ymax - height)

    #show graph
    plt.draw()
    plt.show()


main()


