from bs4 import BeautifulSoup
import requests
import os 
from selenium import webdriver


# create a folder for PDFs
""" fileDir = os.path.dirname(__file__)
filePath2 = os.path.join(fileDir, "../data/" + COUNTY + "-PDF")
filePath2 = os.path.abspath(os.path.realpath(filePath2))
os.mkdir(filePath2) """

def getFilePath(path):
    fileDir = os.path.dirname(__file__)
    filePath = os.path.join(fileDir, path)
    filePath = os.path.abspath(os.path.realpath(filePath))
    return filePath

def scraping(url):
    print("Scraping from " + url)
    f.write("\n\n\n")
    f.write("Scraping from " + url + "\n\n\n")
    result = requests.get(url)
    return BeautifulSoup(result.content, 'html.parser')

def writeData(soup, tag, class_name):
    currdata = soup.find_all(tag, class_= class_name)
    for i in range(len(currdata)):
        f.write(currdata[i].get_text().encode('utf-8'))

def findHref(data):
    for i in range(len(data)):
        for link in data[i].find_all('a'):
            links.append(link.get('href'))

def getPDF(file_url, county):
    title = file_url.split('/').pop()
    fileName = title + '.pdf'
    filePath = getFilePath("../data/" + county + "-PDF")
    r = requests.get(file_url, stream = True)
    with open(os.path.join(filePath,fileName), "wb") as pdf:
        for chunk in r.iter_content(chunk_size=1024):
         if chunk:
             pdf.write(chunk)
    return "data/" + title
    
COUNTY = "fall_river"
textFilePath = '../data/' + COUNTY + '.txt'
f = open(getFilePath(textFilePath), 'w')
links = []

#Scrape all PDFs on Linn County Reopening-Guidance website
url = 'https://www.fallriverma.org/department/corona-virus-information/'
webpage = requests.get(url)
soup = BeautifulSoup(webpage.content, 'html.parser')
section = soup.find('div', class_='catchall-content')
data = section.find_all('a')
print(len(data))

""" for item in data:
    if '(PDF)' in item.get_text():
        link = item.find('a').get('href')
        try:
            getPDF(link, COUNTY)
        except:
            getPDF('https://www.fallriverma.org//'+link, COUNTY)


 """






    




