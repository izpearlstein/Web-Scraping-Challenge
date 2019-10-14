import pandas as pd
import requests
from splinter import Browser
from bs4 import BeautifulSoup

def init_browser():
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    return Browser('chrome', **executable_path, headless=False)

### Single dictionary to store all info for MongoDB
mars = {}

def scrape_news():
    browser = init_browser()

    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    news_title = soup.find('div', class_='content_title').find('a').text
    news_p = soup.find('div', class_='article_teaser_body').text

    mars['news_title'] = news_title
    mars['news_p'] = news_p

    return mars


# #### Mars Space Images

def scrape_featured_image():
    browser = init_browser()

    images_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(images_url)

    images_html = browser.html
    soup = BeautifulSoup(images_html, 'html.parser')

    image = soup.find('a', class_="button fancybox")
    image_url = image['data-fancybox-href']

    main_url = 'https://www.jpl.nasa.gov'
    featured_image_url = main_url + image_url

    mars['featured_image'] = featured_image_url

    return mars


# #### Mars Weather

def scrape_weather():
    browser = init_browser()

    weather_url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(weather_url)

    weather_html = browser.html
    soup = BeautifulSoup(weather_html, 'html.parser')

    weather_tweet = soup.find('div', class_='js-tweet-text-container').text

    mars['weather'] = weather_tweet

    return mars


# #### Mars Facts

def scrape_facts():

    browser = init_browser()

    mars_facts_url = 'https://space-facts.com/mars/'
    mars_table = pd.read_html(mars_facts_url)
    mars_df = mars_table[0]
    mars_df = mars_df[['Mars - Earth Comparison','Mars']]
    mars_df = mars_df.rename(columns = {'Mars - Earth Comparison': 'Parameter'})
    mars_df.set_index('Parameter', inplace=True)
    mars_facts_html = mars_df.to_html()

    mars['facts'] = mars_facts_html

    return mars


# #### Mars Hemispheres

def scrape_hemispheres():

    browser = init_browser()

    hemispheres_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemispheres_url)

    hemispheres_html = browser.html
    soup = BeautifulSoup(hemispheres_html, 'html.parser')

    items = soup.find_all('div', class_='item')

    hemispheres_image_urls = []

    hemispheres_main_url = 'https://astrogeology.usgs.gov'

    for i in items: 
        
        title = i.find('h3').text
        partial_img_url = i.find('a', class_='itemLink product-item')['href']
        browser.visit(hemispheres_main_url + partial_img_url)
        partial_img_html = browser.html
        soup = BeautifulSoup(partial_img_html, 'html.parser')
        img_url = hemispheres_main_url + soup.find('img', class_='wide-image')['src']
        hemispheres_image_urls.append({"title" : title, "img_url" : img_url})

    mars['hemispheres'] = hemispheres_image_urls

    return mars