import requests 
from bs4 import BeautifulSoup 
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time
import os


COUNTY = "snohomish"
fileDir = os.path.dirname(__file__)
filePath = os.path.join(fileDir, "../data/snohomish.txt")
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

soup = scraping("https://www.snohomishcountywa.gov/DocumentCenter/Index/6666")
data = soup.find_all("a", class_="t-link")
numbers = set()
for i in range(len(data)):
    if len(data[i].get_text()) > 2:
        continue
    numbers.add(data[i].get_text())
max = 0
for i in numbers:
    if int(i) > max:
        max = int(i)

soup = scraping("https://snohomishcountywa.gov/Archive.aspx?AMID=124")
data = soup.find(id = "modulecontent")
data = data.find_all("a", href = True)
links = set()
for i in range(len(data)):
    if "ADID" in data[i]['href']:
        links.add("https://snohomishcountywa.gov/" + data[i]['href'])

for i in links:
    soup = scraping(i)
    data1 = soup.find(class_ = "pageStyles")
    data = data1.find_all("p")
    for i in range(len(data)):
        f.write(data[i].get_text(separator = '\n'))
    data = data1.find_all("li")
    for i in range(len(data)):
        f.write(data[i].get_text(separator = '\n'))

PDFS = set()

soup = scraping("https://www.snohomishcountywa.gov/CivicAlerts.aspx?CID=59")
data = soup.find_all("a", class_ = "Hyperlink")
for i in range(len(data)):
    if "DocumentCenter/View" in data[i]['href'] and "snohomishcountywa.gov" not in data[i]['href']:
        PDFS.add("https://snohomishcountywa.gov" + data[i]['href'])

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
driver.get("https://www.snohomishcountywa.gov/DocumentCenter/Index/6666")
time.sleep(3)
download_button = driver.find_element_by_xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "t-arrow-next", " " ))]')
#download_button.click()
content = driver.find_elements_by_class_name("pdf")
for link in content:
    PDFS.add(link.get_attribute("href"))
for i in range(max - 1):
    download_button.click()
    time.sleep(2)
    content = driver.find_elements_by_class_name("pdf")
    for link in content:
        print("LLOOK")
        print(link.get_attribute("href"))
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
    if len(title) == 0:
        title = "NONAME" + str(count)
    r = requests.get(file_url, stream = True)
    path = "../data/" + COUNTY + "-PDF" + "/" + title
    if os.path.isfile(path):
        path = "../data/" + COUNTY + "-PDF" + "/" + title + 1
        count = count + 1
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