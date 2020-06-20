import requests 
from bs4 import BeautifulSoup 
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time


f = open("../data/lafayette.txt", "w")


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
        
            links.append("https://lafayette.org/" + link.get('href'))

# scraping from doing business
# get all links
url = "https://lafayette.org/site453.php"
soup = scraping(url)

links = []

data = soup.select("#subnav")
findHref(data)


first = True
for link in links:
    if first:
        first = False;
        continue;
    soup = scraping(link)
    data = soup.select("#content")
    for i in range(len(data)):
        print(data[i].text)
        f.write(data[i].text)
        f.write("\n\n\n")

# scraping from https://lafayette.org/labor-jobs
url = "https://lafayette.org/labor-jobs"
soup = scraping(url)

links = []

data = soup.select("#subnav")
findHref(data)


first = True
for link in links:
    if first:
        first = False
        continue
    if link == "https://lafayette.org/site343.php":
        break
    soup = scraping(link)
    data = soup.select("#content")
    for i in range(len(data)):
        print(data[i].text)
        f.write(data[i].text)
        f.write("\n\n\n")


f.close()
driver.quit()
print("finished")

