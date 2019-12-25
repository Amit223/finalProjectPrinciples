from Biography import BiograpyGetter

sorted_list_of_dates=[]
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

