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

def scraping(url):
    print("Scraping from " + url)
    f.write("\n\n\n")
    f.write("Scraping from " + url + "\n\n\n")
    r = requests.get(url)
    return BeautifulSoup(r.content, 'html.parser')

def saveText(url):
    soup = scraping(url)
    divs = soup.select("#news_content_body , #news_content_date , h1")
    for div in divs:
        print(div.text)
        f.write(div.text)

def getPDFs(file_url, county):
    title = file_url.split('/').pop()
    r = requests.get(file_url, stream = True)
    with open("../data/" + COUNTY + "-PDF" + "/" + title,"wb") as pdf:
        for chunk in r.iter_content(chunk_size=1024*1024):
            pdf.write(chunk)
    return "data/" + title


COUNTY = "weld"
f = open("../data/" + COUNTY + ".txt", "w")

# scrape from https://www.weldgov.com/newsroom/2020_news
url = 'https://www.weldgov.com/newsroom/2020_news'
soup = scraping(url)
#print(soup.prettify())
main = soup.find('main')

results = main.find_all('a', class_="title")

for result in results:
    url = result.get('href')
    saveText('https://www.weldgov.com' + url)

path = "../data/" + COUNTY + "-PDF"
os.mkdir(path)

# scrape from "https://www.weldgov.com/cms/One.aspx?portalId=169&pageId=96262"
url = 'https://www.weldgov.com/cms/One.aspx?portalId=169&pageId=96262'
soup = scraping(url)
#print(soup.prettify())
div = soup.find('div', class_="advanced-data-display")

results = div.find_all('a')

for result in results:
    url = result.get('href')
    print(url)
    getPDFs('https://www.weldgov.com' + url, 'weld')
    f.write("A PDF HERE\n\n\n")

