from bs4 import BeautifulSoup
import requests
import os 

def getFilePath(path):
    fileDir = os.path.dirname(__file__)
    filePath = os.path.join(fileDir,path)
    return filePath

def writeData(soup, tag, class_name):
    currdata = soup.find_all(tag, class_= class_name)
    for i in range(len(currdata)):
        f.write(currdata[i].get_text())

def findHref(data):
    for i in range(len(data)):
        for link in data[i].find_all('a', class_='btn-info'):
            links.append(link.get('href'))


#create PDF folder for PDF files
COUNTY = 'denver'

try:
    filePath = getFilePath("../data/" + COUNTY + "-PDF")
    os.mkdir(filePath) 
except:
    print('PDF folder already exists!')
    
textFilePath = '../data/' + COUNTY + '.txt'
f = open(getFilePath(textFilePath), 'w')
links = []

#Scrape Denver County 
url = 'https://www.denvergov.org/content/denvergov/en/covid-19/recovery-guidance.html'
webpage = requests.get(url)
soup = BeautifulSoup(webpage.content, 'html.parser')
links = []
data = soup.find_all("div", class_="rawtext section")
findHref(data)

for link in links:
    webpage = requests.get("https://www.denvergov.org/"+link)
    soup = BeautifulSoup(webpage.content, 'html.parser')
    title = soup.find('h1').get_text()
    sections = soup.find_all('div', class_='text section')
    f.write(title + "\n\n")
    for div in sections:
        f.write(div.get_text().encode('utf-8'))
        f.write('\n\n')

f.close()