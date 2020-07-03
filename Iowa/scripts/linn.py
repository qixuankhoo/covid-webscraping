from bs4 import BeautifulSoup
import requests
import os 
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

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
    driver = webdriver.Chrome(executable_path="/Users/qixuan.khoo.19/Downloads/chromedriver")
    driver.get(url)
    time.sleep(1)
    result = driver.execute_script("return document.documentElement.outerHTML")
    return BeautifulSoup(result, 'html.parser')

def writeData(soup, tag, id_name):
    currdata = soup.find(tag, id_= id_name)
    f.write(currdata.get_text().encode('utf-8'))

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

COUNTY = "linn"
textFilePath = '../data/' + COUNTY + '.txt'
f = open(getFilePath(textFilePath), 'w')
links = []

#Scrape all PDFs from all resources on Linn County toolkits website 

url = 'https://www.linncounty.org/1400/Toolkits'
links = []
currSoup = scraping(url)
data = currSoup.find_all('div', class_='widgetBody imageBorder')
for item in data:
    link = item.find('a').get('href')
    links.append('https://www.linncounty.org/'+link)

for link in links:
    currSoup = scraping(link)
    section = currSoup.find_all('div', class_="fr-view")[1]
    items = section.find_all('li')
    pdfLinks = []
    print(len(items))
    for item in items:
        pdfLinks.append(item.find('a').get('href'))
    print(len(pdfLinks))
    for pdfLink in pdfLinks:
        try:
            data = getPDF(pdfLink, COUNTY)
        except:
            data = getPDF('https://www.linncounty.org/'+pdfLink, COUNTY)


    




