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
    title = file_url.split('/').pop()
    fileName = title 
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

COUNTY = "gaston"

#create PDF folder for PDF files
try:
    filePath = getFilePath("../data/" + COUNTY + "-PDF")
    os.mkdir(filePath) 
except:
    print('PDF folder already exists!')

textFilePath = '../data/' + COUNTY + '.txt'
f = open(getFilePath(textFilePath), 'w')
links = []

#Scrape latest updates page 
url = 'https://www.gastongov.com/coronavirus/'
soup = scraping(url)
section = soup.find('div', class_='post clearfix')
lst = section.find_all('p')[1]
data = lst.find_all('a')
for item in data:
    link = item.get('href')
    if 'Documents' in link.split('/'):
        pdf = getPDF('https://www.gastongov.com/'+link, COUNTY)
    else:
        try:
            currSoup = scraping('https://www.gastongov.com/'+link)
            f.write(currSoup.select('.entry')[0].get_text())
        except:
            print('Unscrapeable - media link')

#Scrape business re-opening guidance
links = [
    'https://www.gastondevcorp.com/professional-financial-services',
    'https://www.gastondevcorp.com/restaurants-bars',
    'https://www.gastondevcorp.com/personal-care-grooming',
    'https://www.gastondevcorp.com/exercise-entertainment-facilities',
    'https://www.gastondevcorp.com/retail'
]

for link in links:
    currSoup = scraping(link)
    f.write(currSoup.select('#PAGES_CONTAINERinlineContent')[0].get_text())

f.close()
