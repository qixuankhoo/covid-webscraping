from bs4 import BeautifulSoup
import requests
import os 
from selenium import webdriver
#from webdriver_manager.chrome import ChromeDriverManager
import time

fileDir = os.path.dirname(__file__)
filePath = os.path.join(fileDir, "../data/denver.txt")
filePath = os.path.abspath(os.path.realpath(filePath))
f = open(filePath, "w")
COUNTY = "denver"

def scraping(url):
    print("Scraping from " + url)
    f.write("\n\n\n")
    f.write("Scraping from " + url + "\n\n\n")

    #driver.get(url)
    #time.sleep(1)
    #result = driver.execute_script("return document.documentElement.outerHTML")
    result = requests.get(url)
    return BeautifulSoup(result.content, 'html.parser')

def writeData(soup, tag, class_name):
    currdata = soup.find_all(tag, class_= class_name)
    for i in range(len(currdata)):
        f.write(currdata[i].get_text())

def findHref(data):
    for i in range(len(data)):
        for link in data[i].find_all('a', class_='btn-info'):
            links.append(link.get('href'))


#Scrape Denver County 

url = 'https://www.denvergov.org/content/denvergov/en/covid-19/recovery-guidance.html'
soup = scraping(url)
links = []
data = soup.find_all("div", class_="rawtext section")
findHref(data)
print(len(links))
for link in links:
    currSoup = scraping(url+link)
    writeData(currSoup, 'h1', '')
    writeData(currSoup, 'div', 'text section')
    f.write("\n\n\n")

f.close()
print("finished")

#Create folder for PDF files
'''
path = "../data/" + COUNTY + "-PDF"
os.mkdir(path)
'''

#Scrape Denver County testing information from 'https://www.denvergov.org/content/denvergov/en/covid-19/recovery-guidance/testing.html'
"""
COUNTY = "denver"
fileDir = os.path.dirname(__file__)
filePath = os.path.join(fileDir, "../data/Denver County/denver_testing_info.txt")
filePath = os.path.abspath(os.path.realpath(filePath))
f = open(filePath, 'w')
url = 'https://www.denvergov.org/content/denvergov/en/covid-19/recovery-guidance/testing.html'

webpage = requests.get('https://www.denvergov.org/content/denvergov/en/covid-19/recovery-guidance/testing.html')
soup = BeautifulSoup(webpage.content, 'html.parser')
scraping(url) 
sections = soup.find_all("div", class_="text section")
for div in sections: 
    f.write(div.get_text())
    f.write("\n\n\n")

f.close()

"""

#Scrape Denver County guidance for business information from 'https://www.denvergov.org/content/denvergov/en/covid-19/recovery-guidance/testing.html'
""" 
COUNTY = "denver"
fileDir = os.path.dirname(__file__)
filePath = os.path.join(fileDir, "../data/Denver County/denver_business_info.txt")
filePath = os.path.abspath(os.path.realpath(filePath))
f = open(filePath, 'w')

webpage = requests.get('https://www.denvergov.org/content/denvergov/en/covid-19/recovery-guidance/guidance-for-businesses.html')
soup = BeautifulSoup(webpage.content, 'html.parser')

title = soup.find('h1').find('strong').get_text()
sections = soup.find_all('div', class_='text section')
scraping('https://www.denvergov.org/content/denvergov/en/covid-19/recovery-guidance/guidance-for-businesses.html')
f.write(title + "\n\n")
for div in sections:
    f.write(div.get_text())
    f.write('\n\n')

f.close()

 """

#Scrape Denver County guidance for business information from 'https://www.denvergov.org/content/denvergov/en/covid-19/recovery-guidance/testing.html'
""" 
COUNTY = "denver"
fileDir = os.path.dirname(__file__)
filePath = os.path.join(fileDir, "../data/Denver County/denver_recovery_info.txt")
filePath = os.path.abspath(os.path.realpath(filePath))
f = open(filePath, 'w')

webpage = requests.get('https://www.denvergov.org/content/denvergov/en/covid-19/recovery-guidance/face-covering.html')
soup = BeautifulSoup(webpage.content, 'html.parser')

title = soup.find('h1').find('strong').get_text()
sections = soup.find_all('div', class_='text section')
scraping('https://www.denvergov.org/content/denvergov/en/covid-19/recovery-guidance/face-covering.html')
f.write(title + "\n\n")
for div in sections:
    f.write(div.get_text())
    f.write('\n\n')

f.close()
"""

#Scrape Denver County guidance for residents information from 'https://www.denvergov.org/content/denvergov/en/covid-19/recovery-guidance/guidance-for-residents.html'
""" 
COUNTY = "denver"
fileDir = os.path.dirname(__file__)
filePath = os.path.join(fileDir, "../data/Denver County/denver_guidance_for_residence.txt")
filePath = os.path.abspath(os.path.realpath(filePath))
f = open(filePath, 'w')
url = 'https://www.denvergov.org/content/denvergov/en/covid-19/recovery-guidance/guidance-for-residents.html'

webpage = requests.get(url)
soup = BeautifulSoup(webpage.content, 'html.parser')

title = soup.find('h1').find('strong').get_text()
sections = soup.find_all('div', class_='text section')
scraping(url)
f.write(title + "\n\n")
for div in sections:
    f.write(div.get_text())
    f.write('\n\n')

f.close()
"""




