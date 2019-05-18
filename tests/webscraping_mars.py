#!/usr/bin/env python
# coding: utf-8

# Web Scraping for Mars Mission.¶

import requests
from bs4 import BeautifulSoup
from splinter import Browser
import pandas as pd
import time
import datetime
from pprint import pprint

mars_info = {}

def init_browser():
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    return Browser('chrome', **executable_path, headless=False)

def mars_scrape():
	#Create empty dictionary to store all the mars information.

	# executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
	# return Browser('chrome', **executable_path, headless=False)


	# # Part 1. ### Mars News¶

	url = 'https://mars.nasa.gov/news/'
	browser.visit(url)
	time.sleep(3)
	html = browser.html
	news_soup = BeautifulSoup(html, 'html.parser')
	browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)
	slide_elem = news_soup.select_one('ul.item_list li.slide')
	print(slide_elem)
	news_title = slide_elem.find("div", class_='content_title').get_text()
	print(news_title)
	news_para = slide_elem.find("div", class_='article_teaser_body').get_text()
	print(news_para)

	# Append results from part 1 into the final mars_info dictionary.
	mars_info["Mars_News_Title"] = news_title
	mars_info["Mars_News_Body"] = news_para
	return mars_info

	# # Part 2. ### JPL Mars Images¶ 
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
	print(image_url)

	full_image_url = "https://www.jpl.nasa.gov" + image_url
	print(full_image_url)

	#Append full image url to the Mars dictionary.
	mars_info["Mars_Full_Image"] = full_image_url
	return mars_info

	# # Part 3 . ### Mars Weather tweet¶
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

	# # Part 4. ### Mars Facts¶
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
	html_table
	mars_info["Mars_Facts_Table"] = html_table

	# You can also save the table directly to a file.
	df.to_html('table.html')
	return mars_info

	# # Part 5. ### Mars Hemispheres¶
	 # Visit hemispheres website through splinter module 
	hemispheres_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
	browser.visit(hemispheres_url)

	# HTML Object
	html_hemispheres = browser.html
	soup = BeautifulSoup(html_hemispheres, 'html.parser')

	# Retreive all items that contain mars hemispheres information
	items = soup.find_all('div', class_='item')

	# Create empty list for hemisphere urls 
	hemisphere = []

	hemispheres_main_url = 'https://astrogeology.usgs.gov' 

	    # Loop through the items previously stored
	for i in items: 
	   
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
	    hemisphere.append({"title" : title, "img_url" : img_url})

	mars_info['Hemisphere'] = hemisphere

    
    # Return mars_data dictionary 

	return mars_info




	# url5 =  "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars/"
	# browser.visit(url5)
	# time.sleep(10)
	# html5 = browser.html
	# soup5 = BeautifulSoup(html5, "html.parser")
	# #parse soup object for images of the 4 hemispheres .
	# class_collap_results = soup5.find('div', class_="collapsible results")
	# hemis_items = class_collap_results.find_all('div',class_='item')
	# #hemis_items
	# #loop thru to find tile and the image urls to append to relevant lists. 
	# hemis_img_urls_list=list()
	# img_urls_list = list()
	# title_list = list()
	# for h in hemis_items:
	# 	#save title
	# 	h_title = h.h3.text
	# 	title_list.append(h_title)
	# 	# find the href link.
	# 	h_href  = "https://astrogeology.usgs.gov" + h.find('a',class_='itemLink product-item')['href']
	# 	#print(h_title,h_href)
	# 	#browse the link from each page
	# 	browser.visit(h_href)
	# 	time.sleep(5)
	# 	#Retrieve the  image links and store in a list. 
	# 	html5   = browser.html
	# 	soup_img = BeautifulSoup(html5, 'html.parser')
	# 	h_img_url = soup_img.find('div', class_='downloads').find('li').a['href']
	# 	#print("h_img_url" + h_img_url)
	# 	img_urls_list.append(h_img_url)
	# 	# create a dictionary with  each image and title and append to a list. 
	# 	hemispheres_dict = dict()
	# 	hemispheres_dict['title'] = h_title
	# 	hemispheres_dict['img_url'] = h_img_url
	# 	hemis_img_urls_list.append(hemispheres_dict)
	# #print(len(hemis_img_urls_list))
	# #Add hemispheres list  to the mars_info dictionary.
	# mars_info["Hemisphere_Image_URLs"] = hemis_img_urls_list
	# return mars_info



