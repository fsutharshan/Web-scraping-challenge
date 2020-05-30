#Import dependencies
from splinter import Browser
from bs4 import BeautifulSoup as bs
import re
import time
import os
import pandas as pd
import requests

#Initializing the Browser Method
def init_browser():
    executable_path = {"executable_path":"/Users/frsutharshan/chromedriver"}
    return Browser("chrome", **executable_path, headless = False)

# Method to scrape all the data related to Mars
def scrape():
    browser = init_browser()
    mars_facts_data = {}

    url = "https://mars.nasa.gov/news"
    browser.visit(url)
    time.sleep(10)   # Wait enough time until the page fully loads
    

    html = browser.html
    news_soup = bs(html,"html.parser")

    browser.is_element_present_by_css('div.content_title',wait_time=1)

    #scrapping latest news about mars from nasa
    news_title = news_soup.find_all("div",class_="content_title")[0::1][1].text
    news_paragraph = news_soup.find("div", class_="article_teaser_body").text
    mars_facts_data['news_title'] = news_title
    mars_facts_data['news_paragraph'] = news_paragraph 
    
    #Mars Featured Image
    url_image = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url_image)
    time.sleep(10)  # Wait enough time until the page fully loads

    from urllib.parse import urlsplit
    base_url = "{0.scheme}://{0.netloc}".format(urlsplit(url_image))
    xpath = "//*[@id=\"page\"]/section[3]/div/ul/li[1]/a/div/div[2]/img"

    browser.is_element_present_by_xpath(xpath, wait_time=1)
    results = browser.find_by_xpath(xpath)
    img = results
    img.click()
    time.sleep(10) # Wait enough time until the page fully loads

    html_image = browser.html
    soup = bs(html_image, "html.parser")
    img_url = soup.find("img", class_="fancybox-image")["src"]
    full_img_url = base_url + img_url
    mars_facts_data["featured_image"] = full_img_url

    #Mars Weather

    url_weather = "https://twitter.com/marswxreport?lang=en"
    browser.visit(url_weather)
    time.sleep(10) # Wait enough time until the page fully loads
    html_weather = browser.html
    soup = bs(html_weather, "html.parser")

    mars_weather = soup.find("div", class_="css-901oao r-hkyrab r-1qd0xha r-a023e6 r-16dba41 r-ad9z0x r-bcqeeo r-bnwqim r-qvutc0").text
    mars_facts_data["mars_weather"] = mars_weather
    

    #Mars Facts

    url_facts = "https://space-facts.com/mars/"
    table = pd.read_html(url_facts)
     
    df_mars_facts = table[0]
    df_mars_facts.columns = ["Parameter", "Values"]
    df_mars_facts.set_index(["Parameter"]) 

    mars_html_table = df_mars_facts.to_html()
    mars_html_table = mars_html_table.replace("\n", "")
    
    mars_facts_data["mars_facts_table"] = mars_html_table

    usgs_url="https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(usgs_url) 
    time.sleep(10) # Wait enough time until the page fully loads

    soup = bs(browser.html, "html.parser")
    hemi_attributes_list = soup.find_all('a', class_="itemLink product-item")

    #Remove duplicate links from the list 
    hemi_no_dup_list = []
    hemi_no_dup_list.append(hemi_attributes_list[1])
    hemi_no_dup_list.append(hemi_attributes_list[3])
    hemi_no_dup_list.append(hemi_attributes_list[5])
    hemi_no_dup_list.append(hemi_attributes_list[7])

    # The four hemisphere image URLs 
    hemisphere_image_urls = []
    for hemi_img in hemi_no_dup_list:
        img_title = hemi_img.find('h3').text
       
        link_to_img = "https://astrogeology.usgs.gov/" + hemi_img['href']
        
        browser.visit(link_to_img)
        soup = bs(browser.html, 'html.parser')
        img_tag = soup.find('div', class_='downloads')
        img_url = img_tag.find('a')['href']
        hemisphere_image_urls.append({"Title": img_title, "Image_Url": img_url})
    
    mars_facts_data["hemisphere_img_url"] = hemisphere_image_urls

    browser.quit()  # Cleanup - Close the Chrome instance that was opened for scraping
   
    return mars_facts_data
