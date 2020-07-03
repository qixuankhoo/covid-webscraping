import requests 
from bs4 import BeautifulSoup 
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time
import os


COUNTY = "saginaw"
fileDir = os.path.dirname(__file__)
filePath = os.path.join(fileDir, "../data/saginaw.txt")
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

soup = scraping("http://www.saginawpublichealth.org/coronavirus/")
data1 = soup.find(id = "sidenav")
data = soup.find_all("a", class_ = "nav-link")
mainlinks = set()
for i in range(len(data)):
    if data[i]['href'] == '#':
        continue
    mainlinks.add("http://www.saginawpublichealth.org" + data[i]['href'])

sublinks = set()
for i in mainlinks:
    soup = scraping(i)
    data1 = soup.find(id = "main")
    data = data1.find_all("a")
    for i in range(len(data)):
        if data[i]['href'][0] == "/":
            sublinks.add("http://www.saginawpublichealth.org" + data[i]['href'])
        else:
            sublinks.add(data[i]['href'])
    data = data1.find_all("p")
    for i in range(len(data)):
        f.write(data[i].get_text(separator = '\n'))
    data = data1.find_all("li")
    for i in range(len(data)):
        f.write(data[i].get_text(separator = '\n'))


PDFS = []
for i in sublinks:
    if ".jpg" in i or i in mainlinks:
        continue
    elif ".pdf" in i:
        PDFS.append(i)
    elif "saginawpublichealth.org" in i:
        soup = scraping(i)
        data1 = soup.find(id = "main")
        data = data1.find_all("p")
        for i in range(len(data)):
            f.write(data[i].get_text(separator = '\n'))
        data = data1.find_all("li")
        for i in range(len(data)):
            f.write(data[i].get_text(separator = '\n'))

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
    title = file_url.split('/').pop()[0:200]
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
    getPDFs(url, COUNTY)
    try:
       r = requests.get(url)
    except Exception:
        continue
    fi = io.BytesIO(r.content)
    try:
        reader = PdfFileReader(fi)
    except Exception:
        continue
    number_of_pages = reader.getNumPages()
    for page_number in range(number_of_pages):
        page = reader.getPage(page_number)
        page_content = page.extractText()
        f.write(page_content)

f.close()
driver.quit()
print("finished")