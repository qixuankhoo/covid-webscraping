import requests 
from bs4 import BeautifulSoup 
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time
import os


COUNTY = "spokane"
fileDir = os.path.dirname(__file__)
filePath = os.path.join(fileDir, "../data/spokane.txt")
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

newslinks = set()
soup = scraping("https://www.spokanecounty.org/CivicAlerts.aspx?CID=9")
data = soup.find_all("a", class_ = "more")
for i in range(len(data)):
    newslinks.add("https://www.spokanecounty.org/" + data[i]['href'])
for i in newslinks:
    soup = scraping(i)
    data = soup.find_all(class_ = "fr-view")
    for y in range(len(data)):
        f.write(data[y].get_text(separator = '\n'))

PDFS = set()
soup = scraping("https://www.spokanecounty.org/4589/COVID-19-Information")
data1 = soup.find(id = "moduleContent")
data = data1.find_all("p")
for i in range(len(data)):
    f.write(data[i].get_text(separator = '\n'))
data = data1.find_all("li")
for i in range(len(data)):
    f.write(data[i].get_text(separator = '\n'))

soup = scraping("https://www.spokanecounty.org/4605/COVID-19")
data1 = soup.find(id = "moduleContent")
data = data1.find_all("p")
for i in range(len(data)):
    f.write(data[i].get_text(separator = '\n'))
data = data1.find_all("li")
for i in range(len(data)):
    f.write(data[i].get_text(separator = '\n'))
data = data1.find_all("a")
for i in range(len(data)):
    if "DocumentCenter" in data[i]['href']:
        if "spokecounty.org" not in data[i]['href']:
            PDFS.add("https://www.spokanecounty.org" + data[i]['href'])
        else:
            PDFS.add(data[i]['href'])

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import webbrowser
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--start-maximized")
directory = os.getcwd()[:-7] + "data/" + COUNTY + "-PDF"
prefs = {"download.default_directory": 
                            directory}
chrome_options.add_experimental_option("prefs", prefs)
chrome_options.add_argument('--headless')
chrome_options.add_argument("--enable-javascript")
driver = webdriver.Chrome(ChromeDriverManager().install(), options = chrome_options)
driver.get("https://www.spokanecounty.org/DocumentCenter/Index/2565")
time.sleep(3)
download_button = driver.find_element_by_xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "t-arrow-next", " " ))]')
#download_button.click()
content = driver.find_elements_by_class_name("pdf")
for link in content:
    PDFS.add(link.get_attribute("href"))
for i in range(3):
    download_button.click()
    time.sleep(2)
    content = driver.find_elements_by_class_name("pdf")
    for link in content:
        PDFS.add(link.get_attribute("href"))


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
    count = 1
    title = file_url.split('/').pop()
    r = requests.get(file_url, stream = True)
    path = "../data/" + COUNTY + "-PDF" + "/" + title + ".pdf"
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
