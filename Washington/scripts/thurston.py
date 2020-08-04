  
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
top_section = soup.select_one("#WebPartWPQ5 .ms-rteTable-default")
for a_tag in top_section.find_all('a'):
    try:
        link = a_tag.get("href")
        try:
            pdf = getPDF('https://www.thurstoncountywa.gov'+link, COUNTY)
        except:
            pdf = getPDF(link, COUNTY)
    except:
        print('Not a pdf!')


data = soup.select("div ~ ul p")

for item in data:
    print("item", item.text)
    try: 
        link = item.find('a').get("href")
        try:
            pdf = getPDF('https://www.thurstoncountywa.gov'+link, COUNTY)
        except:
            pdf = getPDF(link, COUNTY)
    except:
        print('Not a pdf!')

#Scrape main page:
url = 'https://www.thurstoncountywa.gov/phss/Pages/coronavirus.aspx'
soup = scraping(url)
body = soup.select('#WebPartWPQ5')[0]
section = body.find('div', class_='text')
f.write(section.get_text(separator='\n'))

f.close()
