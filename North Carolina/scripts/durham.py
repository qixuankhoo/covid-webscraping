import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time
import os

f = open("../data/durham.txt", "w")

def findHref(data):
    for i in range(len(data)):
        for link in data[i].find_all('a'):
            current = link.get('href')
            if current.startswith("http"):
                links.append(current)
            else:
                links.append("https://durhamnc.gov" + current)
            
# Create directory for PDFs
path = "../data/durham-PDF"
os.mkdir(path)
path = "../data/durham-image"
os.mkdir(path)
    
# Scraping from "https://durhamnc.gov/4013/City-of-Durham-COVID-19-Updates-Resource" txt
url = "https://durhamnc.gov/4013/City-of-Durham-COVID-19-Updates-Resource"
r = requests.get(url)
soup = BeautifulSoup(r.content, 'html.parser')
data = soup.select("#contentWrapTS")
f.write("Scraping from " + url + "\n\n\n")
for i in range(len(data)):
    f.write(data[i].get_text(separator='\n'))
f.write("\n\n\n")


# Scraping from "https://durhamnc.gov/4019/Stay-at-Home-Order-FAQs" txt and pdfs
url = "https://durhamnc.gov/4019/Stay-at-Home-Order-FAQs"
r = requests.get(url)
soup = BeautifulSoup(r.content, 'html.parser')
data = soup.select("#contentWrapTS")
links = []
findHref(data)
f.write("Scraping from " + url + "\n\n\n")
for i in range(len(data)):
    f.write(data[i].get_text(separator='\n'))
f.write("\n\n\n")

for link in links:
    r = requests.get(link, verify = False)
    if r.headers['Content-type'] == "application/pdf":
        f.write("Scraping from " + link + "\n\n\n")
        f.write("A PDF here.\n")
        title = ""
        try:
            title = r.headers['Content-DocumentTitle']
        except:
            title = link.split('/').pop()
        with open("../data/" + "durham-PDF" + "/" + title + ".pdf","wb") as pdf:
            for chunk in r.iter_content(chunk_size=1024):
             if chunk:
                 pdf.write(chunk)



# Scraping from "https://durhamnc.gov/4066/Community-Business-Resources" txt
url = "https://durhamnc.gov/4066/Community-Business-Resources"
r = requests.get(url)
soup = BeautifulSoup(r.content, 'html.parser')
data = soup.select("#contentWrapTS")
f.write("Scraping from " + url + "\n\n\n")
for i in range(len(data)):
    f.write(data[i].get_text(separator='\n'))
f.write("\n\n\n")


# Scraping from "https://durhamnc.gov/4014/COVID-19-Coronavirus-Updates-for-City-Em" txt
url = "https://durhamnc.gov/4014/COVID-19-Coronavirus-Updates-for-City-Em"
r = requests.get(url)
soup = BeautifulSoup(r.content, 'html.parser')
data = soup.select("#contentWrapTS")
f.write("Scraping from " + url + "\n\n\n")
for i in range(len(data)):
    f.write(data[i].get_text(separator='\n'))
f.write("\n\n\n")

# Scraping from a list  txt
links = ["https://www.dcopublichealth.org/services/communicable-diseases/communicable-diseases/coronavirus-disease-2020",
"https://www.dcopublichealth.org/services/communicable-diseases/coronavirus-disease-2019/covid-19-faqs",
"https://www.dcopublichealth.org/services/communicable-diseases/coronavirus-disease-2019/covid-19-testing",
"https://www.dcopublichealth.org/services/communicable-diseases/coronavirus-disease-2019/covid-19-modified-hours-of-operation",
"https://www.dcopublichealth.org/services/communicable-diseases/coronavirus-disease-2019/covid-19-email-lists",
"https://www.dcopublichealth.org/services/communicable-diseases/coronavirus-disease-2019/covid-19-resources-volunteering"]
for url in links:
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
    data = soup.select("#ColumnUserControl3")
    f.write("Scraping from " + url + "\n\n\n")
    for i in range(len(data)):
        f.write(data[i].get_text(separator='\n'))
    f.write("\n\n\n")




# Scraping from https://www.dcopublichealth.org/services/communicable-diseases/coronavirus-disease-2019/durham-county-covid-19-graphics
url = "https://www.dcopublichealth.org/services/communicable-diseases/coronavirus-disease-2019/durham-county-covid-19-graphics"
r = requests.get(url)
soup = BeautifulSoup(r.content, 'html.parser')
data = soup.select("#ColumnUserControl3")
links = []
for i in range(len(data)):
    for a_tag in data[i].find_all("a"):
        if a_tag.text == "English" or a_tag.text == "English & Spanish" or a_tag.text == "English and Spanish":
            links.append(a_tag.get("href"))


for link in links:
    r = requests.get(link, verify = False)
    if r.headers['Content-type'] == "application/pdf":
        f.write("Scraping from " + link + "\n\n\n")
        f.write("A PDF here.\n")
        title = ""
        try:
            title = r.headers['Content-DocumentTitle']
        except:
            title = link.split('/').pop()
        with open("../data/" + "durham-PDF" + "/" + title + ".pdf","wb") as pdf:
            for chunk in r.iter_content(chunk_size=1024):
             if chunk:
                 pdf.write(chunk)
    elif r.headers['Content-type'] == "image/png":
        f.write("Scraping from " + link + "\n\n\n")
        f.write("A PDF here.\n")
        title = ""
        try:
            title = r.headers['Content-DocumentTitle']
        except:
            title = link.split('/').pop()
        with open("../data/" + "durham-image" + "/" + title + ".png","wb") as pdf:
            for chunk in r.iter_content(chunk_size=1024):
             if chunk:
                 pdf.write(chunk)



f.close()
print("finished")
