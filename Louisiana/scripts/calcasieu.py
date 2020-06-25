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

def advanced_scraping(url):
    print("Scraping from " + url)
    f.write("\n\n\n")
    f.write("Scraping from " + url + "\n\n\n")
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
    print("A PDF HERE\n")
    f.write("A PDF HERE\n")
    title = file_url.split('/').pop()
    r = requests.get(file_url, stream = True)
    with open("../data/" + county + "-PDF" + "/" + title + ".pdf","wb") as pdf:
        for chunk in r.iter_content(chunk_size=1024*1024):
            pdf.write(chunk)
    return "data/" + title

def saveText(url):
    soup = scraping(url)
    div = soup.find('div', class_='need_hide_detail_widget news_widget content_area clearfix')
    print(div.get_text(separator = '\n'))
    f.write(div.get_text(separator = '\n'))



COUNTY = "calcasieu"
f = open("../data/" + COUNTY + ".txt", "w")


chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
driver = webdriver.Chrome(ChromeDriverManager().install(), options = chrome_options)


# scrape from "https://www.calcasieuparish.gov/residents/news-and-updates"
url = 'https://www.calcasieuparish.gov/residents/news-and-updates'
soup = scraping(url)
div = soup.find('div', class_="news_widget content_area clearfix")
li_tags = div.find_all('li')
for li in li_tags:
    a = li.find('a')
    url = 'https://www.calcasieuparish.gov' + a.get('href')
    saveText(url)

driver.quit()