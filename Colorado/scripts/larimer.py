#!/usr/bin/env python
# coding: utf-8

# In[32]:


import requests 
from bs4 import BeautifulSoup 
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time


f = open("larimer.txt", "w")
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

def getPDFs(file_url):
    title = file_url.split('/').pop()
    r = requests.get(file_url, stream = True)
    for chunk in r.iter_content(chunk_size=1024):
        if chunk:
             f.write(chunk.text)
    return "data/" + title
    
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
    

f.close()
driver.quit()
print("finished")


# In[ ]:




