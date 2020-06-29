import requests 
from bs4 import BeautifulSoup 
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time
import os

f = open("../data/kitsap.txt", "w")
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
driver = webdriver.Chrome(ChromeDriverManager().install(), options = chrome_options)


def scraping(url):
    print("Scraping from " + url)
    f.write("Scraping from " + url + "\n\n\n")
    driver.get(url)
    time.sleep(1)
    result = driver.execute_script("return document.documentElement.outerHTML")
    return BeautifulSoup(result, 'html.parser')
    
def findHref(data):
    for i in range(len(data)):
        for link in data[i].find_all('a'):
            current = link.get('href')
            links.append(current)

def treatLinks(link):
    try:
        if link.startswith("https://content.govdelivery.com/accounts/WAKITSAP/bulletins/"):
            processPage(link)
        else:
            try:
                r = requests.get(link)
                if r.headers['Content-type'] == "application/pdf":
                    f.write("Scraping from " + link + "\n\n\n")
                    f.write("A PDF here.\n")
                    title = link.split('/').pop()
                    with open("../data/" + "kitsap-PDF" + "/" + title,"wb") as pdf:
                        for chunk in r.iter_content(chunk_size=1024):
                            if chunk:
                                pdf.write(chunk)

            except:
                pass
    except:
        pass
        
        
# create directory
path = "../data/kitsap-image"
os.mkdir(path)
path = "../data/kitsap-PDF"
os.mkdir(path)



# Scraping from https://kitsappublichealth.org/CommunityHealth/CoronaVirus.php
url = "https://kitsappublichealth.org/CommunityHealth/CoronaVirus.php"
f.write("Scraping from " + url + "\n\n\n")
soup = scraping(url)
data = soup.find_all("div", id = "accordion-3")

for i in range(len(data)):
    f.write(data[i].text)
    f.write("\n\n\n")
    
# Collect links under safe start
data = soup.find_all("div", id = "collapseFifteen-3")
links = []
for i in range(len(data)):
    for link in data[i].find_all('a'):
        current = link.get('href')
        if current.startswith("./"):
            links.append(current.replace("./","https://kitsappublichealth.org/CommunityHealth/"))
        else:
            links.append(current)
for link in links:
    treatLinks(link)




# Scraping from https://www.kitsapgov.com/Pages/coronavirus.aspx
url = "https://www.kitsapgov.com/Pages/coronavirus.aspx"
f.write("Scraping from " + url + "\n\n\n")
r = requests.get(url)
soup = BeautifulSoup(r.content, 'html.parser')
data = soup.find_all("div", "main-content wrap")
# collect links
links = []
findHref(data)

# write text
for i in range(len(data)):
    f.write(data[i].text)
    f.write("\n\n\n")






def processPage(link):
    f.write("Scraping from " + link + "\n\n\n")
    r = requests.get(link)
    soup = BeautifulSoup(r.content, 'html.parser')
    for content in soup.select("#main-body"):
        f.write(content.text)
        f.write("\n\n\n")

    data = soup.find_all("img")
    # get all picture link
    picturelinks = []
    for picturelink in data:
        current = picturelink.get("src")
        if current not in removePic: picturelinks.append(current)
    getPictures(picturelinks)



def getPictures(links):
    for image_url in links:
        filename = image_url.split("/")[-1]
        r = requests.get(image_url, stream = True)
        with open("../data/" + "kitsap-image" + "/" + filename,"wb") as f:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)

removePic = ["https://content.govdelivery.com/attachments/fancy_images/WAKITSAP/2020/03/3238644/coronavirus-gov-deliveryv2_original.jpg", "/system/images/14588/original/WAKITSAP_banner.gif?1306875323", "https://content.govdelivery.com/attachments/fancy_images/WAKITSAP/2020/03/3238644/coronavirus-gov-deliveryv2_original.jpg",
"https://www.kitsapgov.com/PublishingImages/KC%20Logo%20Color%20(filled%20white).png", "https://content.govdelivery.com/assets/logos/govd-logo-dark-191d8c132e92636d2d67f33aa6576c8f1f8245552c047acb81d0e5c7094def56.png",
"https://content.govdelivery.com/assets/logos/govd-envelope-dark-20px-f7cb83de41ee11fe68a33125cd9e51d9c13a20f59dbe25f05f9c3b44e4f8d65d.png"]

# scrap content in links
# scrap https://content.govdelivery.com/accounts/WAKITSAP/bulletins/ and PDFs
for link in links:
    treatLinks(link)



f.close()
driver.quit()
print("finished")
