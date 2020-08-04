#!/usr/bin/env python
# coding: utf-8

# In[114]:


import urllib.request
from urllib.request import Request, urlopen
import re
from bs4 import BeautifulSoup as soup
url = 'https://www.douglas.co.us/douglascovid19/'
req = Request(url , headers={'User-Agent': 'Mozilla/5.0'})

webpage = urlopen(req).read()
page_soup = soup(webpage, "html.parser")
title = page_soup.find("title")
print(title)


# In[115]:


linksinfo=[]

content = page_soup.findAll("p")
links= page_soup.findAll("a")
for cont in content:
    print(cont.get_text())
    
for i in links:
    linksinfo.append(i.get_text() + ": " + str(i.get('href')))
    print(i.get_text())
    print(i.get('href'))
    
with open(r"../data/douglas.txt",'w') as outfile:
    outfile.write("Scraping from " + url + "\n" + "\n")
    for i in content:
        print(i.get_text(separator = '\n'), file=outfile)


# In[116]:


import urllib.request
import urllib.parse
import requests
from requests import get 
import os
from bs4 import BeautifulSoup

county="douglas"

url           = 'https://www.douglas.co.us/douglascovid19/'
download_path = "../data/" + county + "-PDF"
os.mkdir(download_path)
headers       = {'User-Agent':'Mozilla/5.0'}
request       = urllib.request.Request(url, None, headers)
html          = urllib.request.urlopen(request)
soup          = BeautifulSoup(html.read(),"html.parser") 

for tag in soup.findAll('a', href=True):
    if os.path.splitext(os.path.basename(tag['href']))[1] == '.pdf':
        print(tag['href'])
        a = os.path.join(download_path,tag['href'].split('/')[-1])
        f = open(a, "wb")
        response = requests.get(tag['href'], headers=headers)
        f.write(response.content)
        f.close() 


# In[ ]:





# In[ ]:




