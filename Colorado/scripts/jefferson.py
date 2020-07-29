from bs4 import BeautifulSoup
import requests
import os 
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

def getFilePath(path):
    fileDir = os.path.dirname(__file__)
    filePath = os.path.join(fileDir,path)
    return filePath

def scraping(url):
    print("Scraping from " + url)
    f.write("Scraping from " + url + "\n\n")
    driver.get(url)
    result = driver.execute_script("return document.documentElement.outerHTML")
    return BeautifulSoup(result, 'html.parser')

def getPDF(file_url, county):
    title = file_url.split('/').pop()
    fileName = title + '.pdf'
    filePath = getFilePath("../data/" + county + "-PDF")
    r = requests.get(file_url, stream = True)
    with open(os.path.join(filePath,fileName), "wb") as pdf:
        for chunk in r.iter_content(chunk_size=1024):
         if chunk:
             pdf.write(chunk)
    return "data/" + title


COUNTY = "jefferson"

try:
    filePath = getFilePath("../data/" + COUNTY + "-PDF")
    os.mkdir(filePath) 
except:
    print('PDF folder already exists!')
    
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
driver = webdriver.Chrome(ChromeDriverManager().install(), options = chrome_options) 

textFilePath = '../data/' + COUNTY + '.txt'
f = open(getFilePath(textFilePath), 'w')
links = [
    'https://www.jeffco.us/4057/CARES-Act-Emergency-Grants-Funding',
    'https://www.jeffco.us/4039/Community-Conversations',
    'https://www.jeffco.us/4019/Jeffco-Community-Resources',
    'https://www.jeffco.us/4043/Mental-Health',
    'https://www.jeffco.us/4075/Testing'
]

for link in links:
    try:
        soup = scraping(link)
        section = soup.select('#moduleContent')[0]
        page = section.select('#page')[0]
        f.write(page.get_text())
    except:
        print('Error scraping website')
 

#Scrape stay-at-home order page
url = 'https://www.jeffco.us/4047/Safer-at-Home-Order'
soup = scraping(url)
section = soup.select('#moduleContent')[0]
page = section.select('#page')[0]
lst = page.find_all('div', class_="fr-view")[-1]
data = lst.find('ul')

f.write(page.get_text())

for item in data:
    link = item.find('a').get('href')
    try:
        try: 
            if 'Document' in link: 
                pdf = getPDF(link, COUNTY)
        except:
            if 'Document' in link: 
                pdf = getPDF("https://www.jeffco.us" + link, COUNTY)
    except:
        print('not a PDF!')
 

#Scrape public health info websites --done
url = 'https://www.jeffco.us/4018/Info-for-Public-Health-Partners-Business'
soup = scraping(url)
section = soup.select('#moduleContent')[0]
page = section.select('#page')[0]
lst = page.find_all('ul')[8]
data = lst.find_all('li')

f.write(page.get_text())

for item in data:
    if 'En' not in item.get_text():
        link = item.find('a').get('href')
        try:
            try: 
                if 'Document' in link: 
                    pdf = getPDF(link, COUNTY)
            except:
                if 'Document' in link: 
                    pdf = getPDF("https://www.jeffco.us" + link, COUNTY)
        except:
            print('not a PDF!')



#Scrape closure information website --done
url = 'https://www.jeffco.us/4008/COVID-19-Closure-Information'
soup = scraping(url)
section = soup.select('#moduleContent')[0]
page = section.select('#page')[0]
data = page.find_all('a')

for item in data:
    link = item.get('href')
    try:
        try: 
            if 'Document' in link: 
                pdf = getPDF(link, COUNTY)
        except:
            if 'Document' in link: 
                pdf = getPDF("https://www.jeffco.us" + link, COUNTY)
    except:
        print('not a PDF!')

f.write(page.get_text())

f.close()