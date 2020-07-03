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

def getPDFs(file_url, county):
    print("pdf url", file_url)
    print("A PDF HERE\n")
    f.write("A PDF HERE\n")
    title = file_url.split('/').pop()
    r = requests.get(file_url, stream = True)
    with open("../data/" + county + "-PDF" + "/" + title,"wb") as pdf:
        for chunk in r.iter_content(chunk_size=1024*1024):
            pdf.write(chunk)
    return "data/" + title

def saveText(url):
    soup = scraping(url)
    article = soup.find('div', class_='col-xs-12 content-tag body-content white-tag green-trim')
    f.write(article.text)
    for a_tag in article.find_all('a'):
        link = a_tag.get('href')
        if '.pdf' in link:
            if 'clark' in link:
                getPDFs(link, 'clark')
    
COUNTY = "clark"
f = open("../data/" + COUNTY + ".txt", "w")

pdfPath = "../data/" + COUNTY + "-PDF" 
os.mkdir(pdfPath)

# scrape 'https://www.clark.wa.gov/covid19/cities-and-agencies#expand'
soup = scraping('https://www.clark.wa.gov/covid19/cities-and-agencies#expand')
tabs = soup.select('.list-group-item')
for tab in tabs:
    link = tab.get('href')
    if '/' in link:
        saveText('https://www.clark.wa.gov' + link)

