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

def writeData(soup, tag, class_name):
    currdata = soup.find_all(tag, class_= class_name)
    for i in range(len(currdata)):
        f.write(currdata[i].get_text()) #.encode('utf-8'))

def findHref(data):
    for i in range(len(data)):
        link = data[i].find_all('a')[0]
        links.append(link.get('href'))

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
        fileName = 'mediaFile' + str(random.randint(1,10)) + '.pdf'
        with open(os.path.join(filePath,fileName), "wb") as pdf:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:
                    pdf.write(chunk)
    return "data/" + title
    
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
driver = webdriver.Chrome(ChromeDriverManager().install(), options = chrome_options)

COUNTY = "yakima"

'''
#create PDF folder for PDF files
try:
    filePath = getFilePath("../data/" + COUNTY + "-PDF")
    os.mkdir(filePath) 
except:
    print('PDF folder already exists!')
'''
textFilePath = '../data/' + COUNTY + '.txt'
f = open(getFilePath(textFilePath), 'w')
links = []


#Scrape Covid-19 main site
url = 'https://www.yakimacounty.us/2323/COVID-19'
soup = scraping(url)
title = soup.select('#versionHeadLine')[0].get_text() #.encode('utf-8')
section = soup.select('#page')[0]
page = section.select('.fr-view')[0]
f.write(title)
f.write(page.get_text()) #.encode('utf-8'))


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
    f.write(page.get_text()) #.encode('utf-8'))


f.close()

