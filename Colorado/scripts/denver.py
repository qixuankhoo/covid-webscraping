from bs4 import BeautifulSoup
import requests
import os 

#Scrape Denver County testing information from 'https://www.denvergov.org/content/denvergov/en/covid-19/recovery-guidance/testing.html'
COUNTY = "denver"
fileDir = os.path.dirname(__file__)
filePath = os.path.join(fileDir, "../data/denver.txt")
filePath = os.path.abspath(os.path.realpath(filePath))
f = open(filePath, 'w')
url = 'https://www.denvergov.org/content/denvergov/en/covid-19/recovery-guidance/testing.html'
def scraping(url):
    f.write("Scraping from " + url + "\n\n\n")

def scrapeTextSections(div):
    heading = div.select("h3 strong").get_text()
    f.write(heading+"\n")
    body = div.select("p")
    for paragraph in body:
        f.write(paragraph.get_text())
    f.write("\n")

webpage = requests.get('https://www.denvergov.org/content/denvergov/en/covid-19/recovery-guidance/testing.html')
soup = BeautifulSoup(webpage.content, 'html.parser')
scraping(url) 
sections = soup.find_all("div", class_="text section")
for div in sections: 
    f.write(div.get_text().encode('utf-8'))
    f.write("\n\n\n")

f.close()

    






