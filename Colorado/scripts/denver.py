from bs4 import BeautifulSoup
import requests
import os 


def scraping(url):
    f.write("Scraping from " + url + "\n\n\n")

""" 
#Scrape Denver County testing information from 'https://www.denvergov.org/content/denvergov/en/covid-19/recovery-guidance/testing.html'
COUNTY = "denver"
fileDir = os.path.dirname(__file__)
filePath = os.path.join(fileDir, "../data/denver_testing_info.txt")
filePath = os.path.abspath(os.path.realpath(filePath))
f = open(filePath, 'w')
url = 'https://www.denvergov.org/content/denvergov/en/covid-19/recovery-guidance/testing.html'

webpage = requests.get('https://www.denvergov.org/content/denvergov/en/covid-19/recovery-guidance/testing.html')
soup = BeautifulSoup(webpage.content, 'html.parser')
scraping(url) 
sections = soup.find_all("div", class_="text section")
for div in sections: 
    f.write(div.get_text().encode('utf-8'))
    f.write("\n\n\n")

f.close()

"""
#Scrape Denver County guidance for business information from 'https://www.denvergov.org/content/denvergov/en/covid-19/recovery-guidance/testing.html'
COUNTY = "denver"
fileDir = os.path.dirname(__file__)
filePath = os.path.join(fileDir, "../data/denver_business_info.txt")
filePath = os.path.abspath(os.path.realpath(filePath))
f = open(filePath, 'w')

webpage = requests.get('https://www.denvergov.org/content/denvergov/en/covid-19/recovery-guidance/guidance-for-businesses.html')
soup = BeautifulSoup(webpage.content, 'html.parser')

title = soup.find('h1').find('strong').get_text().encode('utf-8')
sections = soup.find_all('div', class_='text section')
scraping('https://www.denvergov.org/content/denvergov/en/covid-19/recovery-guidance/guidance-for-businesses.html')
f.write(title + "\n\n")
for div in sections:
    f.write(div.get_text().encode('utf-8'))
    f.write('\n\n')

f.close()







