# RUN APPLICATION
import requests
from bs4 import BeautifulSoup
import urllib3
import re
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time
import os
from google_drive_downloader import GoogleDriveDownloader as gdd
import sys


def scraping(url):
    print("\n\n\nScraping from " + url + "\n\n\n")
    f.write("\n\n\nScraping from " + url + "\n\n\n")
    r = requests.get(url)
    return BeautifulSoup(r.content, 'html.parser')

def advanced_scraping(url):
    print("\n\n\nScraping from " + url + "\n\n\n")
    f.write("\n\n\nScraping from " + url + "\n\n\n")
    driver.get(url)
    time.sleep(1)
    result = driver.execute_script("return document.documentElement.outerHTML")
    return BeautifulSoup(result, 'html.parser')

def getPDFs(file_url):
    print("A PDF HERE\n")
    f.write("A PDF HERE\n")
    title = file_url.split('/').pop()
    r = requests.get(file_url, stream = True)
    writePath = "../data/oakland-PDF/" + title + ".pdf"
    print("writing to ", writePath)
    with open(writePath,"wb") as pdf:
        for chunk in r.iter_content(chunk_size=1024*1024):
            pdf.write(chunk)
    return "data/" + title


def saveText(url):
    soup = advanced_scraping(url)
    main = soup.find('main', class_="col-xs-12 col-md-9 col-md-push-3")
    f.write(main.get_text(separator = '\n'))


COUNTY = "oakland"
f = open("../data/" + COUNTY + ".txt", "w")


pdfPath = "../data/" + COUNTY + "-PDF"
os.mkdir(pdfPath)

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument("--enable-javascript")
driver = webdriver.Chrome(ChromeDriverManager().install(), options = chrome_options)


# scrape from 'https://www.oakgov.com/covid/best-practices/Pages/default.aspx'
soup = advanced_scraping('https://www.oakgov.com/covid/best-practices/Pages/default.aspx')
section = soup.find('section', class_="col-xs-12")
for a in section.find_all('a'):
    link = a.get('href')
    #print(link)
    if '.pdf' in link:
        getPDFs("https://www.oakgov.com" + link)
    elif 'best-practices' in link:
        saveText("https://www.oakgov.com" + link)


# scrape from 'https://www.oakgov.com/covid/Pages/Health-Orders.aspx'

soup = advanced_scraping('https://www.oakgov.com/covid/Pages/Health-Orders.aspx')
section = soup.find('section', class_="col-xs-12")
for a in section.find_all('a'):
    link = a.get('href')
    #print(link)
    if '.pdf' in link:
        getPDFs("https://www.oakgov.com" + link)


# scrape from 'https://www.oakgov.com/pages/news.aspx'
url = 'https://www.oakgov.com/pages/news.aspx'
print("\n\n\nScraping from " + url + "\n\n\n")
f.write("\n\n\nScraping from " + url + "\n\n\n")
driver.get(url)
time.sleep(1)
i = 0

newsLinks = driver.find_elements_by_xpath('//*[(@id = "main-content")]//a')

while i < 120 and i < len(newsLinks):
    print("i", i)
    print("\n\n\nSCRAPING NEWS ARTICLE: " + newsLinks[i].text + "\n\n\n")
    f.write("\n\n\nSCRAPING NEWS ARTICLE: " + newsLinks[i].text + "\n\n\n")
    newsLinks[i].click()
    result = driver.execute_script("return document.documentElement.outerHTML")
    soup = BeautifulSoup(result, 'html.parser')
    article = soup.find('article')
    if article:
        f.write(article.get_text(separator = '\n'))
    driver.get(url)
    time.sleep(1)
    loadMoreButton = driver.find_element_by_xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "btn-block", " " ))]')
    if not loadMoreButton:
        break
    i += 1
    for j in range(0, int(i / 10)): # click on it enough to see news article
        loadMoreButton.click()
        time.sleep(0.5)
    newsLinks = driver.find_elements_by_xpath('//*[(@id = "main-content")]//a')
    
print("oakland finished")


driver.quit()
