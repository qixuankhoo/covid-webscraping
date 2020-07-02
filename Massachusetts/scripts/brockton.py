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
from documentcloud import DocumentCloud
from urllib.request import Request, urlopen

client = DocumentCloud()

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
    # dynamically download pdf
    req = Request(file_url, headers={'User-Agent' : 'Mozilla/5.0'})
    webpage = urlopen(req)
    title = file_url.split('/').pop()
    with open("../data/" + county + "-PDF" + "/" + title,"wb") as pdf:
        pdf.write(webpage.read())


def saveText(url):
    soup = scraping(url)
    main = soup.find('div', class_='col col-xs-11')
    if main:
        f.write(main.get_text(separator = '\n'))
    else:
        f.write('\nNo relevant text found\n')

def saveArticle(url):
    soup = advanced_scraping(url)
    article = soup.find('article')
    f.write(article.text)
    for a_tag in article.find_all('a'):
        link = a_tag.get('href')
        if link and '.pdf' in link:
            if ('http' not in link or 'brockton' in link) and 'CDC' not in link and 'guidance-sheet' not in link and 'MDPH' not in link: # not from cdc or state
                getPDFs(link, 'brockton')

COUNTY = "brockton"
f = open("../data/" + COUNTY + ".txt", "w")

pdfPath = "../data/" + COUNTY + "-PDF"
os.mkdir(pdfPath)

# scraping 'https://bphc.org/whatwedo/infectious-diseases/Infectious-Diseases-A-to-Z/Documents/Mask%20Guide.pdf'
getPDFs('https://bphc.org/whatwedo/infectious-diseases/Infectious-Diseases-A-to-Z/Documents/Mask%20Guide.pdf', 'brockton')

# scraping 'https://brockton.ma.us/covid19/'
soup = advanced_scraping('https://brockton.ma.us/covid19/')
text_area = soup.select_one('.fl-node-5e726539b7e8b')
f.write(text_area.text)

content = soup.select_one('.main-content-full-width')
for a_tag in content.find_all('a'):
    link = a_tag.get('href')
    if link and '.pdf' in link:
        if ('http' not in link or 'brockton' in link) and 'CDC' not in link and 'guidance-sheet' not in link and 'MDPH' not in link: # not from cdc or state
            getPDFs(link, 'brockton')

# scraping 'https://brockton.ma.us/business/covid-19-response/'
soup = advanced_scraping('https://brockton.ma.us/business/covid-19-response/')
text_area = soup.find('div', class_='fl-rich-text')
f.write(text_area.text)
for a_tag in text_area.find_all('a'):
    link = a_tag.get('href')
    if link and '.pdf' in link:
        if ('http' not in link or 'brockton' in link) and 'CDC' not in link and 'guidance-sheet' not in link and 'MDPH' not in link: # not from cdc or state
            getPDFs(link, 'brockton')

# scrape https://brockton.ma.us/news/
for page in range(1, 7):
    url = 'https://brockton.ma.us/news/page' + str(page)
    soup = advanced_scraping(url)
    read_mores = soup.select('.moretag')
    for read_more in read_mores:
        link = read_more.get('href')
        saveArticle(link)