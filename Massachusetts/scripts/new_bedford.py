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

def writeData(soup, tag, class_name):
    currdata = soup.find_all(tag, class_= class_name)
    for i in range(len(currdata)):
        f.write(currdata[i].get_text().encode('utf-8'))

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

COUNTY = "new_bedford"

#create PDF folder for PDF files
try:
    filePath = getFilePath("../data/" + COUNTY + "-PDF")
    os.mkdir(filePath) 
except:
    print('PDF folder already exists!')

textFilePath = '../data/' + COUNTY + '.txt'
f = open(getFilePath(textFilePath), 'w')



#Scrape New Bedford economic development guidelines
url = 'http://www.nbedc.org/covid-19-resources-and-information/'
soup = scraping(url)
writeData(soup, 'div', 'avia_textblock')

links = ['https://s3.amazonaws.com/newbedford-ma/wp-content/uploads/20200506082240/Emergency-Order-Reporting-COVID-in-the-Workplace.pdf',
        'https://s3.amazonaws.com/newbedford-ma/wp-content/uploads/sites/42/20200506124549/Emergency-Order-to-Prevent-the-Spread-of-COVID-in-industrial-facilities.pdf']
for link in links:
    data = getPDF(link, COUNTY)

f.close()