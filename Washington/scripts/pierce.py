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
    title = file_url.split('/').pop() + '.pdf'
    r = requests.get(file_url, stream = True)
    with open("../data/" + county + "-PDF" + "/" + title,"wb") as pdf:
        for chunk in r.iter_content(chunk_size=1024*1024):
            pdf.write(chunk)
    return "data/" + title

def saveText(url):
    soup = scraping(url)
    textArea = soup.find('div', id='ColumnUserControl3')
    f.write(textArea.text)

    for a_tag in textArea.find_all('a'):
        link = a_tag.get('href')
        if link and link not in checked:
            checked.add(link)
            if 'showdocument' in link:
                if 'tpchd' not in link:
                    link = 'https://www.tpchd.org' + link
                getPDFs(link, 'pierce')
def saveBlogText(url):
    soup = scraping(url)
    textArea = soup.find('div', class_='blog-detail-view clearfix')
    f.write(textArea.text)

def saveNewsText(url):
    soup = scraping(url)
    textArea = soup.find('div', class_='item fr-view')
    f.write(textArea.get_text(separator = '\n'))

COUNTY = "pierce"
f = open("../data/" + COUNTY + ".txt", "w")

pdfPath = "../data/" + COUNTY + "-PDF" 
os.mkdir(pdfPath)

# scraping from 'https://www.tpchd.org/healthy-people/human-coronavirus'
soup = scraping('https://www.tpchd.org/healthy-people/human-coronavirus')
textArea = soup.find('div', id='ColumnUserControl3')
f.write(textArea.text)

checked = set()

for icon_page in textArea.find_all('a', class_="button-link"):
    link = icon_page.get('href')
    if 'splash' not in link and 'pierce-county-cases' not in link:
        if 'tpchd' not in link:
            link = 'https://www.tpchd.org' + link
        saveText(link)
        checked.add(link)

for a_tag in textArea.find_all('a'):
    link = a_tag.get('href')
    if link and link not in checked:
        checked.add(link)
        if 'showdocument' in link:
            if 'tpchd' not in link:
                link = 'https://www.tpchd.org' + link
            getPDFs(link, 'pierce')
        elif 'Blog/Blog' in link and 'splash' not in link:
            saveBlogText(link)


# scraping 'https://www.co.pierce.wa.us/CivicAlerts.aspx?CID=1'

soup = scraping('https://www.co.pierce.wa.us/CivicAlerts.aspx?CID=1')
read_mores = soup.select('.more')
for read_more in read_mores:
    link = read_more.get('href')
    if int(link.split('=')[-1]) > 4400:
        saveNewsText('https://www.co.pierce.wa.us' + link)
    else:
        break

# scraping 'https://www.co.pierce.wa.us/6759/Safe-Start'
soup = scraping('https://www.co.pierce.wa.us/6759/Safe-Start')
textArea = soup.find('div', class_='fr-view')
f.write(textArea.get_text(separator = '\n'))
for a_tag in textArea.find_all('a'):
    link = a_tag.get('href')
    if 'DocumentCenter' in link:
        getPDFs(link, 'pierce')