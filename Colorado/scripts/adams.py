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
    title = file_url.split('/').pop()
    r = requests.get(file_url, stream = True)
    with open("../data/" + county + "-PDF" + "/" + title + ".pdf","wb") as pdf:
        for chunk in r.iter_content(chunk_size=1024*1024):
            pdf.write(chunk)
    return "data/" + title

def saveText(url):
    soup = scraping(url)
    divs = soup.select('.even li , .even p , .content .article-date')
    for div in divs:   
        print(div.text)
        f.write(div.text)


COUNTY = "adams"
f = open("../data/" + COUNTY + ".txt", "w")

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
driver = webdriver.Chrome(ChromeDriverManager().install(), options = chrome_options)


# scrape from "http://www.adcogov.org/news"
url = 'http://www.adcogov.org/news'
soup = advanced_scraping(url)
div = soup.find('div', class_="col-md-9")
print(div.prettify())

results = div.find_all('a')

for result in results:
    url = result.get('href')
    print(url)
    if 'news' in url:
        saveText('http://www.adcogov.org' + url)



# create a folder for PDFs

triPath = "../data/tri-county-PDF"
os.mkdir(triPath)

        
# tricounty - adams, douglas, arapahoe
# scrape from "https://www.tchd.org/825/Public-Health-Orders"
url = 'https://www.tchd.org/825/Public-Health-Orders'
soup = scraping(url)
links = []
results = soup.find_all('a')

count = 0

for result in results:
    url = result.get('href')
    
    if 'drive.google' in url:
        gdownload(url, triPath + "/drive" + str(count) + ".pdf")
        count += 1
        f.write("A PDF HERE\n\n\n")
    elif 'DocumentCenter' in url:
        getPDFs('https://www.tchd.org/' + url, "tri-county")
        f.write("A PDF HERE\n\n\n")

