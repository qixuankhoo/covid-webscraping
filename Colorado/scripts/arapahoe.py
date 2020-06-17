import requests 
from bs4 import BeautifulSoup 
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time
import os
from google_drive_downloader import GoogleDriveDownloader as gdd

import urllib3
import re

COUNTY = "arapahoe"
f = open("../data/" + COUNTY + ".txt", "w")
path = "../data/" + COUNTY + "-PDF"
os.mkdir(path)

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
driver = webdriver.Chrome(ChromeDriverManager().install(), options = chrome_options)

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
    with open("../data/" + COUNTY + "-PDF" + "/" + title + ".pdf","wb") as pdf:
        for chunk in r.iter_content(chunk_size=1024*1024):
            pdf.write(chunk)
    return "data/" + title

def scraping(url):
    print("Scraping from " + url)
    f.write("\n\n\n")
    f.write("Scraping from " + url + "\n\n\n")
    driver.get(url)
    time.sleep(1)
    result = driver.execute_script("return document.documentElement.outerHTML")
    return BeautifulSoup(result, 'html.parser')


# tricounty - adams, douglas, araphoe
# scrape from "https://www.tchd.org/825/Public-Health-Orders"
url = 'https://www.tchd.org/825/Public-Health-Orders'
soup = scraping(url)
links = []
results = soup.find_all('a')

count = 0

for result in results:
    url = result.get('href')
    
    if 'drive.google' in url:
        gdownload(url, "../data/" + COUNTY + "-PDF/drive" + str(count) + ".pdf")
        count += 1
        f.write("A PDF HERE\n\n\n")
    elif 'DocumentCenter' in url:
        getPDFs('https://www.tchd.org/' + url, COUNTY)
        f.write("A PDF HERE\n\n\n")

url = "https://www.arapahoegov.com/2098/COVID-19-News-Updates"
soup = scraping(url)

links = []
data = soup.find_all("div", class_= "fr-view")


for i in range(len(data)):
    for link in data[i].find_all('a'):
        links.append(link.get('href'))

#
for link in links:
    currSoup = scraping(link)
    currdata = currSoup.find_all("div", class_= "content")
    for i in range(len(currdata)):
        f.write(currdata[i].text)



# scrap from https://www.arapahoegov.com/covid19
f.write("--------------------------------------------")
url = "https://www.arapahoegov.com/covid19"
soup = scraping(url)
data = soup.find_all("div", class_= "widget editor pageStyles wide")
for i in range(len(data)):
    f.write(data[i].text)
    f.write("\n\n\n")




f.close()
driver.quit()
print("finished")
