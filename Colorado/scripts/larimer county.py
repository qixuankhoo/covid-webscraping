#!/usr/bin/env python
# coding: utf-8

# In[2]:


from bs4 import BeautifulSoup
import urllib.request
import re


# In[3]:


url="https://www.larimer.org/health/communicable-disease/coronavirus-covid-19/think-or-know-you-have-covid-19/covid-19-testing"
page = urllib.request.urlopen(url) 
soup = BeautifulSoup(page, 'html.parser')
print(soup)


# In[23]:


linksinfo=[]

links= soup.find_all('a')
content= soup.find_all('p')
for i in content:
    print((i.get_text()))
 
    
links= soup.find_all('a')
for i in links:
    linksinfo.append(i.get_text() + ": " + str(i.get('href')))
    print(i.get_text())
    print(i.get('href'))
    
linksinfo

with open('larimerdata.txt','w') as outfile:
    outfile.write("CONTENT" + "\n" + "\n")
    for i in content:
        print(i.get_text(), file=outfile)
    outfile.write("\n" + "\n"+ "LINKS" + "\n" + "\n")
   
    for item in linksinfo:
        print(item, file=outfile)


# In[ ]:




