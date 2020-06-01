#imports
from urllib import error
from urllib.parse import unquote, quote
from urllib.request import urlopen, Request, urlretrieve
from bs4 import BeautifulSoup
from requests import get
from os import system, path
from time import sleep
from platform import system as sys

#gets all cards from the card list in the cardset wiki in bulbapedia
def getCardsLinks(url):
    req = Request(url, headers={"User-Agent" : "Magic Browser"})
    html = urlopen(req) 
    bsObj = BeautifulSoup(html.read(),"html5lib")
    numbers="1234567890"
    cards = []
    cardSet = url.split("/")[-1]
    url = url.replace("/wiki/" + cardSet, "")
    cardSet= cardSet.replace("_(TCG)", "")
    
    for hyperlink in bsObj.find_all('a'):
        link = (hyperlink.get('href'))
        if link != None:
            if (cardSet + "_") in link and link[-1]==")" and link[-2] in numbers:
                if "http" not in link:
                    link = url + link
                cards.append(link)
                
    for link in cards:
        if link[-2]=="1" and link[-3]=="_":
            cards=cards[cards.index(link)::]
            break
    
    return cards, cardSet, url

#gets the image link from the specfic card pic wiki in bulbapedia
def getImageUrl(cardUrl, cardName, cardSet ,cardsetcaps):
    req = Request(cardUrl, headers={"User-Agent" : "Magic Browser"})
    html = urlopen(req)
    bsObj = BeautifulSoup(html.read(),"html5lib", from_encoding="ascii")
    
    for hyperlink in bsObj.find_all('a'):
        link = (hyperlink.get('href'))
        if link != None and "upload" in link:
            if "/" + cardName in link:
                card = "https:" + link
                break
            elif "/" + cardSetCaps in link:
                card = "https:" + link
                break
            elif "/" + cardSet in link:
                card = "https:" + link
                break
    return card

#clears the screen for stetic purposes (works in linux and windows)
def clear():
    if "windows" in sys().lower():
        system("cls")
    else:
        system("clear")  

#downloads and names the card with a nice format inside of a previously made folder with the name of the cardset in the same directory of this script
def downloadCard(card, set_name, name, idnumber, quantity):
    name=unquote(name)
    if "png" in card:
        file = idnumber.zfill(3) + "-" + name + ".png"
    else:
        file = idnumber.zfill(3) + "-" + name + ".jpg"
    req=get(card)
    with open(path.join(set_name, file), "wb") as image:
        image.write(req.content)
    clear()
    print(f"{set_name} \nDownloaded: {name} {idnumber}/{quantity}")
                     
#url of the cardset edit this variable to a different cardset link to change it
URL="https://bulbapedia.bulbagarden.net/wiki/Base_Set_(TCG)"
    
cardsLinks, card_set, URL = getCardsLinks(URL)

#url base to generate the images links according to bulbapedias format
URLbase= URL + "/wiki/File:"

#gets the 1st word of the cardset
cardSetFirstWord= card_set.split("_")[0]

#removes underscores from the crad set name
card_set = card_set.replace("_", "")

#gets the amount of cards in the cardset
cardsAmount=len(cardsLinks)

#id number that will be used to determine the number of the card as "Alakazam 1/102"
idn=0

#cardset name but only its initials
cardSetCaps = "".join([char for char in card_set if char.isupper()])

#makes a folder named as the cardset in the same directory of this script
system(f"mkdir {card_set}")

