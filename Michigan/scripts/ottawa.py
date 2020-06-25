import requests 
from bs4 import BeautifulSoup 
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time

f = open("../data/ottawa.txt", "w")

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
    
# Scraping from https://www.miottawa.org/Health/OCHD/coronavirus.htm
url = "https://www.miottawa.org/Health/OCHD/coronavirus.htm"
soup = scraping(url)

links = []
data = soup.find_all("ul", class_= "styled")
#print(data)
for i in range(len(data)):
    for link in data[i].select('li a'):
        current = link.get('href')
        if current.startswith("https://content.govdelivery.com"):
            links.append(current)
links.append(current)

print(links)

for link in links:
    f.write("Scraping from " + link)
    html_content = requests.get(link).text
    soup = BeautifulSoup(html_content, 'html.parser')
    f.write(soup.text)
    f.write("\n\n\n")
    
f.close()
driver.quit()
print("finished")
