import requests 
from bs4 import BeautifulSoup 
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time
import os


COUNTY = "union"
fileDir = os.path.dirname(__file__)
filePath = os.path.join(fileDir, "../data/union.txt")
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

soup = scraping("https://www.unioncountync.gov/news/county-facilities-closed-independence-day?ccm_paging_p=1&ccm_order_by=&ccm_order_by_direction=")
data = soup.find_all(class_="pagination")
for i in range(len(data)):
    s = data[i].get_text()
    s = s.split("…")
    s = s[1].split("N")
    pages = int(s[0])

for i in range(pages):
    if i == 0:
        continue
    soup = scraping("https://www.unioncountync.gov/news/county-facilities-closed-independence-day?ccm_paging_p=" + str(i) + "&ccm_order_by=&ccm_order_by_direction=")
    data = soup.find_all("a", class_="ccm-block-page-list-read-more")
    print(data)
    for y in range(len(data)):
        soup = scraping(data[y]['href'])
        data1 = soup.find_all(class_="uc-box")
        for j in range(len(data1)):
            f.write(data1[j].get_text(separator = '\n'))

PDFS = set()

soup = scraping("https://www.unioncountync.gov/news/coronavirus-what-you-need-know")
data1 = soup.find(class_ = "uc-box")
data = data1.find_all("p")
for i in range(len(data)):
    f.write(data[i].get_text(separator = '\n'))
data = data1.find_all('li')
for i in range(len(data)):
    f.write(data[i].get_text(separator = '\n'))
data = data1.find_all("a", href = True)
for i in range(len(data)):
    try:
        g = data[i]['href']
    except Exception:
        continue
    if "download_file" in data[i]['href'] or ".pdf" in data[i]['href']:
        if data[i]['href'][0] == "/":
            PDFS.add("https://www.unioncountync.gov" + data[i]['href'])
        else:
            PDFS.add(data[i]['href'])
    elif "unioncountync.gov" in data[i]['href']:
        soup = scraping(data[i]['href'])
        data = soup.find_all("p")
        for i in range(len(data)):
            f.write(data[i].get_text(separator = '\n'))
    elif data[i]['href'][0] == "/":
        soup = scraping("https://www.unioncountync.gov" + data[i]['href'])
        data = soup.find_all("p")
        for i in range(len(data)):
            f.write(data[i].get_text(separator = '\n'))
data1 = soup.find(class_ = "uc-list")
data = data1.find_all("p")
for i in range(len(data)):
    f.write(data[i].get_text(separator = '\n'))
data = data1.find_all('li')
for i in range(len(data)):
    f.write(data[i].get_text(separator = '\n'))
data = data1.find_all("a", href = True)
for i in range(len(data)):
    try:
        g = data[i]['href']
    except Exception:
        continue
    if "download_file" in data[i]['href'] or ".pdf" in data[i]['href']:
        if data[i]['href'][0] == "/":
            PDFS.add("https://www.unioncountync.gov" + data[i]['href'])
        else:
            PDFS.add(data[i]['href'])
    elif "unioncountync.gov" in data[i]['href']:
        soup = scraping(data[i]['href'])
        data = soup.find_all("p")
        for i in range(len(data)):
            f.write(data[i].get_text(separator = '\n'))
    elif data[i]['href'][0] == "/":
        soup = scraping("https://www.unioncountync.gov" + data[i]['href'])
        data = soup.find_all("p")
        for i in range(len(data)):
            f.write(data[i].get_text(separator = '\n'))
data1 = soup.find("h4")
data = data1.find_all("p")
for i in range(len(data)):
    f.write(data[i].get_text(separator = '\n'))
data = data1.find_all('li')
for i in range(len(data)):
    f.write(data[i].get_text(separator = '\n'))
data = data1.find_all("a", href = True)
for i in range(len(data)):
    try:
        g = data[i]['href']
    except Exception:
        continue
    if "download_file" in data[i]['href'] or ".pdf" in data[i]['href']:
        if data[i]['href'][0] == "/":
            PDFS.add("https://www.unioncountync.gov" + data[i]['href'])
        else:
            PDFS.add(data[i]['href'])
    elif "unioncountync.gov" in data[i]['href']:
        soup = scraping(data[i]['href'])
        data = soup.find_all("p")
        for i in range(len(data)):
            f.write(data[i].get_text(separator = '\n'))
    elif data[i]['href'][0] == "/":
        soup = scraping("https://www.unioncountync.gov" + data[i]['href'])
        data = soup.find_all("p")
        for i in range(len(data)):
            f.write(data[i].get_text(separator = '\n'))


f.close()
driver.quit()
print("finished")