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
    filePath = os.path.join(fileDir,path)
    filePath = os.path.abspath(os.path.realpath(filePath))
    return filePath

def scraping(url):
    print("Scraping from " + url)
    f.write("\n\n\n")
    f.write("Scraping from " + url + "\n\n\n")
    driver.get(url)
    time.sleep(5)
    result = driver.execute_script("return document.documentElement.outerHTML")
    return BeautifulSoup(result, 'html.parser')

def getPDF(file_url, county):
    print("file url of PDF", file_url)
    fileName = file_url.split('/').pop()
    if '.pdf' not in fileName:
        fileName += '.pdf'
    filePath = getFilePath("/data/" + county + "-PDF")
    r = requests.get(file_url, stream = True)
    with open(os.path.join(filePath,fileName), "wb") as pdf:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                pdf.write(chunk)
    return "data/" + fileName


chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
driver = webdriver.Chrome(ChromeDriverManager().install(), options = chrome_options)

COUNTY = "thurston"

#create PDF folder for PDF files
try:
    filePath = getFilePath("../data/" + COUNTY + "-PDF")
    os.mkdir(filePath) 
except:
    print('PDF folder already exists!')
    
textFilePath = '../data/' + COUNTY + '.txt'
f = open(getFilePath(textFilePath), 'w')
links = []


#Scrape Letters to the Community PDFs
url = 'https://www.thurstoncountywa.gov/phss/Pages/coronavirus.aspx'
soup = scraping(url)
section = soup.find('div', class_='ExternalClass013DDBDFF84449D4A508A19321F2DB08')
div = section.find_all('div')[1]
data = div.find('ul').find_all('li')
print(len(data))
for item in data:
    link = item.find('a').get('href')
    data = getPDF('https://www.thurstoncountywa.gov'+link, COUNTY)

#Scrape main page:
url = 'https://www.thurstoncountywa.gov/phss/Pages/coronavirus.aspx'
soup = scraping(url)
section = soup.find('div', class_='ExternalClass013DDBDFF84449D4A508A19321F2DB08').get_text().encode('utf-8')
f.write(section)
f.close()