import requests 
from bs4 import BeautifulSoup 
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time
import os
import re

f = open("../data/johnson.txt", "w")


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
            links.append(link.get('href'))


# scraping from https://www.johnson-county.com/dept_health.aspx?id=27320
url = "https://www.johnson-county.com/dept_health.aspx?id=27320"
soup = scraping(url)
data = soup.select("p")
links = []
for i in range(len(data)):
    for link in data[i].select('a:first-child'):
        links.append(link.get('href'))

print(links)



# make directory for pdfs



# start scraping for pdfs
path = "../data/" + "johnson-PDF"
os.mkdir(path)

def pdfs(link):
    print("Scraping from " + link)
    f.write("Scraping from " + link + "\n\n\n")
    try:
        r = requests.get(link, verify = False, stream = True)

        if r.headers['Content-Type'] == "application/pdf":
            f.write("A PDF HERE\n\n\n")
            print("pdf " + link)
            d = r.headers['Content-Disposition']
            pre_title = re.findall("filename=(.+)", d)[0]

            title = re.findall("\"(.*?)\"", pre_title)[0]
            with open("../data/johnson-PDF/" + title,"wb") as pdf:
                for chunk in r.iter_content(chunk_size=1024):
                    if chunk:
                        pdf.write(chunk)
        else:
            print("----" + link)

    except:
        pass


for link in links:
    print("processing...")
    print(link)
    pdfs(link)


# scraping from https://coronavirus-johnsoncounty.hub.arcgis.com/pages/frequently-asked-questions
url = "https://coronavirus-johnsoncounty.hub.arcgis.com/pages/frequently-asked-questions"
soup = scraping(url)


data = soup.find_all("div", class_= "markdown-card ember-view")
for i in range(len(data)):
    f.write(data[i].text)
    f.write("\n\n\n")


# scraping from https://coronavirus-johnsoncounty.hub.arcgis.com/"
url = "https://coronavirus-johnsoncounty.hub.arcgis.com/"
soup = scraping(url)


data = soup.find_all("div", id= "ember63")
for i in range(len(data)):
    f.write(data[i].text)
    f.write("\n\n\n")


f.close()
driver.quit()
print("finished")

