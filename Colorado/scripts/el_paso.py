#!/usr/bin/env python
# coding: utf-8

# In[45]:


import requests 
from bs4 import BeautifulSoup 
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time


f = open("../data/el_paso.txt", "w")
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
urls = ["https://www.elpasocountyhealth.org/outbreaks-in-el-paso-county",
       "https://www.elpasocountyhealth.org/covid-19-testing-information",
       "https://www.elpasocountyhealth.org/safer-at-home-phase",
       "https://www.elpasocountyhealth.org/managing-symptoms-at-home",
       "https://www.elpasocountyhealth.org/personal-protective-equipment-and-cloth-face-coverings",
       "https://www.elpasocountyhealth.org/managing-mental-and-emotional-needs",
       "https://www.elpasocountyhealth.org/news/news-release/2020/el-paso-county-public-health-provides-update-to-el-paso-county-board-of",
       "https://www.elpasoco.com/el-paso-county-public-health-presents-restaurant-variance-request-el-paso-county-board-commissioners/"]
for url in urls:
    soup = scraping(url)
    data = soup.find_all("p")
    for i in range(len(data)):
        f.write(data[i].text)



f.close()
driver.quit()
print("finished")


# In[ ]:




