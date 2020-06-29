import requests 
from bs4 import BeautifulSoup 
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time
import os

f = open("../data/forsyth.txt", "w")

def findHref(data):
    for i in range(len(data)):
        for link in data[i].find_all('a'):
            current = link.get('href')
            if current.startswith("http"):
                links.append(current)
            else:
                links.append("https://durhamnc.gov" + current)
     
# Scraping from "http://www.forsyth.cc/covidupdate/#casecount" txt
url = "http://www.forsyth.cc/covidupdate/#casecount"
r = requests.get(url)
soup = BeautifulSoup(r.content, 'html.parser')
data = soup.select("#testing")
f.write("Scraping from " + url + "\n\n\n")
for i in range(len(data)):
    print(data[i].text)
f.write("\n\n\n")

data = soup.select("#casecount")
for i in range(len(data)):
    print(data[i].text)
f.write("\n\n\n")

data = soup.select("#about")
for i in range(len(data)):
    f.write(data[i].text)
f.write("\n\n\n")

data = soup.select("#clickherecomehere")
for i in range(len(data)):
    f.write(data[i].text)
f.write("\n\n\n")

data = soup.select("#contact")
for i in range(len(data)):
    f.write(data[i].text)
f.write("\n\n\n")


# Create directory for PDFs
path = "../data/forsyth-PDF"
os.mkdir(path)

link = "http://forsyth.cc/publichealth/documents/Mental_Health_Crisis_Resources_COVID_19_English.pdf"
r = requests.get(link, verify = False)
if r.headers['Content-type'] == "application/pdf":
    f.write("Scraping from " + link + "\n\n\n")
    f.write("A PDF here.\n")
    title = ""
    try:
        title = r.headers['Content-DocumentTitle']
    except:
        title = link.split('/').pop()
    with open("../data/" + "forsyth-PDF" + "/" + title,"wb") as pdf:
        for chunk in r.iter_content(chunk_size=1024):
         if chunk:
             pdf.write(chunk)
             
             
f.close()
print("finished")