#uses all the previous stuff explained before to scrape all the card links using all the formats within the bulbapedia links (known to me)
#which includes finding scraping naming and downloading every HTTP error means the card doesnt use that format so it tests the next format
for card in cardsLinks:
    URLbase = URLbase.replace("archives", "bulbapedia")
    idn+=1
    name=card.split("/")[-1].split("(")[0].replace("_", "")
    if card_set=="BaseSet" and "Zapdos" in name:
        URLbase = URLbase.replace("bulbapedia", "archives")
    if card_set=="BaseSet" and "Farfetch" in name:
        name = unquote(name)
        name =  name.replace("'", "")
    if card_set=="BaseSet" and "Nidoran" in name:
        name = "Nidoran"
    if card_set=="BaseSet" and name=="GustofWind":
        name = "GustOfWind"
    URL=URLbase+name+card_set+str(idn)+".jpg"
    try:
        card = getImageUrl(URL, name, card_set, cardSetCaps)
        downloadCard(card, card_set, name, str(idn), cardsAmount)
    except KeyboardInterrupt:
        break
    except error.HTTPError:
        try:
            URL=URLbase+cardSetCaps+str(idn)+name+".jpg"
            card = getImageUrl(URL, name, card_set, cardSetCaps)
            downloadCard(card, card_set, name, str(idn), cardsAmount)
        except error.HTTPError:
            try:
                originalName=name
                upper=0
                indexes=[]
                name = unquote(name)
                for char in name:
                    if char.isupper():
                        upper+=1
                        if upper>1:
                            indexes.append(name.index(char))
                for indx in indexes:
                    name = name[0:indx] + "_" + name[indx::]
                name=quote(name)
                URL=URLbase+name+"_"+cardSetFirstWord+"_"+str(idn)+".jpg"
                card = getImageUrl(URL, name, card_set, cardSetCaps)
                downloadCard(card, card_set, name, str(idn), cardsAmount)
            except error.HTTPError:
                try:
                    name=originalName
                    URL=URLbase+card_set+str(idn)+name+".jpg"
                    card = getImageUrl(URL, name, card_set, cardSetCaps)
                    downloadCard(card, card_set, name, str(idn), cardsAmount)
                except error.HTTPError:
                    try:
                        URL=URLbase+name+".jpg"
                        card = getImageUrl(URL, name, card_set, cardSetCaps)
                        downloadCard(card, card_set, name, str(idn), cardsAmount)
                    except error.HTTPError:
                        try:
                            URL=URLbase+name+card_set+str(idn)+".png"
                            card = getImageUrl(URL, name, card_set, cardSetCaps)
                            downloadCard(card, card_set, name, str(idn), cardsAmount)
                        except error.HTTPError:
                            try:
                                URL=URLbase+cardSetCaps+str(idn)+name+".png"
                                card = getImageUrl(URL, name, card_set, cardSetCaps)
                                downloadCard(card, card_set, name, str(idn), cardsAmount)
                            except error.HTTPError:
                                try:
                                    originalName=name
                                    upper=0
                                    indexes=[]
                                    name = unquote(name)
                                    for char in name:
                                        if char.isupper():
                                            upper+=1
                                            if upper>1:
                                                indexes.append(name.index(char))
                                    for indx in indexes:
                                        name = name[0:indx] + "_" + name[indx::]
                                    name=quote(name)
                                    URL=URLbase+name+"_"+cardSetFirstWord+"_"+str(idn)+".jpg"
                                    card = getImageUrl(URL, name, card_set, cardSetCaps)
                                    downloadCard(card, card_set, name, str(idn), cardsAmount)
                                except error.HTTPError:
                                    try:
                                        name=originalName
                                        URL=URLbase+card_set+str(idn)+name+".png"
                                        card = getImageUrl(URL, name, card_set, cardSetCaps)
                                        downloadCard(card, card_set, name, str(idn), cardsAmount)
                                    except error.HTTPError:
                                        try:
                                            URL=URLbase+name+".png"
                                            card = getImageUrl(URL, name, card_set, cardSetCaps)
                                            downloadCard(card, card_set, name, str(idn), cardsAmount)
                                        except error.HTTPError as err:
                                            card = [name, idn, err]
                                            print(card)
 
#sleeps 3 seconds for having enough display time to read the log of the final card in the cardset
sleep(3)
