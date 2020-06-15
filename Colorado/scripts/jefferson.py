from bs4 import BeautifulSoup
import requests
import os 


def scraping(url):
    f.write("Scraping from " + url + "\n\n\n")

COUNTY = "jefferson"
fileDir = os.path.dirname(__file__)
filePath = os.path.join(fileDir, "../data/Jefferson County 2020-6-14/jefferson_covid19.txt")
filePath = os.path.abspath(os.path.realpath(filePath))
f = open(filePath, 'w')
url = 'https://www.jeffco.us/3999/Coronavirus-Disease-2019-COVID-19'

webpage = requests.get(url)
soup = BeautifulSoup(webpage.content, 'html.parser')

title = soup.find('h1', class_='headline').get_text().encode('utf-8')
scraping(url)
f.write(title + '\n\n')
sections = soup.find_all('div', class_='fr-view')
for div in sections:
    f.write(div.get_text().encode('utf-8'))
    f.write('\n')
f.close()