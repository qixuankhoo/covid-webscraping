import requests 
from bs4 import BeautifulSoup 
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time

f = open("../data/pueblo.txt", "w")
url = "https://county.pueblo.org/board-county-commissioners/covid-19-variance-information"


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
    


soup = scraping(url)


data = soup.find_all("div", class_= "paragraph paragraph--type--bp-simple paragraph--view-mode--default paragraph--id--7277")
for i in range(len(data)):
    f.write(data[i].text)
    print(data[i].text)
    f.write("\n\n\n")




# scrap from https://county.pueblo.org/public-health/covid-19
f.write("--------------------------------------------")
url = "https://county.pueblo.org/public-health/covid-19"
#paragraph__column paragraph-content
soup = scraping(url)

data = soup.find_all("div", class_= "field field--name-bp-text field--type-text-long field--label-hidden field--item")
for i in range(len(data)):
    f.write(data[i].text)
    print(data[i].text)
    f.write("\n\n\n")
    
f.close()
print("finished")
