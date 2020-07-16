# coding: utf-8
from bs4 import BeautifulSoup
import requests
import os 
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import random


def getFilePath(path):
    fileDir = os.path.dirname(__file__)
    filePath = os.path.join(fileDir, path)
    filePath = os.path.abspath(os.path.realpath(filePath))
    return filePath

def scraping(url):
    print("Scraping from " + url)
    f.write("\n\n\n")
    f.write("Scraping from " + url + "\n\n\n")
    driver = webdriver.Chrome()
    driver.get(url)
    time.sleep(1)
    result = driver.execute_script("return document.documentElement.outerHTML")
    return BeautifulSoup(result, 'html.parser')

def getPDF(file_url, county):
    title = file_url.split('/').pop()
    fileName = title + '.pdf'
    filePath = getFilePath("../data/" + county + "-PDF")
    r = requests.get(file_url, stream = True)
    try: 
        with open(os.path.join(filePath,fileName), "wb") as pdf:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:
                    pdf.write(chunk)
    except:
        fileName = 'mediaFile' + random.randint(1,10) + '.pdf'
        with open(os.path.join(filePath,fileName), "wb") as pdf:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:
                    pdf.write(chunk)
    return "data/" + title
    

COUNTY = "whatcom"

#create PDF folder for PDF files
try:
    filePath = getFilePath("../data/" + COUNTY + "-PDF")
    os.mkdir(filePath) 
except:
    print('PDF folder already exists!')
    
textFilePath = '../data/' + COUNTY + '.txt'
f = open(getFilePath(textFilePath), 'w')

#Scrape Covid-19 press releases
url = 'http://whatcomcounty.us/3377/Media-Press'
soup = scraping(url)
table = soup.find('tbody')
data = table.find_all('a')
for item in data:
    link = item.get('href')
    try:
        data = getPDF('http://whatcomcounty.us'+link, COUNTY)
    except:
        data = getPDF(link, COUNTY)


#Scrape Covid-19 County Guidelines
links = [
    'http://whatcomcounty.us/3404/Masks-and-Face-Coverings',
    'http://whatcomcounty.us/3374/Resources-for-Businesses-Organizations',
    'http://whatcomcounty.us/3356/Healthcare-Providers',
    'https://www.whatcomcounty.us/3369/Individuals-Families-Households#highrisk',
    'http://whatcomcounty.us/3388/COVID-19-Testing',
]

for link in links:
    soup = scraping(link)
    title = soup.select('#versionHeadLine')[0].get_text()
    section = soup.select('#page')[0]
    page = section.select('.fr-view')[0]
    f.write(title)
    f.write(page.get_text().encode('utf-8'))

f.close()



