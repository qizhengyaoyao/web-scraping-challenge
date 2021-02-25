# Dependencies
from bs4 import BeautifulSoup
from splinter import Browser, browser
import requests
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager

def init_browser():
    #path of webdriver
    executable_path = {'executable_path': ChromeDriverManager().install()}
    return Browser('chrome', **executable_path, headless=False)

def scrape():
    # News url for scraping
    browser = init_browser()
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    html=browser.html
    soup=BeautifulSoup(html,'html.parser')
    
    # Retrieve the latest news title
    news_title = soup.find_all('div', class_='content_title')[1].text
    #print(f"Latest news title: {news_title}")

    # Retrive the latest new paragraph
    news_p=soup.find('div', class_='article_teaser_body').text
    #print(f"Latest news: {news_p}")

    # Image url for scraping
    base_url="https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/"
    idx_url="index.html"
    browser.visit(base_url+idx_url)
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    # Retrieve the url of featured image
    img_url=soup.find_all('img', class_='headerimage')[0]['src']
    featured_image_url=base_url+img_url
    #featured_image_url

    # Mars facts table url for scraping
    facts_url="https://space-facts.com/mars/"
    browser.visit(facts_url)
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    # Retrieve the mars fact table
    tb=pd.read_html('https://space-facts.com/mars/')
    facts_tb=tb[0]
    facts_tb.rename(columns={0:'Description',1:'Mars'},inplace=True)
    facts_tb.set_index('Description',inplace=True)
    #facts_tb

    # Convert pandas table to html
    facts_tb_html=facts_tb.to_html()
    facts_tb_html=facts_tb_html.replace('\n','')
    #print(facts_tb_html)

    # Mars hemispheres url for scraping
    base_url="https://astrogeology.usgs.gov"
    search_url="/search/results?q=hemisphere+enhanced&k1=target&v1=Mars/"
    browser.visit(base_url+search_url)
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    # Retrieve the urls of all hemispheres image link
    search_list=[]
    hemi_url=soup.find_all('div', class_='description')
    search_list=[base_url+hemi.find('a')['href'] for hemi in hemi_url]
    #search_list

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
        img_url=soup.find_all('li')[0].a['href']
        #print(img_url)
        hemi_img_dct["title"]=title
        hemi_img_dct["img_url"]=img_url
        hemisphere_image_urls.append(hemi_img_dct)
    #print(hemisphere_image_urls)

    # Return a dictionary value
    Mars_dict={
        "news_title":news_title,
        "news_p":news_p,
        "featured_image_url":featured_image_url,
        "facts_tb_html":facts_tb_html,
        "hemisphere_image_urls":hemisphere_image_urls
    }

    browser.quit()
    return Mars_dict





