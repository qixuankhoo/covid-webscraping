import requests 
from bs4 import BeautifulSoup 
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time

f = open("../data/king.txt", "w")
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
    
# Scraping from "https://www.kingcounty.gov/depts/health/covid-19.aspx"
url = "https://www.kingcounty.gov/depts/health/covid-19.aspx"
soup = scraping(url)

data = soup.find_all("div", class_= "panel-body")
links = []
first = True
for i in range(len(data)):
    for link in data[i].find_all('a'):
        current = link.get('href')
        if first:
            first = False
            continue
        if current.startswith("/depts/health/covid-19/languages/"): continue
        links.append("https://www.kingcounty.gov" + current)
links.append("https://www.kingcounty.gov/depts/health/covid-19/languages/ASL.aspx")
for link in links:
    f.write("Scraping from " +link)
    r = requests.get(link, stream = True)
    soup = BeautifulSoup(r.content, 'html.parser')
    data = soup.find_all("div", id="main-content-sr")
    for content in data:
        f.write(content.text)
        f.write("\n\n\n")


def findHref(data, count):
    for i in range(len(data)):
        for link in data[i].find_all('a'):
            current = link.get('href')
            if count >= 0: count = count - 1
            if count < 0: links.append("https://www.kingcounty.gov" + current)


# under https://www.kingcounty.gov/depts/health/covid-19/providers/LTCF.aspx  healthcare and service providers
soup = scraping("https://www.kingcounty.gov/depts/health/covid-19/providers/LTCF.aspx")
data = soup.select("#sidebar")

links = []
findHref(data, 4)

for link in links:
    f.write("Scraping from " +link)
    r = requests.get(link, stream = True)
    soup = BeautifulSoup(r.content, 'html.parser')
    data = soup.find_all("div", id="main-content-sr")
    for content in data:
        f.write(content.text)
        f.write("\n\n\n")


# under https://www.kingcounty.gov/depts/health/covid-19/support/emergency-food.aspx community support and well-being
soup = scraping("https://www.kingcounty.gov/depts/health/covid-19/support/emergency-food.aspx")
data = soup.select("#sidebar")

links = []
findHref(data, 5)
for link in links:
    f.write("Scraping from " +link)
    r = requests.get(link, stream = True)
    soup = BeautifulSoup(r.content, 'html.parser')
    data = soup.find_all("div", id="main-content-sr")
    for content in data:
        f.write(content.text)
        f.write("\n\n\n")


# under https://www.kingcounty.gov/depts/health/covid-19/care/testing.aspx Symptoms, testing and care
soup = scraping("https://www.kingcounty.gov/depts/health/covid-19/care/testing.aspx")
data = soup.select("#sidebar")

links = []
findHref(data, 4)
print(links)
for link in links:
    f.write("Scraping from " +link)
    r = requests.get(link, stream = True)
    soup = BeautifulSoup(r.content, 'html.parser')
    data = soup.find_all("div", id="main-content-sr")
    for content in data:
        f.write(content.text)
        f.write("\n\n\n")



# under https://www.kingcounty.gov/depts/health/covid-19/schools-childcare/positive-cases.aspx Schools and child care
soup = scraping("https://www.kingcounty.gov/depts/health/covid-19/schools-childcare/positive-cases.aspx")
data = soup.select("#sidebar")

links = []
findHref(data, 4)
for link in links:
    f.write("Scraping from " +link)
    r = requests.get(link, stream = True)
    soup = BeautifulSoup(r.content, 'html.parser')
    data = soup.find_all("div", id="main-content-sr")
    for content in data:
        f.write(content.text)
        f.write("\n\n\n")


# under https://www.kingcounty.gov/depts/health/covid-19/workplaces/grocery-stores.aspx Business
soup = scraping("https://www.kingcounty.gov/depts/health/covid-19/workplaces/grocery-stores.aspx")
data = soup.select("#sidebar")

links = []
findHref(data, 4)
for link in links:
    f.write("Scraping from " +link)
    r = requests.get(link, stream = True)
    soup = BeautifulSoup(r.content, 'html.parser')
    data = soup.find_all("div", id="main-content-sr")
    for content in data:
        f.write(content.text)
        f.write("\n\n\n")




# under https://www.kingcounty.gov/depts/health/covid-19/community-faith-organizations/FAQ.aspx Community and faith-based organizations
soup = scraping("https://www.kingcounty.gov/depts/health/covid-19/community-faith-organizations/FAQ.aspx")
data = soup.select("#sidebar")
links = []
findHref(data, 4)
for link in links:
    f.write("Scraping from " +link)
    r = requests.get(link, stream = True)
    soup = BeautifulSoup(r.content, 'html.parser')
    data = soup.find_all("div", id="main-content-sr")
    for content in data:
        f.write(content.text)
        f.write("\n\n\n")



f.close()
driver.quit()
print("finished")
