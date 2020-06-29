import requests 
from bs4 import BeautifulSoup 
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time
import os

f = open("../data/lynn.txt", "w")
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
driver = webdriver.Chrome(ChromeDriverManager().install(), options = chrome_options)

def scraping(url):
    print("Scraping from " + url)
    f.write("Scraping from " + url + "\n\n\n")
    driver.get(url)
    time.sleep(1)
    result = driver.execute_script("return document.documentElement.outerHTML")
    return BeautifulSoup(result, 'html.parser')

def findHref(data):
    for i in range(len(data)):
        for link in data[i].find_all('a'):
            current = link.get('href')
            if (current.startswith("http")):
                links.append(current)
            else:
                links.append("http://www.lynnma.gov/covid19/" + current)

# Scraping from http://www.lynnma.gov/covid19/resources.shtml
# scrap all the texts in the link
link = "http://www.lynnma.gov/covid19/resources.shtml"
soup = scraping(link)
data = soup.find_all("div", class_= "p7GPcontent")
for i in range(len(data)):
    f.write(data[i].text)
    f.write("\n\n\n")

# Scraping from http://www.lynnma.gov/covid19/press.shtml
# scrap all the texts in the link
link = "http://www.lynnma.gov/covid19/press.shtml"
soup = scraping(link)
data = soup.find_all("div", class_= "p7GPcontent")
for i in range(len(data)):
    print(data[i].text)
    f.write(data[i].text)
    f.write("\n\n\n")

# Scraping from http://www.lynnma.gov/covid19/resources.shtml#p7GPc1_9
link = "http://www.lynnma.gov/covid19/resources.shtml#p7GPc1_9"
soup = scraping(link)
data = soup.find_all("div", id= "p7GPc1_9")
links = []
findHref(data)


# make directory for pdfs
path = "../data/" + "lynn-PDF"
os.mkdir(path)


# start scraping for pdfs
def getPDFs(file_url):
    r = requests.get(file_url, stream = True)
    if (r.headers['Content-Type'] != "application/pdf"):
        f.write("Not scrapped")
        return
    f.write("A PDF HERE")
    title = file_url.split('/').pop()
    with open("../data/" + "lynn-PDF" + "/" + title,"wb") as pdf:
        for chunk in r.iter_content(chunk_size=1024):
         if chunk:
             pdf.write(chunk)
    
for link in links:
    f.write("Scraping from " + link + "\n")
    getPDFs(link)
    f.write("\n\n\n")

driver.quit()
f.close()
print("finished")
