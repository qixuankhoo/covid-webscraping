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
    main = soup.find('div', class_='col col-xs-11')
    if main:
        f.write(main.get_text(separator = '\n'))
    else:
        f.write('\nNo relevant text found\n')


COUNTY = "macomb"
f = open("../data/" + COUNTY + ".txt", "w")


pdfPath = "../data/" + COUNTY + "-PDF"
os.mkdir(pdfPath)

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument("--enable-javascript")
driver = webdriver.Chrome(ChromeDriverManager().install(), options = chrome_options)


# scrape from 'https://health.macombgov.org/Health-Programs-DC-Coronavirus'
soup = scraping('https://health.macombgov.org/Health-Programs-DC-Coronavirus')
section = soup.find('section', id='content')
for a_tag in section.find_all('a'):
    link = a_tag.get('href')
    if 'macombgov' in link or 'http' not in link: # macomb government
        if 'cdc.gov' not in link and 'michigan.gov' not in link: # definitely macomb government
            if 'http' not in link:
                link = 'https://health.macombgov.org' + link
                
            if '.pdf' in link:
                getPDFs(link, "macomb")
            else:
                saveText(link)


# scrape from 'https://government.macombgov.org/Government-Newsroom'
soup = advanced_scraping('https://government.macombgov.org/Government-Newsroom')
div = soup.find('div', id='ui-id-3')
for a_tag in div.find_all('a'):
    link = a_tag.get('href')
    saveText(link)

driver.quit()