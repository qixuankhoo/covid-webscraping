#!/usr/bin/env python
# coding: utf-8

# In[43]:


import requests 
from bs4 import BeautifulSoup 
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time
import re


f = open("../data/larimer.txt", "w")
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

    
# scrap from https://www.elpasocountyhealth.org/outbreaks-in-el-paso-county
urls = ["https://www.larimer.org/health/communicable-disease/coronavirus-covid-19/larimer-county-positive-covid-19-numbers",
       "https://www.larimer.org/health/communicable-disease/coronavirus/faqs",
       "https://www.larimer.org/health/communicable-disease/coronavirus-covid-19/covid-19-information-healthcare-providers",
       "https://www.larimer.org/health/communicable-disease/coronavirus-covid-19/retirement-communities-long-term-care-and-nursing"]
for url in urls:
    soup = scraping(url)
    data = soup.find_all("p")
    for i in range(len(data)):
        f.write(data[i].text)

urls = ["https://www.larimer.org/health/communicable-disease/coronavirus-covid-19/safer-at-home",
       "https://www.larimer.org/health/communicable-disease/coronavirus-covid-19/think-or-know-you-have-covid-19/covid-19-testing",
       "https://www.larimer.org/contact-tracing",
       "https://www.larimer.org/health/communicable-disease/coronavirus-covid-19/home-care-and-testing-information/managing-stress",
       "https://www.larimer.org/health/communicable-disease/coronavirus-covid-19/schools-and-childcare/covid-19-resources-schools",
       "https://www.larimer.org/health/communicable-disease/coronavirus-covid-19/schools-and-childcare/covid-19-information",
       "https://www.larimer.org/health/communicable-disease/coronavirus-covid-19/face-coverings-and-masks",
       "https://www.larimer.org/health/communicable-disease/coronavirus-covid-19/protecting-our-community-0",
       ]
for url in urls:
    soup = scraping(url)
    data = soup.find_all("p")
    for i in range(len(data)):
        f.write(data[i].text)
    data = soup.find_all("li")
    for i in range(len(data)):
        f.write(data[i].text)
    
soup = scraping("https://www.larimer.org/health/communicable-disease/coronavirus-covid-19/covid-19-public-health-orders-and-press-releases")
data = soup.find_all(class_="externalLink")


def findHref(data):
    links = []
    pdfs = []
    for i in range(len(data)):
        links.append(data[i]['href'])
    for y in links:
        if "pdf" in y:
            pdfs.append(y)
    return pdfs

soup = scraping("https://www.larimer.org/health/communicable-disease/coronavirus-covid-19/covid-19-public-health-orders-and-press-releases")
data = soup.find_all(class_="externalLink", href = True)
pdfs = findHref(data)

import PyPDF2
import io

import requests
from PyPDF2 import PdfFileReader


for url in pdfs:
    print("Scraping from" + url)
    r = requests.get(url)
    fi = io.BytesIO(r.content)
    reader = PdfFileReader(fi)
    number_of_pages = reader.getNumPages()
    for page_number in range(number_of_pages):
        page = reader.getPage(page_number)
        page_content = page.extractText()
        f.write(page_content)

def findHrefs(data):
    links = []
    for i in range(len(data)):
        g = data[i].find_all('a')
        for h in g:
            if "spotlights" in h['href'] and "www." in h["href"]:
                links.append(h['href'])
    return links        

soup = scraping("https://www.larimer.org/health/communicable-disease/coronavirus-covid-19/covid-19-public-health-orders-and-press-releases")
data = soup.find_all("ul")
links = findHrefs(data)

for link in links:
    soup = scraping(link)
    data = soup.find_all("p")
    for i in range(len(data)):
        f.write(data[i].text)




# from larimer county
# In[3]:


url="https://www.larimer.org/health/communicable-disease/coronavirus-covid-19/think-or-know-you-have-covid-19/covid-19-testing"
page = urllib.request.urlopen(url)
soup = BeautifulSoup(page, 'html.parser')
print(soup)


# In[23]:


linksinfo=[]

links= soup.find_all('a')
content= soup.find_all('p')
for i in content:
    print((i.get_text()))
 
    
links= soup.find_all('a')p
for i in links:
    linksinfo.append(i.get_text() + ": " + str(i.get('href')))
    print(i.get_text())
    print(i.get('href'))
    
linksinfo

with open('larimer.txt','w') as outfile:
    outfile.write("CONTENT" + "\n" + "\n")
    for i in content:
        print(i.get_text(), file=outfile)
    outfile.write("\n" + "\n"+ "LINKS" + "\n" + "\n")
   
    for item in linksinfo:
        print(item, file=outfile)


# In[ ]:





f.close()
driver.quit()
print("finished")







