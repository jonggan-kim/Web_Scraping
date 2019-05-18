#!/usr/bin/env python
# coding: utf-8

# # Web Scraping for Mars Mission.¶
import requests
from bs4 import BeautifulSoup
from splinter import Browser
import os
import pandas as pd
import time
import datetime
from pprint import pprint


def init_browser():
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    return Browser('chrome', **executable_path, headless=False)
#Create empty dictionary to store all the mars information.
mars_info = {}      
# # Part 1. ### Mars News¶
def scrape_mars_news():
   try:
      browser = init_browser()
      url = 'https://mars.nasa.gov/news/'
      browser.visit(url)
      time.sleep(3)
      html = browser.html
      news_soup = BeautifulSoup(html, 'html.parser')
      browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)
      slide_elem = news_soup.select_one('ul.item_list li.slide')
      news_title = slide_elem.find("div", class_='content_title').get_text()
      news_para = slide_elem.find("div", class_='article_teaser_body').get_text()
      # Append results from part 1 into the final mars_info dictionary.
      mars_info["Mars_News_Title"] = news_title
      mars_info["Mars_News_Body"] = news_para
      return mars_info
   finally:
      browser.quit()

   # # Part 2. ### JPL Mars Images¶ 
def scrape_mars_image():

   try: 
      browser = init_browser()
      url2 = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
      browser.visit(url2)
      full_image_elem = browser.find_by_id('full_image')
      full_image_elem.click()
      time.sleep(3)
      more_info_elem = browser.find_link_by_partial_text('more info')
      more_info_elem.click()
      time.sleep(3)
      html2 = browser.html
      image_soup = BeautifulSoup(html2, 'html.parser')
      lede1=image_soup.select_one('figure.lede a img')
      image_url=lede1.get("src")
      full_image_url = "https://www.jpl.nasa.gov" + image_url
      #Append full image url to the Mars dictionary.
      mars_info["Mars_Full_Image"] = full_image_url
      return mars_info
   finally:
      browser.quit()


   # # Part 3 . ### Mars Weather tweet¶
def scrape_mars_weather():
   try: 
      browser = init_browser()
      url3 = 'https://twitter.com/marswxreport?lang=en'
      browser.visit(url3)
      time.sleep(3)
      html3 = browser.html
      mars_weather = BeautifulSoup(html3, 'html.parser')
      mars_weather.find_all('p', class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text") 
      tweet_mars_weather = mars_weather.body.find_all('p')[5].text
      #Add weather tweet to the mars_info dict.
      mars_info["Mars_Weather_Tweet"] = tweet_mars_weather
      return mars_info
   finally:
      browser.quit()

   # # Part 4. ### Mars Facts¶
def scrape_mars_facts():
   try:
      browser = init_browser()
      url4 = "https://space-facts.com/mars/"
      tables = pd.read_html(url4)
      tables
      df = tables[0]
      df.columns = ["0", "1"]
      df.columns = ["Mars Profile", "Fact Data"]
      df.head(10)
      # Pandas also had a to_html method that we can use to generate HTML tables from DataFrames.
      html_table = df.to_html()
      html_table
      # You may have to strip unwanted newlines to clean up the table.
      html_table = html_table.replace('\n', '')
      # You can also save the table directly to a file.
      df.to_html('table.html')
      mars_info["Mars_Facts_Table"] = html_table
      return mars_info
   finally:
      browser.quit()

   # # Part 5. ### Mars Hemispheres¶
def scrape_mars_hemispheres():
   try:   
      browser = init_browser()
      mars_hemis = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
      browser.visit(mars_hemis)
      html=browser.html
      soup = BeautifulSoup(html,"html.parser")
      #Retreive all items that contain mars hemispheres information
      items = soup.find_all('div', class_='item')
      # Create empty list for hemisphere urls 
      hemisphere_image_urls = []
      # Store the main_ul 
      hemispheres_main_url = 'https://astrogeology.usgs.gov'
      for i in items:
        # Store title
         title = i.find('h3').text
         # Store link that leads to full image website
         partial_img_url = i.find('a', class_='itemLink product-item')['href']
         # Visit the link that contains the full image website 
         browser.visit(hemispheres_main_url + partial_img_url)
         # HTML Object of individual hemisphere information website 
         partial_img_html = browser.html 
         # Parse HTML with Beautiful Soup for every individual hemisphere information website 
         soup = BeautifulSoup( partial_img_html, 'html.parser')
         # Retrieve full image source 
         img_url = hemispheres_main_url + soup.find('img', class_='wide-image')['src']
         # Append the retreived information into a list of dictionaries 
         hemisphere_image_urls.append({"title" : title, "img_url" : img_url})
      # Display hemisphere_image_urls
      hemisphere_image_urls
      mars_info["Hemisphere_Image"] = hemisphere_image_urls
      return mars_info
   finally:
      browser.quit()

def scrape_mars_datetime():
   try:   
      browser = init_browser()
      #Generate date time and store in the dictionary.
      now_datetime = datetime.datetime.utcnow()
      mars_info["Date"] = now_datetime
      return mars_info
   finally:
      browser.quit()