import requests 
from bs4 import BeautifulSoup 
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time
import os

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
driver = webdriver.Chrome(ChromeDriverManager().install(), options = chrome_options)

f = open("../data/boulder.txt", "w")
COUNTY = "boulder"
def advanced_scraping(url):
    print("Scraping from " + url)
    f.write("\n\n\n")
    f.write("Scraping from " + url + "\n\n\n")
    driver.get(url)
    time.sleep(1)
    driver.execute_script("jQuery('#news-list-2020').dataTable().fnDestroy();")
    result = driver.execute_script("return document.documentElement.outerHTML")
    return BeautifulSoup(result, 'html.parser')
    
def scraping(url):
    print("Scraping from " + url)
    f.write("\n\n\n")
    f.write("Scraping from " + url + "\n\n\n")
    driver.get(url)
    time.sleep(1)
    result = driver.execute_script("return document.documentElement.outerHTML")
    return BeautifulSoup(result, 'html.parser')

def findHref(data):
    for i in range(len(data)):
        for link in data[i].find_all('a'):
            links.append(link.get('href'))
            
def scraping2(link, tag, class_name, county):
    print("Scraping from " + link)
    f.write("Scraping from " + link + "\n\n\n")
    driver.get(link)
    time.sleep(5)
    body = driver.find_element_by_tag_name('body')
    if body.text.strip():
        print("html " + link)
        result = driver.execute_script("return document.documentElement.outerHTML")
        soup = BeautifulSoup(result, 'html.parser')
        writeData(soup, tag, class_name)
    else:
        f.write("A PDF HERE\n\n\n")
        print("pdf " + link)
        result = driver.current_url
        data = getPDFs(result, county)
        
def getPDFs(file_url, county):
    title = file_url.split('/').pop()
    r = requests.get(file_url, stream = True)
    with open("../data/" + COUNTY + "-PDF" + "/" + title,"wb") as pdf:
        for chunk in r.iter_content(chunk_size=1024):
         if chunk:
             pdf.write(chunk)
    return "data/" + title
    
def writeData(soup, tag, class_name):
    currdata = soup.find_all(tag, class_= class_name)
    for i in range(len(currdata)):
        print(currdata[i].text)
        f.write(currdata[i].text)
        print(currdata[i].text)

# create a folder for PDFs

path = "../data/" + COUNTY + "-PDF"
os.mkdir(path)
        
# scrap from "https://www.bouldercounty.org/news/"
url = "https://www.bouldercounty.org/news/"
soup = advanced_scraping(url)
links = []
data = soup.find_all("a", class_= "read-more-link")


for a_tag in data:
    links.append(a_tag.get('href'))

for link in links:
    if link == 'https://www.bouldercounty.org/news/single-fatality-confirmed-after-fire-ignites-at-lydia-morgan-senior-housing-in-louisville/':
        break
    currSoup = scraping(link)
    currdata = currSoup.find_all("div", class_= "vc_col-sm-9")
    for i in range(len(currdata)):
        f.write(currdata[i].text)
        f.write("\n\n\n")




# scrap from "https://www.bouldercounty.org/families/disease/covid-19/covid-19-resources/"
f.write("--------------------------------------------")
url = "https://www.bouldercounty.org/families/disease/covid-19/covid-19-resources/"
soup = scraping(url)
data = soup.find_all("div", class_= "wpb_wrapper")
for i in range(len(data)):
    f.write(data[i].text)
    f.write("\n\n\n")



# scrap from "https://www.bouldercounty.org/families/disease/covid-19/prevention"
f.write("--------------------------------------------")
url = "https://www.bouldercounty.org/families/disease/covid-19/prevention/"
soup = scraping(url)
data = soup.find_all("div", class_= "vc_col-sm-8 wpb_column column_container col no-padding color-dark")
for i in range(len(data)):
    f.write(data[i].text)
    f.write("\n\n\n")

# scrap from "https://www.bouldercounty.org/families/disease/covid-19/disease/"
url = "https://www.bouldercounty.org/families/disease/covid-19/disease/"
soup = scraping(url)
data = soup.select("#content > div:nth-child(2) > div > div.vc_col-sm-8.wpb_column.column_container.col.no-padding.color-dark > div > div.vc_tta-container")
for i in range(len(data)):
    print(data[i].text)
    f.write(data[i].text)
    print(data[i].text)
    

links = []
data = soup.select("#content > div:nth-child(2) > div > div.vc_col-sm-8.wpb_column.column_container.col.no-padding.color-dark > div > div.wpb_text_column.wpb_content_element > div > h3")
for i in range(len(data)):
    index = i + 2
    selector = "#content > div:nth-child(2) > div > div.vc_col-sm-8.wpb_column.column_container.col.no-padding.color-dark > div > div.wpb_text_column.wpb_content_element > div > h3:nth-child(" + str(index) + ")"
    element = soup.select(selector)
    findHref(element)
for link in links:
    print("-----------------------")
    scraping2(link, "div", "wpb_text_column wpb_content_element", COUNTY)
    
# scrap from "https://www.bouldercounty.org/families/disease/covid-19/public-health-orders/"
url = "https://www.bouldercounty.org/families/disease/covid-19/public-health-orders/"
soup = scraping(url)
data = soup.select("#content > div:nth-child(2) > div > div.vc_col-sm-8.wpb_column.column_container.col.no-padding.color-dark > div > div > div > ul:nth-child(5)")
data1 = soup.select("#content > div:nth-child(2) > div > div.vc_col-sm-8.wpb_column.column_container.col.no-padding.color-dark > div > div > div > ul:nth-child(7)")

links = []
findHref(data)
findHref(data1)

DEBUG = True

chrome_options = webdriver.ChromeOptions()
if not DEBUG:
    chrome_options.add_argument('--headless')
driver = webdriver.Chrome(ChromeDriverManager().install(), options = chrome_options)

for link in links:
    scraping2(link, "div", "wpb_wrapper", COUNTY)


# ------------------------------


f.close()
driver.quit()
print("finished")
