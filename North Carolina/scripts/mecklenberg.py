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
    print("file_url", file_url)
    print(file_url.split("/"))
    fileName = title
    print("title" ,title)
    filePath = getFilePath("../data/" + county + "-PDF")
    r = requests.get(file_url, stream = True)
    with open(os.path.join(filePath,fileName), "wb") as pdf:
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


#Scrape business re-opening guidance page
url = 'https://www.mecknc.gov/news/Pages/Update-on-Novel-Coronavirus.aspx'
soup = scraping(url)
f.write(soup.select('.mc-page')[0].get_text())


#Scrape resources PDFs
url = 'https://www.mecknc.gov/news/Pages/Update-on-Novel-Coronavirus.aspx'
soup = scraping(url)
sections = soup.select('#gradient-resources')
for section in sections:
    data = section.find_all('li')
    for item in data:
        text = item.find('a').get_text()
        link = item.find('a').get('href')
        if 'NC' in text or 'N.C.' in text or 'CDC' in text:
            continue
        else:
            try:
                full_url = link
                if 'mecknc.gov' not in full_url:
                    full_url = 'https://www.mecknc.gov/' + full_url
                currSoup = scraping(full_url)
                f.write(currSoup.select('.mc-page-content')[0].get_text())
            except:
                pdf = getPDF('https://www.mecknc.gov/'+link, COUNTY)

f.close()
