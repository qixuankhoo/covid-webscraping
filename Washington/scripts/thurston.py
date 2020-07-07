from bs4 import BeautifulSoup
import requests
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time


def getFilePath(path):
    fileDir = os.path.dirname(__file__)
    filePath = os.path.join(fileDir,path)
    return filePath

def scraping(url):
    print("Scraping from " + url)
    f.write("\n\n\n")
    f.write("Scraping from " + url + "\n\n\n")
    driver = webdriver.Chrome(executable_path="/Users/qixuan.khoo.19/Downloads/chromedriver")
    driver.get(url)
    time.sleep(5)
    result = driver.execute_script("return document.documentElement.outerHTML")
    return BeautifulSoup(result, 'html.parser')

def getPDF(file_url, county):
    title = file_url.split('/').pop()
    fileName = title + '.pdf'
    filePath = getFilePath("/data/" + county + "-PDF")
    r = requests.get(file_url, stream = True)
    with open(os.path.join(filePath,fileName), "wb") as pdf:
        for chunk in r.iter_content(chunk_size=1024):
         if chunk:
             pdf.write(chunk)
    return "data/" + title


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
    data = getPDF('http://thurstoncountywa.gov'+link, COUNTY)

#Scrape main page:
url = 'https://www.thurstoncountywa.gov/phss/Pages/coronavirus.aspx'
soup = scraping(url)

