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
from urllib.request import Request, urlopen


def scraping(url):
    print("\n\n\nScraping from " + url + "\n\n\n")
    f.write("\n\n\nScraping from " + url + "\n\n\n")
    r = requests.get(url)
    return BeautifulSoup(r.content, 'html.parser')

def advanced_scraping(url):
    req = Request(url, headers={'User-Agent' : 'Mozilla/5.0'})
    webpage = urlopen(req).read()
    print("Scraping from " + url)
    f.write("\n\n\n")
    f.write("Scraping from " + url + "\n\n\n")
    return BeautifulSoup(webpage, 'html.parser')

def gdownload(url, destination):
    print(url)
    splits = url.split("/")
    d_location = -1
    google_id = ""

    for i, split in enumerate(splits):
        if split == 'd':
            d_location = i
        elif 'id=' in split:
            google_id = split[split.find('id=')+3:]
    if d_location != -1 and google_id == "":
        google_id = splits[d_location + 1]
    gdd.download_file_from_google_drive(file_id=google_id,
                                    dest_path=destination)

def getPDFs(file_url, county, date):
    print("pdf url", file_url)
    f.write("A PDF HERE\n")
    # dynamically download pdf
    title = 'Proclamation_' + date.lstrip()
    r = requests.get(file_url, stream = True)
    with open("../data/" + county + "-PDF" + "/" + title + ".pdf","wb") as pdf:
        for chunk in r.iter_content(chunk_size=1024*1024):
            pdf.write(chunk)


def saveText(url):
    soup = scraping(url)
    section = soup.find('section', class_='composer_content')
    f.write(section.text)

COUNTY = "wake"
f = open("../data/" + COUNTY + ".txt", "w")

pdfPath = "../data/" + COUNTY + "-PDF"
#os.mkdir(pdfPath)

# scrape from 'https://covid19.wakegov.com/'
soup = scraping('https://covid19.wakegov.com/')
'''
divs = soup.find_all('div', class_='vc_column-inner')
for div in divs:
    if 'News Releases' not in div.text and 'Guidance For:' not in div.text:
        f.write(div.text)

proclamations = soup.select('.vc_btn3-color-grey')
for proclamation in proclamations:
    date = proclamation.text
    link = proclamation.get('href')
    getPDFs(link, 'wake', date)
'''

# scrape all tabs
links = set()
tabs = soup.select('.non_mega_menu a')
for tab in tabs:
    link = tab.get('href')
    if len(link.split('/')[-2]) != 2 and link.split('/')[-2] != 'news-releases':
        links.add(link)
links.add('https://covid19.wakegov.com/service-hours/')
links.add('https://covid19.wakegov.com/wakeforward/')

for link in links:
    saveText(link)


# scrape 'https://covid19.wakegov.com/news-releases/'
for page in range(1,11):
    url = 'https://covid19.wakegov.com/news-releases/page/' + str(page)
    soup = scraping(url)
    news_links = soup.select('.content a')
    