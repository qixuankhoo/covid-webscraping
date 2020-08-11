from bs4 import BeautifulSoup
import requests
import os 
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import time

from urllib.request import Request, urlopen


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
        f.write(currdata[i].get_text())

def findHref(data):
    for i in range(len(data)):
        for link in data[i].find_all('a'):
            links.append(link.get('href'))

def getPDF(file_url, county):
    print("pdf url", file_url)
    print("A PDF HERE\n")
    f.write("A PDF HERE\n")
    # dynamically download pdf
    req = Request(file_url, headers={'User-Agent' : 'Mozilla/5.0'})
    webpage = urlopen(req)
    title = file_url.split('/').pop()
    if '.pdf' not in title:
        title += '.pdf'
    with open("../data/" + county + "-PDF" + "/" + title,"wb") as pdf:
        pdf.write(webpage.read())
    
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
driver = webdriver.Chrome(ChromeDriverManager().install(), options = chrome_options)

COUNTY = "fall_river"

#create PDF folder for PDF files
try:
    filePath = getFilePath("../data/" + COUNTY + "-PDF")
    os.mkdir(filePath) 
except:
    print('PDF folder already exists!')

textFilePath = '../data/' + COUNTY + '.txt'
f = open(getFilePath(textFilePath), 'w')
links = []

#Scrape all PDFs on Fall River County Reopening-Guidance website
url = 'https://www.fallriverma.org/department/corona-virus-information/'
soup = scraping(url)
data = soup.find_all('tr')
print('done')
findHref(data)
print(len(links))

for link in links:
    if "fallriverma" in link:
        getPDF(link, COUNTY)
    else:
        getPDF('https://www.fallriverma.org'+link, COUNTY)


f.close()






    




