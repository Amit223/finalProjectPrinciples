from Biography import BiograpyGetter
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.dates as mdates
from datetime import datetime


singer_picture=None
def funcTester():
    singer="Justin_Timberlake"
    url="https://en.wikipedia.org/wiki/"+singer
    discography_url="https://en.wikipedia.org/wiki/"+singer+"_discography"
    bio=BiograpyGetter(url,discography_url)
    #test1:
    print(bio.getSingerPicture())
    #test2:
    print(bio.getSingerBirthDate())
    #test3:
    print(bio.getSingerSpouses())
    #test4:
    print(bio.getSingerSingles())
    #test 5:
    print(bio.getSingerStudioAlbums())


#this function opens gui and show singer's life
def main():
    sorted_list_of_dates = get_dates("Justin Timberlake")
    print(sorted_list_of_dates)
    visualization(sorted_list_of_dates,"Justin Timberlake")



def get_dates(singer_name):
    names=singer_name.split()
    full_name=names[0]+"_"+names[1]
    url = "https://en.wikipedia.org/wiki/" + full_name
    discography_url = "https://en.wikipedia.org/wiki/" + full_name + "_discography"
    bio = BiograpyGetter(url, discography_url)
    #get all info about singer
    singer_picture=bio.getSingerPicture()
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

def visualization(list,name):
    dates=[x[0]for x in list]
    dates = [datetime.strptime(d, "%Y") for d in dates]
    names=[x[2]for x in list]
    print( names)
    levels = np.array([-5, 5, -3, 3, -1, 1])
    fig, ax = plt.subplots(figsize=(8, 5))

    # Create the base line
    start = min(dates)
    stop = max(dates)
    ax.plot((start, stop), (0, 0), 'k', alpha=.5)

    # Iterate through releases annotating each one
    for ii, (iname, idate) in enumerate(zip(names, dates)):
        level = levels[ii % 6]
        vert = 'top' if level < 0 else 'bottom'

        ax.scatter(idate, 0, s=100, facecolor='w', edgecolor='k', zorder=9999)
        # Plot a line up to the text
        ax.plot((idate, idate), (0, level), c='r', alpha=.7)
        # Give the text a faint background and align it properly
        ax.text(idate, level, iname,
                horizontalalignment='right', verticalalignment=vert, fontsize=14,
                backgroundcolor=(1., 1., 1., .3))
    ax.set(title=name)
    # Set the xticks formatting
    # format xaxis with 3 month intervals
    ax.get_xaxis().set_major_locator(mdates.MonthLocator(interval=12))
    ax.get_xaxis().set_major_formatter(mdates.DateFormatter("%Y"))
    fig.autofmt_xdate()

    # Remove components for a cleaner look
    #plt.setp((ax.get_yticklabels() + ax.get_yticklines() +list(ax.spines.values())), visible=False)
    plt.show()

main()


