#!/usr/bin/env python
# coding: utf-8

# In[32]:


import requests 
from bs4 import BeautifulSoup 
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time
import os


COUNTY = "polk"
fileDir = os.path.dirname(__file__)
filePath = os.path.join(fileDir, "../data/polk.txt")
filePath = os.path.abspath(os.path.realpath(filePath))
f = open(filePath, 'w')
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
driver = webdriver.Chrome(ChromeDriverManager().install(), options = chrome_options)

def scraping(url):
    print("Scraping from " + url)
    f.write("\n\n\n")
    f.write("Scraping from " + url + "\n\n\n")
    driver.get(url)
    time.sleep(1)
    result = driver.execute_script("return document.documentElement.outerHTML")
    return BeautifulSoup(result, 'html.parser')

soup = scraping("https://www.polkcountyiowa.gov/news-and-announcements/updated-polk-county-service-modifications-and-closures-04-01-2020/")
data = soup.find_all(class_="py-3")
for i in range(len(data)):
    f.write(data[i].get_text(separator = '\n'))
    
soup = scraping("https://www.polkcountyiowa.gov/health-department/2019-novel-coronavirus-covid-19/")
data = soup.find_all(class_="nav-link")
links = []
for i in range(len(data)):
    if data[i]['href'] not in links:
        links.append(data[i]['href'])
scrapelinks = []
for i in range(len(links)):
    if "2019-novel-coronavirus-covid-19" in links[i]:
        scrapelinks.append("https://www.polkcountyiowa.gov" + links[i])
        
soup = scraping("https://www.polkcountyiowa.gov/health-department/2019-novel-coronavirus-covid-19/first-responders-covid-19-resources/")
data = soup.find_all()
scrapelinks2 = []
for i in range(len(scrapelinks)):
    soup = scraping(scrapelinks[i])
    data = soup.find_all("a")
    for i in range(len(data)):
        scrapelinks2.append(data[i]['href'])
PDFS = []
done = []
for i in range(len(scrapelinks2)):
    if ".pdf" in scrapelinks2[i] and "toolkit" not in scrapelinks2[i]:
        PDFS.append(scrapelinks2[i])
    if "health" in scrapelinks2[i] and scrapelinks2[i][0] == "/" and scrapelinks2[i] not in done:
        done.append(scrapelinks2[i])
        soup = scraping("https://www.polkcountyiowa.gov" + scrapelinks2[i])
        data = soup.find_all("p")
        for i in range(len(data)):
            f.write(data[i].get_text(separator = '\n'))
    # if "http" in scrapelinks2[i] and "19" in scrapelinks2[i] and scrapelinks2[i] not in done:
    #     done.append(scrapelinks2[i])
    #     soup = scraping(scrapelinks2[i])
    #     data = soup.find_all("p")
    #     for i in range(len(data)):
    #         f.write(data[i].get_text(separator = '\n'))

import PyPDF2
import io

import requests
from PyPDF2 import PdfFileReader


path = "../data/" + COUNTY + "-PDF"
fileDir = os.path.dirname(__file__)
filePath = os.path.join(fileDir, path)
filePath = os.path.abspath(os.path.realpath(filePath))
os.makedirs(filePath, exist_ok=True)

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
    print("Scraping from" + url)
    if url[0] == "/":
        getPDFs("https://www.polkcountyiowa.gov" + url, COUNTY)    
        r = requests.get("https://www.polkcountyiowa.gov" + url)
    else:
        getPDFs(url, COUNTY)
        continue
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





# In[ ]:




