from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import pandas as pd
import json

def webScraping(articleLink):
    f = open("data/article.txt", "w")

    # Webpagina link ophalen
    response = {}
    websites = ["bbc.com/news", "cnbc", "cnn.com"]
    usedWebsite = ""
    heading = ""
   
   # Kijken van welke nieuws website de link is
    for website in websites:
        if(articleLink.find(website) != -1):
            usedWebsite = website
            req = Request(articleLink, headers={'User-Agent': 'Chrome'})

    # Error response sturen als de link van een verkeerde website is
    if usedWebsite == "":
        response = {
            "status":False,
            "message":"Invalid link"
        }
        return response 

    
    try: 
        # webpagina lezen en omvormen door html parser 
        webpage = urlopen(req).read()
        soup = BeautifulSoup(webpage, features="html.parser")

        if(usedWebsite == "bbc.com/news"):
            # de tekst uit de webpagina halen en wegschrijven
            heading = soup.find('h1',attrs={'id':'main-heading'}).text
            divs = soup.find_all('div',attrs={'data-component':'text-block'})
            
            for div in divs:
                paragraph = div.find('p').text
                f.write(paragraph)
                f.write("\n")       

        if(usedWebsite == "cnbc"):
            # de tekst uit de webpagina halen en wegschrijven
            heading = soup.find('h1',attrs={'class':'ArticleHeader-headline'}).text
            divs = soup.find_all('div',attrs={'class':'group'})
            
            for div in divs:
                paragraphs = div.find_all('p')

                for paragraph in paragraphs:
                    f.write(paragraph.text)
                    f.write("\n")

        if(usedWebsite == "cnn.com"):
            # de tekst uit de webpagina halen en wegschrijven
            heading = soup.find('h1',attrs={'class':'pg-headline'}).text
            divs = soup.find_all('div',attrs={'class':'zn-body__paragraph'})
            
            for div in divs:
                paragraph = div.text
                f.write(paragraph)
                f.write("\n")

        # checken of er weldegelijk iets is opgehaald
        if(len(divs) == 0):
            response = {
                "status":False,
                "message":"Invalid article link, try another one"
            }
            return response
            
    except:
        # Error response bij een fout doorsturen 
        response = {
            "status":False,
            "message":"Something went wrong retrieving the article"
        }
        return response 
    
    # Succes response doorsturen
    response = {
        "status":True,
        "heading": heading,
        "message":"Article successfully retrieved"
    }
    return response 

    f.close()
