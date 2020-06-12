import requests 
from bs4 import BeautifulSoup 
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time

f = open("../data/arapahoe.txt", "w")
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
    

url = "https://www.arapahoegov.com/2098/COVID-19-News-Updates"
soup = scraping(url)

links = []
data = soup.find_all("div", class_= "fr-view")


for i in range(len(data)):
    for link in data[i].find_all('a'):
        links.append(link.get('href'))

#
for link in links:
    currSoup = scraping(link)
    currdata = currSoup.find_all("div", class_= "content")
    for i in range(len(currdata)):
        f.write(currdata[i].text)



# scrap from https://www.arapahoegov.com/covid19
f.write("--------------------------------------------")
url = "https://www.arapahoegov.com/covid19"
soup = scraping(url)
data = soup.find_all("div", class_= "widget editor pageStyles wide")
for i in range(len(data)):
    f.write(data[i].text)
    f.write("\n\n\n")

f.close()
driver.quit()
print("finished")
