import requests 
from bs4 import BeautifulSoup 
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time
import os

f = open("../data/lowell.txt", "w")
url = "http://lowellma.gov/coronavirus"

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
    

# Scraping from http://lowellma.gov/coronavirus
soup = scraping(url)
links = []
data = soup.find_all("div", id= "structuralContainer6")


    
for i in range(len(data)):
    f.write(data[i].text)
    f.write("\n\n\n")
    for link in data[i].find_all('a'):
        current = link.get('href')
        if (current.startswith("http")):
            links.append(current)
        else:
            links.append("http://lowellma.gov" +current)
        
#print(links)
link.append("http://lowellma.gov/1449/Wear-A-Mask-In-Public")



# make directory for pdfs
path = "../data/" + "lowell-PDF"
os.mkdir(path)


# start scraping for pdfs
def getPDFs(file_url):
    r = requests.get(file_url, stream = True)
    if (r.headers['Content-Type'] != "application/pdf"):
        f.write("Not scrapped")
        return
    f.write("A PDF HERE")
    title = file_url.split('/').pop()
    with open("../data/" + "lowell-PDF" + "/" + title + ".pdf","wb") as pdf:
        for chunk in r.iter_content(chunk_size=1024):
         if chunk:
             pdf.write(chunk)

# only scrape links which are a pdf.
for link in links:
    f.write("Scraping from " + link + "\n\n\n")
    r = requests.get(link, stream = True)
#    print(r.headers)
    getPDFs(link)
    f.write("\n\n\n")




f.close()
driver.quit()
print("finished")
