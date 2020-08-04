import requests 
from bs4 import BeautifulSoup 
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time
import os


COUNTY = "buncombe"
fileDir = os.path.dirname(__file__)
filePath = os.path.join(fileDir, "../data/buncombe.txt")
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

soup = scraping("https://www.buncombecounty.org/covid-19/default.aspx")
articles = set()
for i in range(100):
    data = soup.find(id = "cph_widgets_content_cph_widgets_ctl00_rptRecentPosts_hypTitle_" + str(i))
    if data is None:
        break
    articles.add("https://www.buncombecounty.org" + data['href'])


for i in articles:
    soup = scraping(i)
    data1 = soup.find(id = "center-column")
    data = data1.find_all("p")
    for y in range(len(data)):
        f.write(data[y].get_text(separator = '\n'))
    data = data1.find_all("li")
    for y in range(len(data)):
        f.write(data[y].get_text(separator = '\n'))    

soup = scraping("https://www.buncombecounty.org/covid-19/default.aspx")
PDFS = set()
data1 = soup.find(class_ = "list-col-4")
data = data1.find_all("a")
for i in range(len(data)):
    PDFS.add("https://www.buncombecounty.org" + data[i]['href'])

soup = scraping("https://www.buncombecounty.org/countycenter/news-detail.aspx?id=18543")
data1 = soup.find(id = "center-column")
data = data1.find_all("p")
for i in range(len(data)):
    f.write(data[i].get_text(separator = '\n'))
data = data1.find_all("li")
for i in range(len(data)):
    f.write(data[i].get_text(separator = '\n'))

soup = scraping("https://www.buncombecounty.org/countycenter/news-detail.aspx?id=18637")
data1 = soup.find(id = "center-column")
data = data1.find_all("p")
for i in range(len(data)):
    f.write(data[i].get_text(separator = '\n'))
data = data1.find_all("li")
for i in range(len(data)):
    f.write(data[i].get_text(separator = '\n'))

soup = scraping("https://www.buncombecounty.org/countycenter/news-detail.aspx?id=18653")
data = soup.find_all("a", class_="active")
for i in range(len(data)):
    if data[i].text == "English":
        PDFS.add("https://www.buncombecounty.org" + data[i]['href'])

soup = scraping("https://www.buncombecounty.org/covid-19/default.aspx#sec-questions-concerns")
data = soup.find_all(class_="panel-title")
for i in range(len(data)):
    f.write(data[i].get_text(separator = '\n'))

soup = scraping("https://www.buncombecounty.org/covid-19/default.aspx#sec-questions-concerns")
data = soup.find_all(class_ = "panel-body")
for i in range(len(data)):
    f.write(data[i].get_text(separator = '\n'))

soup = scraping("https://www.buncombecounty.org/covid-19/general-preparedness.aspx")
data1 = soup.find(id = "sec-general-preparedness")
data = data1.find_all("p")
for i in range(len(data)):
    f.write(data[i].get_text(separator = '\n'))
data = data1.find_all("li")
for i in range(len(data)):
    f.write(data[i].get_text(separator = '\n'))

soup = scraping("https://www.buncombecounty.org/covid-19/health-provider-information.aspx")
data1 = soup.find(id = "sec-providers-guidance")
data = data1.find_all("a")
for i in range(len(data)):
    PDFS.add(data[i]['href'])

data1 = soup.find(class_ = "col-sm-6")
data = data1.find_all("p")
for i in range(len(data)):
    f.write(data[i].get_text(separator = '\n'))
data = data1.find_all("li")
for i in range(len(data)):
    f.write(data[i].get_text(separator = '\n'))

data1 = soup.find(class_ = "list-col-2")
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
    getPDFs(url, COUNTY)
    print("Scraping from" + url)
    r = requests.get(url)
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