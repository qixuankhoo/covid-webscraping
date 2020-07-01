#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests 
from bs4 import BeautifulSoup 
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time
import os



COUNTY = "pottawattamie"
fileDir = os.path.dirname(__file__)
filePath = os.path.join(fileDir, "../data/pottawattamie.txt")
filePath = os.path.abspath(os.path.realpath(filePath))
f = open(filePath, 'w')
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
driver = webdriver.Chrome(ChromeDriverManager().install(), options = chrome_options)
from google_drive_downloader import GoogleDriveDownloader as gdd

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
    gdd.download_file_from_google_drive(file_id=google_id,
                                    dest_path=destination)

gdownload("https://drive.google.com/file/d/1cIh0t1fcpSORc-fbgApWMNSfGqgGltKJ/view", triPath + "/drive" + str(count) + ".pdf")

f.close()
driver.quit()
print("finished")


# In[ ]:




