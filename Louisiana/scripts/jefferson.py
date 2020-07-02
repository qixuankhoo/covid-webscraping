#!/usr/bin/env python
# coding: utf-8

# In[9]:


from bs4 import BeautifulSoup
import urllib.request
import re


# In[10]:


url="https://www.visitjeffersonparish.com/about-us/jefferson-parish-coronavirus-preparedness/"
page = urllib.request.urlopen(url) 
soup = BeautifulSoup(page, 'html.parser')
print(soup)


# In[11]:


linksinfo=[]

links= soup.find_all('a')
content= soup.find_all('p')
for i in content:
    print((i.get_text()))
 
    
links= soup.find_all('a')
for i in links:
    if 'www' in str(i.get('href')):
        linksinfo.append(str(i.get('href')))
    print(i.get_text())
    print(i.get('href'))
    
linksinfo

with open(r"C:\Users\Raghav's Computer\Covid Muser\data\jefferson.txt",'w') as outfile:
    outfile.write("CONTENT" + "\n" + "\n")
    for i in content:
        print(i.get_text(), file=outfile)
    outfile.write("\n" + "\n"+ "LINKS" + "\n" + "\n")
   
    for item in linksinfo:
        print(item, file=outfile)


# In[12]:


# Scraping PDFS

import os
import requests
from urllib.parse import urljoin

pdfs=[]
for i in soup.select("a[href$='.pdf']"):
    pdfs.append(i)
if len(pdfs)>0: #Only creates folder if the website has pdfs
    folder_location = r"C:\Users\Raghav's Computer\Covid Muser\data\jefferson-PDF"
    if not os.path.exists(folder_location):os.mkdir(folder_location)
    response = requests.get(url)
    soup= BeautifulSoup(response.text, "html.parser")     
    for link in soup.select("a[href$='.pdf']"):
        filename = os.path.join(folder_location,link['href'].split('/')[-1])
        with open(filename, 'wb') as f:
            try:
                f.write(requests.get(urljoin(url,link['href'])).content)
            except Exception:
                continue


# In[ ]:




