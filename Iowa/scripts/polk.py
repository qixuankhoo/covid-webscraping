#!/usr/bin/env python
# coding: utf-8

# In[32]:


import requests 
from bs4 import BeautifulSoup 
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time


f = open("../data/polk.txt", "w")
#f = open("polk.txt", "w")
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
    f.write(data[i].text)
    
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
            f.write(data[i].text)
    if "http" in scrapelinks2[i] and "19" in scrapelinks2[i] and scrapelinks2[i] not in done:
        done.append(scrapelinks2[i])
        soup = scraping(scrapelinks2[i])
        data = soup.find_all("p")
        for i in range(len(data)):
            f.write(data[i].text)

import PyPDF2
import io

import requests
from PyPDF2 import PdfFileReader


for url in PDFS:
    print("Scraping from" + url)
    if url[0] == "/":
        r = requests.get("https://www.polkcountyiowa.gov" + url)
    else:
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




