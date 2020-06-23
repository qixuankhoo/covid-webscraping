import requests 
from bs4 import BeautifulSoup 
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time
import os

f = open("../data/woodbury.txt", "w")


def scraping(url):
    print("Scraping from " + url)
    f.write("Scraping from " + url + "\n\n\n")
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    driver = webdriver.Chrome(ChromeDriverManager().install(), options = chrome_options)
    driver.get(url)
    time.sleep(1)
    result = driver.execute_script("return document.documentElement.outerHTML")
    driver.quit()
    return BeautifulSoup(result, 'html.parser')
    
def findHref(data):
    for i in range(len(data)):
        for link in data[i].find_all('a'):
            current = link.get('href')
            if (current.startswith('http')):
                link.append(current)
            else:
                links.append("http://siouxlanddistricthealth.org" + current)



url = "http://siouxlanddistricthealth.org/component/content/article/4-a-z-search/231-covid-19.html?directory=85"
soup = scraping(url)
links = []

data = soup.find_all("table", class_= "contentpaneopen")
findHref(data)
print(links)
for i in range(len(data)):
    f.write(data[i].text)
    f.write("\n\n\n")


# make directory for pdfs
path = "../data/" + "woodbury-PDF"
os.mkdir(path)


# start scraping for pdfs
def getPDFs(file_url):
    r = requests.get(file_url, stream = True)
    if (r.headers['Content-Type'] != "application/pdf"):
        f.write("Not scrapped")
        return
    f.write("A PDF HERE")
    title = file_url.split('/').pop()
    with open("../data/" + "woodbury-PDF" + "/" + title,"wb") as pdf:
        for chunk in r.iter_content(chunk_size=1024):
         if chunk:
             pdf.write(chunk)

# only scrape links which are a pdf.
for link in links:
    f.write("Scraping from " + link + "\n\n\n")
    getPDFs(link)
    f.write("\n\n\n")




f.close()
print("finished")
