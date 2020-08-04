#!/usr/bin/env python
# coding: utf-8

# In[1]:


from bs4 import BeautifulSoup
import urllib.request
import re


# In[2]:


url="http://www.co.cumberland.nc.us/COVID19closures"
page = urllib.request.urlopen(url) 
soup = BeautifulSoup(page, 'html.parser')
print(soup)


# In[3]:


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
    


# In[4]:


# Scraping PDFS

import os
import requests
from urllib.parse import urljoin

county="cumberland"
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


# In[11]:


#words=["COVID-19", "COVID", "Coronavirus", "cases", "Cases", "testing", "Testing"]
with open(r"../data/cumberland.txt",'w', encoding='utf-8') as outfile:
    outfile.write("Scraping from " + url + "\n" +"\n")
    for i in content:
        print(i.get_text(separator = '\n'), file=outfile)  
    url="http://www.co.cumberland.nc.us/departments/public-information-group/public-information-office/new-releases"
    page = urllib.request.urlopen(url) 
    soup = BeautifulSoup(page, 'html.parser')
    for a in soup.select('.ml-2 a'):
        #for i in words:
            #if i in a.text:
        print("href", a.get('href'))
        if a.get('href'):
            url="http://www.co.cumberland.nc.us"+str(a.get('href'))
            print(url)
            page = urllib.request.urlopen(url)
            soup = BeautifulSoup(page, 'html.parser')
            newcontent= soup.find_all('p')
            outfile.write("Scraping from " + url + "\n" +"\n")
            for cont in newcontent:
                print(cont.get_text(separator = '\n'), file=outfile)


# In[ ]:




