from bs4 import BeautifulSoup
import requests
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

fileDir = os.path.dirname(__file__)
filePath = os.path.join(fileDir, "../data/cambridgeCopy.txt")
filePath = os.path.abspath(os.path.realpath(filePath))
f = open(filePath, "w")

COUNTY = "cambridge"

def getFilePath(path):
    fileDir = os.path.dirname(__file__)
    filePath = os.path.join(fileDir, path)
    filePath = os.path.abspath(os.path.realpath(filePath))
    return filePath

def scraping(url):
    print("Scraping from " + url)
    f.write("\n\n\n")
    f.write("Scraping from " + url + "\n\n\n")
    driver = webdriver.Chrome(executable_path="/Users/qixuan.khoo.19/Downloads/chromedriver")
    driver.get(url)
    time.sleep(1)
    result = driver.execute_script("return document.documentElement.outerHTML")
    return BeautifulSoup(result, 'html.parser')

def writeData(soup, tag, id_name):
    currdata = soup.find_all(tag, id_name)
    for i in range(len(currdata)):
        f.write(currdata[i].get_text().encode('utf-8'))

def findHref(data, url):
    for i in range(len(data)):
        for link in data[i].find_all('a'):
            if 'https' not in link.get('href'):
                links.append('https://www.cambridgema.gov'+link.get('href'))
            else:
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

""" 
#Scrape general info websites 
links = []
url = 'https://www.cambridgema.gov/covid19'
soup = scraping(url)
data = soup.find_all('a', class_='button')
for item in data:
    links.append('https://www.cambridgema.gov/'+item.get('href'))

for link in links:
    currSoup = scraping(link)
    f.write(currSoup.find('h1').get_text())
    writeData(currSoup, 'article', 'mainContent')
 """
#Scrape 'Updates' website
links = []
url = 'https://www.cambridgema.gov/covid19/updates'
soup = scraping(url)
section = soup.find('article', class_='mainContent')
data = section.find_all('a')
for item in data[6:]:
    link = item.get('href')
    try:
        data = getPDF('https://www.cambridgema.gov'+link, COUNTY)
    except:
        currSoup = scraping('https://www.cambridgema.gov/'+link)
        f.write(currSoup.find('h1').get_text())
        writeData(currSoup, 'article', 'mainContent')
    





