import requests 
from bs4 import BeautifulSoup 
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time
import os

f = open("../data/kalamazoo.txt", "w")

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
driver = webdriver.Chrome(ChromeDriverManager().install(), options = chrome_options)

def scraping(url):
    print("Scraping from " + url)
    f.write("Scraping from " + url + "\n\n\n")
    driver.get(url)
    time.sleep(2)
    result = driver.execute_script("return document.documentElement.outerHTML")
    return BeautifulSoup(result, 'html.parser')
# Make a directory
path = "../data/kalamazoo-PDF"
os.mkdir(path)

# Scraping from https://www.kalcounty.com/hcs/covid19news.php
url = "https://www.kalcounty.com/hcs/covid19news.php"
soup = scraping(url)
data = soup.find_all("div", class_= "main")
links = []
for i in range(len(data)):
    for link in data[i].select('a'):
        current = link.get('href')
        if current.startswith("http"):
            links.append(current)
        elif current.startswith("/"):
            links.append("https://www.kalcounty.com" + current)
            

def downloadImagePDFs(link):
    r = requests.get(link)
    if r.headers['Content-type'] == "application/pdf":
        f.write("Scraping from " + link + "\n\n\n")
        f.write("A PDF here.\n")
        title = link.split('/').pop()
        if "spanish" in title.lower():
            return
        with open("../data/" + "kalamazoo-PDF" + "/" + title,"wb") as pdf:
            for chunk in r.iter_content(chunk_size=1024):
                 if chunk:
                     pdf.write(chunk)
                     
for link in links:
    downloadImagePDFs(link)
    
    
    
# Scraping from https://www.kalcounty.com/hcs/covid19.php
url = "https://www.kalcounty.com/hcs/covid19.php"
soup = scraping(url)
data = soup.find_all("div", class_= "panel panel-primary")
f.write("Scraping from " + url + "\n\n\n")
for i in range(len(data)):
    f.write(data[i].text)
f.write("\n\n\n")
    
f.close()
driver.quit()
print("finished")
