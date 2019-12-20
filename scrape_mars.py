import pandas as pd
import pymongo
import os
from bs4 import BeautifulSoup as bs
from splinter import Browser
import requests
import time
from selenium import webdriver
#from webdriver_manager.chrome import ChromeDriverManager

#driver = webdriver.Chrome(ChromeDriverManager().install())

#driver = webdriver.Chrome('/Users/wheeler/.wdm/drivers/chromedriver/79.0.3945.36/mac64/chromedriver') 
#driver = webdriver.Chrome('/usr/local/bin/chromedriver')
#NASA Mars News
#Scrape the NASA Mars News Site and collect the latest News Title and Paragraph Text. 
#Assign the text to variables that you can reference later.


def init_browser():
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    return Browser("chrome", **executable_path, headless=False)



def scrape_info():
    browser=init_browser()
    #mars_data={}


    news_url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    browser.visit(news_url)
    html = browser.html
    soup =bs(html, "html.parser")



    # Define the variables for later use
    # article = soup.find("div", class_='list_text')
    news_t = soup.find("div", class_="content_title")
    news_p = soup.find("div", class_ ="article_teaser_body")



    #JPL Mars Space Images - Featured Image

    #Visit the url for JPL Featured Space Image.
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)
    image_url='https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'



    #Use splinter to navigate the site and find the image url for the current Featured Mars Image
    #and assign the url string to a variable called featured_image_url.
    browser.visit(image_url)
    browser.click_link_by_partial_text('FULL IMAGE')



    # Setting time so we can go to the next page and find the image in full size
    browser.is_element_present_by_text("more info", wait_time=1)
    more_info_element = browser.find_link_by_partial_text("more info")
    more_info_element.click()



    #getting the url for the image
    html = browser.html
    img_soup = bs(html, "html.parser")

    image = img_soup.find("img", class_="main_image")['src']



    #complete the url for the image
    featured_image_url=f'https://www.jpl.nasa.gov'+image
    featured_image_url



    #Mars Weather

    #Visit the Mars Weather twitter account and scrape the latest Mars weather tweet from the page. 
    #Save the tweet text for the weather report as a variable called mars_weather.

    tw_url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(tw_url)
    html=browser.html
    twitter_soup=bs(html,'html.parser')



    mars_tweet = twitter_soup.find('div', class_="js-tweet-text-container")
    mars_weather = mars_tweet.p.text
    mars_weather




    #Mars Facts
    #Visit the Mars Facts webpage here and use Pandas to scrape the table containing facts about 
    #the planet including Diameter, Mass, etc.

    #mars_df = pd.read_html("https://space-facts.com/mars/")[0]
    #mars_df.columns=["Description", "Value"]
    #mars_df.set_index("Description", inplace=True)
    #mars_df

    facts_url = "https://space-facts.com/mars/"

    mars_data = pd.read_html(facts_url)
    time.sleep(2)

    mars_data = mars_data[0]
    print(mars_data)
   # mars_data.columns = ["Description", "Value"]
    #mars_data = mars_data.set_index("Description", inplace = True)
    mars_facts = mars_data.to_html(index = True, header =True)
    return mars_facts



    #Use Pandas to convert the data to a HTML table string.
    #df_html=mars_df.to_html()

    #Mars Hemispheres

    #Visit the USGS Astrogeology site to obtain high resolution images for each of Mar's hemispheres.

    hemisphere_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemisphere_url)
    html=browser.html
    #hemi_soup=bs(html,'html.parser')



    #Getting the base url
    hemisphere_base_url = 'https://astrogeology.usgs.gov'
    print(hemisphere_base_url)


        
    hemisphere =[]
    hemisphere_list=['Cerberus','Schiaparelli','Syrtis','Valles']
    for hemi in hemisphere_list:
        hemispheres={}
        url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
        browser.visit(url)
        html = browser.html
        soup = bs(html,'html.parser')
        browser.click_link_by_partial_text(hemi)
        html = browser.html
        soup = bs(html,'html.parser')
        hemispheres['image']=soup.find('a',target="_blank")['href']
        hemispheres['title']=soup.find('h2',class_="title").text
        hemisphere.append(hemispheres)

   


    mars_hemisphere_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

    hemisphere_results = []

    for i in range(1,9,2):
        hemisphere_dict = {}
        
        browser.visit(mars_hemisphere_url)
        time.sleep(1)
        hemispheres_html = browser.html
        hemispheres_soup = bs(hemispheres_html, 'html.parser')
        hemispherenamelinks = hemispheres_soup.find_all('a', class_='product-item')
        hemispherename = hemispherenamelinks[i].text.strip('Enhanced')
        
        linkdetail = browser.find_by_css('a.product-item')
        linkdetail[i].click()
        time.sleep(1)
        browser.find_link_by_text('Sample').first.click()
        time.sleep(1)
        browser.windows.current = browser.windows[-1]
        hemisphereimgage_html = browser.html
        browser.windows.current = browser.windows[0]
        browser.windows[-1].close()
        
        hemisphereimgage_soup = bs(hemisphereimgage_html, 'html.parser')
        hemisphereimage_path = hemisphereimgage_soup.find('img')['src']

        print(hemispherename)
        hemisphere_dict['title'] = hemispherename.strip()
        
        print(hemisphereimage_path)
        hemisphere_dict['img_url'] = hemisphereimage_path

        hemisphere_results.append(hemisphere_dict)

  
    # Store data in a dictionary
    mars_data = {
        #"news_title": news_t[0],
        #"news_p": news_p[0],
        "featured_image": featured_image_url,
        "mars_weather": mars_weather,
        "mars_facts": mars_data,
        "hemisphereimage_urls": hemisphere_results

    }
    print(mars_data)
    return mars_data