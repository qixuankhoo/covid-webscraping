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

client = DocumentCloud()


COUNTY = "genesee"

def scraping(url):
    print("\n\n\nScraping from " + url + "\n\n\n")
    f.write("\n\n\nScraping from " + url + "\n\n\n")
    r = requests.get(url)
    return BeautifulSoup(r.content, 'html.parser')

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
        

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--start-maximized")

directory = os.getcwd()[:-7] + "data/" + COUNTY + "-PDF"
prefs = {"download.default_directory":
                        directory}
chrome_options.add_experimental_option("prefs", prefs)
chrome_options.add_argument('--headless')
chrome_options.add_argument("--enable-javascript")
driver = webdriver.Chrome(ChromeDriverManager().install(), options = chrome_options)

def downloadDocumentCloud(url):

    print("pdf url", url)
    driver.get(url)
    time.sleep(3)
    download_button = driver.find_element_by_xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "SendTrackDownloadView__downloadContainer___1nbjO", " " ))]//*[contains(concat( " ", @class, " " ), concat( " ", "spectrum-ActionButton--quiet", " " ))]')
    download_button.click()
    time.sleep(2)
    
    

f = open("../data/" + COUNTY + ".txt", "w")


pdfPath = "../data/" + COUNTY + "-PDF"
os.mkdir(pdfPath)



# scrape 'https://gchd.us/resources/media-releases-2/'
soup = scraping('https://gchd.us/resources/media-releases-2/')
section = soup.find('div', id="Text")
for a_tag in section.find_all('a'):
    if int(a_tag.text.split()[-1].split('/')[-1]) > 19: # after 2019
        getPDFs(a_tag.get('href'), 'genesee')
    else:
        break

# scrape from 'https://gchd.us/covid-19-residents/' and 'http://gchd.us/employers-and-workers/'
for url in ['https://gchd.us/covid-19-residents/', 'http://gchd.us/employers-and-workers/']:
    soup = scraping(url)
    section = soup.find('div', class_='wp-block-column')
    for a_tag in section.find_all('a'):
        link = a_tag.get('href')
        if 'documentcloud' in link:
            downloadDocumentCloud(link)

# scrape from 'https://gchd.us/covid-19-education/'
url = 'https://gchd.us/covid-19-education/'
soup = scraping(url)
sections = soup.find_all('div', class_='wp-block-column')
i = 0
for section in sections:
    if i == 0:
        i = 1
        continue
    for a_tag in section.find_all('a'):
        link = a_tag.get('href')
        if 'documentcloud' in link:
            downloadDocumentCloud(link)
