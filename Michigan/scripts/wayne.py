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

def saveScribdText(url):
    soup = advanced_scraping(url)
    section = soup.find('div', class_='newpage')
    f.write(section.text)


COUNTY = "wayne"
f = open("../data/" + COUNTY + ".txt", "w")


pdfPath = "../data/" + COUNTY + "-PDF"
os.mkdir(pdfPath)

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument("--enable-javascript")
chrome_options.add_argument("--start-maximized")
directory = os.getcwd()[:-7] + "data/" + COUNTY + "-PDF"
prefs = {"download.default_directory": 
                        directory} # IMPORTANT - ENDING SLASH V IMPORTANT}
chrome_options.add_experimental_option("prefs", prefs)
driver = webdriver.Chrome(ChromeDriverManager().install(), options = chrome_options)



# scrape from 'https://www.waynecounty.com/departments/hhvs/wellness/novel-coronavirus-information.aspx'
soup = scraping('https://www.waynecounty.com/departments/hhvs/wellness/novel-coronavirus-information.aspx')
div = soup.find('div', class_='ui basic vertical segment')
for a_tag in div.find_all('a'):
    print(a_tag)
    link = a_tag.get('href')
    if '.pdf' in link:
        print(link)
        if link[0] == '/': # valid
            getPDFs('https://www.waynecounty.com' + link, 'wayne')

situation_report = soup.select_one('strong .button')
url = situation_report.get('href')
saveScribdText(url)

driver.quit() 