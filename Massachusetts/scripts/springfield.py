import requests 
from bs4 import BeautifulSoup 
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time
import os


COUNTY = "springfield"
fileDir = os.path.dirname(__file__)
filePath = os.path.join(fileDir, "../data/springfield.txt")
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

#currentPageContentMenu a

soup = scraping("https://www.springfield-ma.gov/cos/index.php?id=covid")
data = soup.find(id = "currentPageContentMenu")
data = data.find_all("a")
mainlinks = set()
for i in range(len(data)):
    mainlinks.add("https://www.springfield-ma.gov/cos/" + data[i]['href'])

sublinks = set()
for l in mainlinks:
    soup = scraping(l)
    data1 = soup.find(id = "content")
    data = data1.find_all("p")
    for i in range(len(data)):
        f.write(data[i].get_text(separator = '\n'))
    data = data1.find_all("li")
    for i in range(len(data)):
        f.write(data[i].get_text(separator = '\n'))
    data = data1.find_all("a")
    for i in range(len(data)):
        sublinks.add(data[i]['href'])

PDFS = set()
print("GOT HERE")
for i in sublinks:
    if i in mainlinks:
        continue
    if "pdf" in i:
        PDFS.add(i)
    elif "springfield-ma.gov" in i:
        soup = scraping(i)
        data1 = soup.find(id = "content")
        data = data1.find_all("p")
        for i in range(len(data)):
            f.write(data[i].get_text(separator = '\n'))
        data = data1.find_all("li")
        for i in range(len(data)):
            f.write(data[i].get_text(separator = '\n'))
print("GOT HERE")
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
    if "http" not in url and "www" not in url:
        print(url)
        try:
            getPDFs("https://www.springfield-ma.gov/cos/" + url, COUNTY)  
        except Exception:
            print("FAIL")
            continue  
        r = requests.get("https://www.springfield-ma.gov/cos/" + url)
    else:
        try:
            getPDFs(url, COUNTY)
        except Exception:
            continue
        r = requests.get(url)
    try:
        fi = io.BytesIO(r.content)
    except Exception:
        continue
    try:
        reader = PdfFileReader(fi)
    except Exception:
        continue
    try:
        number_of_pages = reader.getNumPages()
    except Exception:
        continue
    for page_number in range(number_of_pages):
        page = reader.getPage(page_number)
        page_content = page.extractText()
        f.write(page_content)


f.close()
driver.quit()
print("finished")