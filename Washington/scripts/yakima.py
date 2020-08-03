from bs4 import BeautifulSoup
import requests
import os 
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
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
    driver.get(url)
    time.sleep(1)
    result = driver.execute_script("return document.documentElement.outerHTML")
    return BeautifulSoup(result, 'html.parser')


def getPDF(file_url, county):
    fileName = file_url.split('/').pop()
    if '.pdf' not in fileName:
        fileName += '.pdf'
    filePath = getFilePath("../data/" + county + "-PDF")
    r = requests.get(file_url, stream = True)
    with open(os.path.join(filePath,fileName), "wb") as pdf:
        for chunk in r.iter_content(chunk_size=1024):
         if chunk:
             pdf.write(chunk)
    return "data/" + fileName
    
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
driver = webdriver.Chrome(ChromeDriverManager().install(), options = chrome_options) 

COUNTY = "yakima"

textFilePath = '../data/' + COUNTY + '.txt'
f = open(getFilePath(textFilePath), 'w')
links = []

#create PDF folder for PDF files
try:
    filePath = getFilePath("../data/" + COUNTY + "-PDF")
    os.mkdir(filePath) 
except:
    print('PDF folder already exists!')
    

#Scrape Covid-19 main site
url = 'https://www.yakimacounty.us/2323/COVID-19'
soup = scraping(url)
title = soup.select('#versionHeadLine')[0].get_text() #.encode('utf-8')
section = soup.select('#page')[0]
page = section.select('.fr-view')[0]
f.write(title)
f.write(page.get_text())


#Scrape Covid-19 County Guidelines
links = [
    'https://www.yakimacounty.us/2343/Workplaces',
    'https://www.yakimacounty.us/2337/Schools',
    'https://www.yakimacounty.us/2342/High-Risk-Individuals',
    'https://www.yakimacounty.us/2336/Community'
]

for link in links:
    soup = scraping(link)
    title = soup.select('#versionHeadLine')[0].get_text() #.encode('utf-8')
    section = soup.select('#page')[0]
    page = section.select('.fr-view')[0]
    f.write(title)
    f.write(page.get_text())


#Scrape Media Releases
url = 'https://www.yakimacounty.us/2386/COVID-19-Media-Releases'
soup = scraping(url)
data = soup.select('#page li')

for item in data:
    try:
        link = item.find('a').get('href')
        print(link)
        try:
            pdf = getPDF('https://www.yakimacounty.us'+link, COUNTY)
        except:
            pdf = getPDF(link, COUNTY)
    except:
        print('Not a pdf!')

f.close()

