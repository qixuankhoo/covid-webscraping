# RUN APPLICATION
import requests
from bs4 import BeautifulSoup
import urllib3
import re
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time
import os
from google_drive_downloader import GoogleDriveDownloader as gdd
import sys

def scraping(url):
    print("\n\n\nScraping from " + url + "\n\n\n")
    f.write("\n\n\nScraping from " + url + "\n\n\n")
    r = requests.get(url)
    return BeautifulSoup(r.content, 'html.parser')

def advanced_scraping(url):
    print("\n\n\nScraping from " + url + "\n\n\n")
    f.write("\n\n\nScraping from " + url + "\n\n\n")
    driver.get(url)
    time.sleep(1)
    result = driver.execute_script("return document.documentElement.outerHTML")
    return BeautifulSoup(result, 'html.parser')

def gdownload(url, destination):
    print(url)
    splits = url.split("/")
    d_location = -1
    google_id = ""

    for i, split in enumerate(splits):
        if split == 'd':
            d_location = i
        elif 'id=' in split:
            google_id = split[split.find('id=')+3:]
    if d_location != -1 and google_id == "":
        google_id = splits[d_location + 1]
    gdd.download_file_from_google_drive(file_id=google_id,
                                    dest_path=destination)

def getPDFs(file_url, county):
    print("pdf url", file_url)
    print("A PDF HERE\n")
    f.write("A PDF HERE\n")
    title = file_url.split('/').pop()
    if len(title) > 255:
        title = title[:250] + '.pdf'
    r = requests.get(file_url, stream = True)
    with open("../data/" + county + "-PDF" + "/" + title,"wb") as pdf:
        for chunk in r.iter_content(chunk_size=1024*1024):
            pdf.write(chunk)
    return "data/" + title

def saveBphc(url):
    soup = scraping(url)
    contents = soup.find_all('div', class_='ms-rtestate-field')
    for content in contents:
        f.write(content.get_text(separator = '\n'))
        for a_tag in content.find_all('a'):
            link = a_tag.get('href')
            if link and '.pdf' in link and ('English' in a_tag.text or 'health emergency' in a_tag.text):
                if 'http' in link:
                    getPDFs(link, 'boston')
                else:
                    getPDFs('https://bphc.org' + link, 'boston')

def saveText(url):
    soup = scraping(url)
    main = soup.find('section', class_='main-content')
    if main:
        f.write(main.text)
    else:
        f.write('\nNo relevant text found\n')

COUNTY = "boston"
f = open("../data/" + COUNTY + ".txt", "w")


pdfPath = "../data/" + COUNTY + "-PDF"
os.mkdir(pdfPath)

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument("--enable-javascript")
chrome_options.add_argument("--start-maximized")
directory = os.getcwd()[:-7] + "data/" + COUNTY + "-PDF"
prefs = {"download.default_directory": 
                        directory} 
chrome_options.add_experimental_option("prefs", prefs)
driver = webdriver.Chrome(ChromeDriverManager().install(), options = chrome_options)

# scrape from 'https://www.boston.gov/departments/public-health-commission/coronavirus-guidance'
soup = scraping('https://www.boston.gov/departments/public-health-commission/coronavirus-guidance')
date = soup.select_one('.brc-lu')
f.write(date.text + "\n\n\n")
contents = soup.find_all('div', class_='content')
for content in contents:
    title = content.find('div', class_='sh')
    if title and 'CDC' not in title.text:
        if "guidance" in title.text:
            for a_tag in content.find_all('a'):
                link = a_tag.get('href')
                if 'boston.gov' in link:
                    saveText(a_tag.get('href'))
                elif '.pdf' in link:
                    getPDFs(link, 'boston')
        else:
            f.write(content.get_text(separator = '\n'))

# scrape from 'https://www.boston.gov/news/coronavirus-disease-covid-19-boston'
soup = scraping('https://www.boston.gov/news/coronavirus-disease-covid-19-boston')
date = soup.select_one('time')
f.write("Date: " + date.text + "\n\n\n")
contents = soup.find_all('div', class_='content')
for content in contents:
    title = content.find('div', class_='sh')
    if title:
        f.write(content.text)

# scrape from 'https://www.boston.gov/departments/public-health-commission/when-you-should-be-tested-covid-19'
saveText('https://www.boston.gov/departments/public-health-commission/when-you-should-be-tested-covid-19')

# scrape from 'https://www.boston.gov/departments/public-health-commission/coronavirus-timeline'
saveText('https://www.boston.gov/departments/public-health-commission/coronavirus-timeline')

# scrape from 'https://www.boston.gov/news/covid-19-resource-guide-bostons-immigrants'
saveText('https://www.boston.gov/news/covid-19-resource-guide-bostons-immigrants')

# scrape from 'https://www.boston.gov/health-and-human-services/covid-19-reopening-city-boston'
soup = scraping('https://www.boston.gov/health-and-human-services/covid-19-reopening-city-boston')
page_contents = soup.select('#content :nth-child(1)')
for page_content in page_contents:
    f.write(page_content.text)


done = False

# scrape from 'https://www.bostonpublicschools.org/Page/8080'
soup = scraping('https://www.bostonpublicschools.org/Page/8080')
page_contents = soup.select('#sw-content-container1 h1 , .ui-article')
for page_content in page_contents:
    for a_tag in page_content.find_all('a'):
        link = a_tag.get('href')
        if '.pdf' in link:
            if "Remote learning Update" in link:
                if not done:
                    getPDFs(link, 'boston')
                    done = True
            else:
                getPDFs('https://www.bostonpublicschools.org/' + link, 'boston')
    f.write(page_content.text)

# scrape from 'https://www.bostonpublicschools.org/' 
# this is definitely the best source for policy info

soup = scraping('https://bphc.org/whatwedo/infectious-diseases/Infectious-Diseases-A-to-Z/covid-19/Pages/default.aspx')
pages = soup.select('.ms-navedit-linkNode')
for page in pages:
        link = page.get('href')
        saveBphc('https://bphc.org' + link)

driver.quit() 