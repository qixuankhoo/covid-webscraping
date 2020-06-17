#!/usr/bin/env python
# coding: utf-8

# In[2]:


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


# In[7]:


linksinfo=[]

content = page_soup.findAll("p")
links= page_soup.findAll("a")
for cont in content:
    print(cont.get_text())
    
for i in links:
    linksinfo.append(i.get_text() + ": " + str(i.get('href')))
    print(i.get_text())
    print(i.get('href'))
    
print(linksinfo)

with open('douglasdata.txt','w') as outfile:
    outfile.write("CONTENT" + "\n" + "\n")
    for i in content:
        print(i.get_text(), file=outfile)
    outfile.write("\n" + "\n"+ "LINKS" + "\n" + "\n")
   
    for item in linksinfo:
        print(item, file=outfile)


# In[ ]:




