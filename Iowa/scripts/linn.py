from bs4 import BeautifulSoup
import requests
import os 
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import time

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

def writeData(soup, tag, id_name):
    currdata = soup.find(tag, id_= id_name)
    f.write(currdata.get_text())

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

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
driver = webdriver.Chrome(ChromeDriverManager().install(), options = chrome_options)
COUNTY = "linn"

#create PDF folder for PDF files
try:
    filePath = getFilePath("../data/" + COUNTY + "-PDF")
    os.mkdir(filePath) 
except:
    print('PDF folder already exists!')
    
textFilePath = '../data/' + COUNTY + '.txt'
f = open(getFilePath(textFilePath), 'w')
links = []

#Scrape all links to resources on Linn County toolkits website --done
try:
    url = 'https://www.linncounty.org/1400/Toolkits'
    links = []
    currSoup = scraping(url)
    data = currSoup.find_all('div', class_='widgetBody imageBorder')

    for item in data:
        link = item.find('a').get('href')
        links.append('https://www.linncounty.org'+link)
except:
    print('Error scraping website!') 

#Scrape business guidance website --done
try:
    url = 'https://www.linncounty.org/1404/Business-Guidance'
    currSoup = scraping(url)
    section = currSoup.find_all('div', class_="siteWrap2")[1]
    f.write(section.get_text())
except:
    print('Error scraping website!')

#Scrape mental health website --done
try:
    url = 'https://www.linncounty.org//1405/Mental-Health'
    currSoup = scraping(url)
    data = currSoup.find_all('p')

    for item in data:
        text = item.get_text()
        if 'PDF' in text:
            link = item.find('a')
            pdf = getPDF(link.get('href'), COUNTY)
        else:
            f.write(text)
except:
    print('Error scraping website!')
 
#Scrape senior guidance 
try:
    url = 'https://www.scottcountyiowa.gov/health/covid19/assisted-living-senior-centers'
    currSoup = scraping(url)
    section = currSoup.find('div', class_='field field-name-body field-type-text-with-summary field-label-hidden')
    f.write(section.get_text())
except: 
    print('Error scraping website!')


#Scrape individuals-families-home website
try:
    url = 'https://www.scottcountyiowa.gov/health/covid19/individuals-families-home'
    currSoup = scraping(url)
    section = currSoup.find('div', class_='field field-name-body field-type-text-with-summary field-label-hidden')
    f.write(section.get_text())
except: 
    print('Error scraping website!')

f.close()