# 	url5= "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
# 	browser.visit(url5)
# 	hemisphere_list = []
# 	links = browser.find_by_css("a.product-item h3")

# 	for i in range(len(links)):
# 		hemisphere = ()
# 		# We have to find the elements on each loop to avoid a stale element exception
# 		browser.find_by_css("a.product-item h3")[i].click()

# 		# Next, we find the Sample image anchor tag and extract the href
# 		sample_elem = browser.find_link_by_text('Sample').first
# 		hemisphere['img_url'] = sample_elem['href']

# 		# Get Hemisphere title
# 		hemisphere['title'] = browser.find_by_css("h2.title").text

# 		# Append hemisphere object to list
# 		# hemisphere.append(hemisphere)
# 		# print(hemisphere)
# 		hemisphere_list.append({"title" : title, "img_url" : img_url})
# 		mars_info['Hemisphere_Image_URLs'] = hemisphere_list

# 		# Finally, we navigate backwards
# 		browser.back()


#     #Add hemispheres list  to the mars_info dictionary.
# #	mars_info["Hemisphere_Image_URLs"] = hemisphere_list

# 	return mars_info

    #Generate date time and store in the dictionary.
    # hemisphere_image_urls = []
    # for i in range(4):

    #     # Find the elements on each loop to avoid a stale element exception
    #     browser.find_by_css("a.product-item h3")[i].click()

    #     hemi_data = scrape_hemisphere(browser.html)

    #     # Append hemisphere object to list
    #     hemisphere_image_urls.append(hemi_data)

    #     # Finally, we navigate backwards
    #     browser.back()
    #     print(hemisphere_image_urls)
    # mars_info[]=hemisphere_image_urls


	now_datetime = datetime.datetime.utcnow()
	mars_info["Date_Time"] = now_datetime

	return mars_info

    #Return final dictionary with all the mars information that was scraped in the 5 steps above. 
	print("just before final return of mars_info")
	mars_return =  {
	    "News_Title":mars_info["Mars_News_Title"],
	    "News_Summary":mars_info["Mars_News_Body"],
	    "Full_Image":mars_info["Mars_Full_Image"],
	    "Weather_Tweet":mars_info["Mars_Weather_Tweet"],
	    "Mars_Facts":html_table,
	    "Hemisphere":hemisphere,
	    "Date":mars_info["Date_Time"],
	}
	return mars_return
# def scrape_hemisphere(html_text):

#     # Soupify the html text
#     hemi_soup = BeautifulSoup(html_text, "html.parser")

#     # Try to get href and text except if error.
#     try:
#         title_elem = hemi_soup.find("h2", class_="title").get_text()
#         sample_elem = hemi_soup.find("a", text="Sample").get("href")

#     except AttributeError:

#         # Image error returns None for better front-end handling
#         title_elem = None
#         sample_elem = None

#     hemisphere = {
#         "title": title_elem,
#         "img_url": sample_elem
#     }

#     return hemisphere

# from splinter import Browser
# from bs4 import BeautifulSoup


# def init_browser():
#     # @NOTE: Replace the path with your actual path to the chromedriver
#     executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
#     return Browser("chrome", **executable_path, headless=False)


# def scrape():
#     browser = init_browser()
#     listings = {}

#     url = "https://raleigh.craigslist.org/search/hhh?max_price=1500&availabilityMode=0"
#     browser.visit(url)

#     html = browser.html
#     soup = BeautifulSoup(html, "html.parser")

#     listings["headline"] = soup.find("a", class_="result-title").get_text()
#     listings["price"] = soup.find("span", class_="result-price").get_text()
#     listings["hood"] = soup.find("span", class_="result-hood").get_text()

#     return listings
 



