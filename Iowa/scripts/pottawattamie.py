#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests 
from bs4 import BeautifulSoup 
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time
import os
from google_drive_downloader import GoogleDriveDownloader as gdd
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
driver = webdriver.Chrome(ChromeDriverManager().install(), options = chrome_options)



COUNTY = "pottawattamie"
fileDir = os.path.dirname(__file__)
filePath = os.path.join(fileDir, "../data/pottawattamie.txt")
filePath = os.path.abspath(os.path.realpath(filePath))
f = open(filePath, 'w')

def scraping(url):
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
        print(google_id)
    gdd.download_file_from_google_drive(file_id=google_id,
                                    dest_path=destination)

path = "../data/" + COUNTY + "-PDF"
fileDir = os.path.dirname(__file__)
filePath = os.path.join(fileDir, path)
filePath = os.path.abspath(os.path.realpath(filePath))
os.makedirs(filePath, exist_ok=True)

soup = scraping("https://sites.google.com/pcema-ia.org/covid-19/home")
data = soup.find_all("a", class_="FKF6mc TpQm9d QmpIrf")
links = []
for i in range(len(data)):
    links.append(data[i]['href'])
newlinks = []
for i in links:
    if i[0] == "/":
        newlinks.append("https://sites.google.com" + i)
    elif "q=https" in i:
        i = i.replace("url?q=", "SPLIT")
        i = i.replace("&sa", "SPLIT")
        j = i.split("SPLIT")
        q = j[1].replace("%2F", "/")
        q = q.replace("%3D", "=")
        q = q.replace("%25", "%")
        q = q.replace("%3F", "?")
        q = q.replace("%3A", ":")
        newlinks.append(q)
    else:
        newlinks.append(i)

soup = scraping("https://sites.google.com/pcema-ia.org/covid-19/community-resources?authuser=0")
data = soup.find_all("a", class_="XqQF9c")
links = []
for i in range(len(data)):
    links.append(data[i]['href'])
for i in links:
    if i[0] == "/":
        newlinks.append("https://sites.google.com" + i)
    elif "q=https" in i:
        i = i.replace("url?q=", "SPLIT")
        i = i.replace("&sa", "SPLIT")
        j = i.split("SPLIT")
        q = j[1].replace("%2F", "/")
        q = q.replace("%3D", "=")
        q = q.replace("%25", "%")
        q = q.replace("%3F", "?")
        q = q.replace("%3A", ":")
        newlinks.append(q)
    else:
        newlinks.append(i)

data = soup.find_all("a", class_="QmpIrf")
links = []
for i in range(len(data)):
    links.append(data[i]['href'])
for i in links:
    if i[0] == "/":
        newlinks.append("https://sites.google.com" + i)
    elif "q=https" in i:
        i = i.replace("url?q=", "SPLIT")
        i = i.replace("&sa", "SPLIT")
        j = i.split("SPLIT")
        q = j[1].replace("%2F", "/")
        q = q.replace("%3D", "=")
        q = q.replace("%25", "%")
        q = q.replace("%3F", "?")
        q = q.replace("%3A", ":")
        newlinks.append(q)
    else:
        newlinks.append(i)

soup = scraping("https://sites.google.com/pcema-ia.org/covid-19/press-releases-media?authuser=0")
data = soup.find_all("a", class_="XqQF9c")
links = []
for i in range(len(data)):
    links.append(data[i]['href'])
for i in links:
    if i[0] == "/":
        newlinks.append("https://sites.google.com" + i)
    elif "q=https" in i:
        i = i.replace("url?q=", "SPLIT")
        i = i.replace("&sa", "SPLIT")
        j = i.split("SPLIT")
        q = j[1].replace("%2F", "/")
        q = q.replace("%3D", "=")
        q = q.replace("%25", "%")
        q = q.replace("%3F", "?")
        q = q.replace("%3A", ":")
        newlinks.append(q)
    else:
        newlinks.append(i)


PDFS = []
GDOCS = []
done = []

for link in newlinks:
    if "drive.google" in link:
        if "1OlXqKypHk9c3Nu46kn_gh7ZLaAIAerM0" in link:
            continue
        GDOCS.append(link)
    elif "pdf" in link:
        PDFS.append(link)
    else:
        if link not in done:
            done.append(links)
            soup = scraping(link)
            data = soup.find_all("p")
            for i in range(len(data)):
                f.write(data[i].text)

import PyPDF2
import io
import glob

import requests
from PyPDF2 import PdfFileReader


count = 0
for i in GDOCS:
    if i not in done:
        done.append(i)
        gdownload(i, filePath + "/drive" + str(count) + ".pdf")
        count = count + 1

for file in glob.glob(filePath + "/*.pdf"):
    if file.endswith('.pdf'):
        try:
            fileReader = PyPDF2.PdfFileReader(open(file, "rb"))
        except:
            print("failed to read pdf", file)
        else:
            count = 0
            count = fileReader.numPages
            while count >= 0:
                count -= 1
                pageObj = fileReader.getPage(count)
                text = pageObj.extractText()
                f.write(text)

def getPDFs(file_url, county):
    title = file_url.split('/').pop()
    r = requests.get(file_url, stream = True)
    path = "../data/" + COUNTY + "-PDF" + "/" + title
    fileDir = os.path.dirname(__file__)
    filePath = os.path.join(fileDir, path)
    filePath = os.path.abspath(os.path.realpath(filePath))
    h = open(filePath, "wb")
    with h as pdf:
        for chunk in r.iter_content(chunk_size=1024):
         if chunk:
             pdf.write(chunk)
    return "data/" + title

for url in PDFS:
    if "Homemade" in url:
        continue
    getPDFs(url, COUNTY)
    print("Scraping from" + url)
    r = requests.get(url)
    fi = io.BytesIO(r.content)
    reader = PdfFileReader(fi)
    number_of_pages = reader.getNumPages()
    for page_number in range(number_of_pages):
        page = reader.getPage(page_number)
        page_content = page.extractText()
        f.write(page_content)

f.close()
driver.quit()
print("finished")


# In[ ]:




