import requests
from bs4 import BeautifulSoup
import csv
import sys



def content_gathering(uri):   #Function to request the required web page html content
        pg = requests.get(uri)

        if pg.status_code == 200:
            contents = pg.content
            return contents
        else:
            print("Can't Retrieve the contente Due to some error")
        

def img_parser(content):   #Function to prase the img tag link and store it as a csv file 

        img = BeautifulSoup(content,'html.parser')
        img_links = img.find_all('img')
        link = []
        fields = ["Id","links"]
        filename = "img_link.csv"
        Id = 1


        for x in img_links:
            link.append([Id,x.get('src')])  #Extracting Links and adding it to the list
            Id+=1

        
        with open(filename, 'w') as csvfile:  #Creating the csv File and exporting the data to it
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(fields)
            csvwriter.writerows(link)



img_parser(content_gathering(sys.argv[1]))







