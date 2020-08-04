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

def getPDF(file_url, county):
    title = ' '.join(file_url.split('/')).split().pop()
    if '.pdf' not in title:
        title += '.pdf'
    fileName = title
    filePath = getFilePath("../data/" + county + "-PDF")
    r = requests.get(file_url, stream = True)
    with open(filePath + "/" + fileName, "wb") as pdf:
        for chunk in r.iter_content(chunk_size=1024):
         if chunk:
             pdf.write(chunk)
    return "../data/" + title

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
driver = webdriver.Chrome(ChromeDriverManager().install(), options = chrome_options)

COUNTY = "mecklenberg"

#create PDF folder for PDF files
try:
    filePath = getFilePath("../data/" + COUNTY + "-PDF")
    os.mkdir(filePath) 
except:
    print('PDF folder already exists!')

textFilePath = '../data/' + COUNTY + '.txt'
f = open(getFilePath(textFilePath), 'w')


#Scrape business guidance 
url = 'https://www.mecknc.gov/news/Pages/COVID-19-Business-Toolkit.aspx'
soup = scraping(url)
data = soup.select('h4+ a')
print(len(data))
for item in data:
    link = item.get('href')
    try:
        try:
            pdf = getPDF(link, COUNTY)
        except:
            pdf = getPDF('https://www.mecknc.gov' + link, COUNTY)
    except:
        print('Not a PDF')


#Scrape healthy-eating blog
url = 'http://blog.mecknc.gov/healthy-food/'
soup = scraping(url)
title = soup.select('.post-title')[0]
body = soup.select('.post-content')[0]
f.write(title.get_text())
f.write(body.get_text())


#Scrape Charlotte-Mcklenburg school info
url = 'https://www.cms.k12.nc.us/cmsdepartments/csh/covid-19/Pages/default.aspx'
soup = scraping(url)
content = soup.select('#site_content')[0]
f.write(content.get_text())

f.close()
