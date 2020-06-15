from bs4 import BeautifulSoup
import requests

#Scrape Denver County testing information from 'https://www.denvergov.org/content/denvergov/en/covid-19/recovery-guidance/testing.html'
COUNTY = "denver"
f = open("../data/denver.txt", "w")
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
main_title = soup.select("h1 strong").get_text()
sub_title = soup.select("h2 strong").get_text()
f.write(main_title + "\n" + sub_title + "\n")
divs = soup.find_all("div", class_="text section")
for div in divs[1:]: 
    scrapeTextSections(div)

f.close()

    






