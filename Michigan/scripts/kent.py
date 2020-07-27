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

def writeEmail(url):
    soup = scraping(url)
    data = soup.find_all('td', class_="editor-text")
    for item in data:
        f.write(item.get_text().encode('utf-8'))

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

COUNTY = "kent"
textFilePath = '../data/' + COUNTY + '.txt'
f = open(getFilePath(textFilePath), 'w')
links = []

#create PDF folder for PDF files
try:
    filePath = getFilePath("../data/" + COUNTY + "-PDF")
    os.mkdir(filePath) 
except:
    print('PDF folder already exists!')

#Scrape Covid-19 updates 
url = 'https://www.accesskent.com/Health/covid-19-news.htm'
soup = scraping(url)
section = soup.find('article')
lists = []
lists.append(section.find('ul', class_="styled"))
lists.append(soup.find_all('ul', class_="accordion")[0])

for lst in lists:
    data = lst.find_all('li')
    for item in data:
        link = item.find('a').get('href')
        if 'https://www' not in link.split('.'):
            try:
                writeEmail(link)
            except:
                continue
        else:
            try:
                getPDF(link, COUNTY)
            except:
                continue

f.close()