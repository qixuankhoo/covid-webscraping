import requests 
from bs4 import BeautifulSoup 
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time
import os


COUNTY = "east_baton_rouge"
fileDir = os.path.dirname(__file__)
filePath = os.path.join(fileDir, "../data/east_baton_rouge.txt")
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


soup = scraping("https://www.brla.gov/2175/Restart-BR")
data = soup.find_all(class_= "secondaryNavItem")
list = set()
for i in range(len(data)):
    list.add("https://www.brla.gov" + data[i]['href'])


sublinks = set()
for i in list:
    soup = scraping(i)
    data1 = soup.find(id = "page")
    data = data1.find_all("li")
    for i in range(len(data)):
        f.write(data[i].get_text(separator = '\n'))
    data = data1.find_all("p")
    for i in range(len(data)):
        f.write(data[i].get_text(separator = '\n'))
    data = soup.find(id = "page")
    data = data.find_all("a")
    for i in range(len(data)):
        sublinks.add(data[i]['href'])

for i in sublinks:
    if i[0] == "/":
        sublinks.remove(i)
        sublinks.add("https://www.brla.gov" + i)

PDFS = []
for i in sublinks:
    print("idk")
    print(i)
    if "Word" in i:
        continue
    if ("Center/View" in i and "brla.gov" in i) or ".pdf" in i or "brla.gov/businessguidelines" in i:
        PDFS.append(i)
    elif "brla.gov" in i:
        soup = scraping(i)
        data = soup.find_all("p")
        for y in range(len(data)):
            f.write(data[y].get_text(separator = '\n'))

import glob

import requests

path = "../data/" + COUNTY + "-PDF"
fileDir = os.path.dirname(__file__)
filePath = os.path.join(fileDir, path)
filePath = os.path.abspath(os.path.realpath(filePath))
os.makedirs(filePath, exist_ok=True)

def getPDFs(file_url, county):
    title = file_url.split('/').pop()
    if ".pdf" not in title:
        title += ".pdf"
    r = requests.get(file_url, stream = True)
    with open("../data/" + county + "-PDF" + "/" + title,"wb") as pdf:
        for chunk in r.iter_content(chunk_size=1024*1024):
            pdf.write(chunk)


for url in PDFS:
    getPDFs(url, COUNTY)
    
driver.quit()
print("finished")
