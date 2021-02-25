#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Dependencies
from bs4 import BeautifulSoup
from splinter import Browser
import requests
import pandas as pd


# In[2]:


#path of webdriver
executable_path = {'executable_path': '../chromedriver'}
browser = Browser('chrome', **executable_path, headless=False)


# ### NASA Mars News

# In[3]:


# News url for scraping
url = 'https://mars.nasa.gov/news/'
browser.visit(url)
html=browser.html
soup=BeautifulSoup(html,'html.parser')


# In[4]:


# Retrieve the latest news title
news_title=soup.find_all('div', class_='content_title')[1].text
print(f"Latest news title: {news_title}")


# In[5]:


# Retrive the latest new paragraph
news_p=soup.find_all('div', class_='article_teaser_body')[0].text
print(f"Latest news: {news_p}")


# ### JPL Mars Space Images - Featured Image

# In[6]:


# Image url for scraping
jpl_url="https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html"
browser.visit(jpl_url)
html = browser.html
soup = BeautifulSoup(html, "html.parser")


# In[7]:


# Retrieve the url of featured image
img_url=soup.find_all('img', class_='headerimage')[0]['src']
featured_image_url=jpl_url+img_url
featured_image_url


# ### Mars Facts

# In[8]:


# Mars facts table url for scraping
facts_url="https://space-facts.com/mars/"
browser.visit(facts_url)
html = browser.html
soup = BeautifulSoup(html, "html.parser")


# In[9]:


# Retrieve the mars fact table
tb=pd.read_html('https://space-facts.com/mars/')
facts_tb=tb[0]
facts_tb.rename(columns={0:'Description',1:'Mars'},inplace=True)
facts_tb.set_index('Description',inplace=True)
facts_tb


# In[10]:


# Convert pandas table to html
facts_tb_html=facts_tb.to_html()
facts_tb_html.replace('\n','')
print(facts_tb_html)


# ### Mars Hemispheres

# In[11]:


# Mars hemispheres url for scraping
base_url="https://astrogeology.usgs.gov"
search_url="/search/results?q=hemisphere+enhanced&k1=target&v1=Mars/"
browser.visit(base_url+search_url)
html = browser.html
soup = BeautifulSoup(html, "html.parser")


# In[12]:


# Retrieve the urls of all hemispheres image link
search_list=[]
hemi_url=soup.find_all('div', class_='description')
search_list=[base_url+hemi.find('a')['href'] for hemi in hemi_url]
search_list


# In[13]:


# Retrieve the urls of all full resolution image for the hemispheres image link list
hemisphere_image_urls=[]
for s_url in search_list:
    print(f"Extracting info from {s_url}")
    browser.visit(s_url)
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    hemi_img_dct={}
    title=soup.find('h2',class_='title').text
    #print(title)
    img_url=soup.find_all('li')[1].a['href']
    #print(img_url)
    hemi_img_dct["title"]=title
    hemi_img_dct["img_url"]=img_url
    hemisphere_image_urls.append(hemi_img_dct)

print(hemisphere_image_urls)


# In[14]:


# Return a dictionary value
Mars_dict={
    "news_title":news_title,
    "news_p":news_p,
    "featured_image_url":featured_image_url,
    "facts_tb_html":facts_tb_html,
    "hemisphere_image_urls":hemisphere_image_urls
}


# In[15]:


Mars_dict


# In[ ]:




