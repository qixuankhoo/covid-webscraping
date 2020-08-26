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


chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
driver = webdriver.Chrome(ChromeDriverManager().install(), options = chrome_options)

def scraping(url):
    print("Scraping from " + url)
    f.write("\n\n\n")
    f.write("Scraping from " + url + "\n\n\n")
    driver.get(url)
    time.sleep(1)
    result = driver.execute_script("return document.documentElement.outerHTML")
    return BeautifulSoup(result, 'html.parser')

COUNTY = "scott"
textFilePath = '../data/' + COUNTY + '.txt'
f = open(getFilePath(textFilePath), 'w')

#Scrape Covid-19 Recommendations page
url = 'https://www.scottcountyiowa.gov/health/covid19/recommendations#4-cs'
soup = scraping(url)
data = soup.find_all('div', class_='field field-name-field-para-text field-type-text-long field-label-hidden')

for item in data:
    f.write(item.get_text())


#Scrape Covid-19 FAQ page
url = 'https://www.scottcountyiowa.gov/health/post/covid-19-frequently-asked-questions'
soup = scraping(url)
faqs = soup.find('div', class_='field field-name-body field-type-text-with-summary field-label-hidden').get_text()
f.write(faqs)


#Scrape community resources
links = [
    'https://www.scottcountyiowa.gov/health/covid19/individuals-families-home',
    'https://www.scottcountyiowa.gov/health/covid19/assisted-living-senior-centers',
    'https://www.scottcountyiowa.gov/health/covid19/businesses',
    'https://www.scottcountyiowa.gov/health/covid19/faith-based'
]

for link in links:
    try:
        soup = scraping(link)
        data = soup.find('div', class_='field field-name-body field-type-text-with-summary field-label-hidden').get_text()
        f.write(data)
    except:
        print('Error scraping this website!')

f.close()
