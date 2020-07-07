#!/usr/bin/env python
# coding: utf-8

# In[3]:


from bs4 import BeautifulSoup
import urllib.request
import re


# In[4]:


url="http://www.worcesterma.gov/coronavirus"
page = urllib.request.urlopen(url) 
soup = BeautifulSoup(page, 'html.parser')
print(soup)


# In[5]:


linksinfo=[]

links= soup.find_all('a')
content= soup.find_all('p')
for i in content:
    print((i.get_text(separator = '\n')))
 
    
links= soup.find_all('a')
for i in links:
    if 'www' in str(i.get('href')):
        linksinfo.append(str(i.get('href')))
    print(i.get_text(separator = '\n'))
    print(i.get('href'))
    
linksinfo
    


# In[6]:


# Scraping PDFS

import os
import requests
from urllib.parse import urljoin

county="worcester"
pdfs=[]
for i in soup.select("a[href$='.pdf']"):
    pdfs.append(i)
if len(pdfs)>0: 
    #Only creates folder if the website has pdfs
    path = "../data/" + county + "-PDF"
    os.mkdir(path)
    response = requests.get(url)
    soup= BeautifulSoup(response.text, "html.parser")     
    for link in soup.select("a[href$='.pdf']"):
        filename = os.path.join(path,link['href'].split('/')[-1])
        with open(filename, 'wb') as f:
            try:
                f.write(requests.get(urljoin(url,link['href'])).content)
            except Exception:
                continue


# In[7]:


with open(r"../data/worcester.txt",'w', encoding='utf-8') as outfile:
    outfile.write("Scraping from " + url + "\n" + "\n")
    for i in content:
        print(i.get_text(separator = '\n'), file=outfile)
#     outfile.write("\n" + "\n"+ "LINKS" + "\n" + "\n")
   
#     for item in linksinfo:
#         print(item, file=outfile)
        
     
    


# In[ ]:




