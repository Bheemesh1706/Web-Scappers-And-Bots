import requests

from bs4 import BeautifulSoup



def content_gathering(uri): 
        pg = requests.get(uri)

        if pg.status_code == 200:
            contents = pg.content
            return contents
        else:
            print("Can't Retrieve the contente Due to some error")
        

def img_parser(content):

        img = BeautifulSoup(content,'html.parser')
        img_links = img.find_all('img')

        for x in img_links:
            print (x)



img_parser(content_gathering('https://en.wikipedia.org/wiki/Stock'))







