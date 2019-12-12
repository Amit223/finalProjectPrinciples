from Biography import BiograpyGetter

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
    x=5


funcTester()