from splinter import Browser
from bs4 import BeautifulSoup
import time

def init_browser():
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)
    return browser

def scrape():
    browser = init_browser()

    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    time.sleep(2)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    quotes = soup.select(".content_title")
    news_title = quotes[0].text

    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    time.sleep(2)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    quotes = soup.select(".article_teaser_body")
    news_p = quotes[0].text

    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    time.sleep(2)
    browser.click_link_by_partial_text('FULL IMAGE')
    time.sleep(2)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    quotes = soup.find_all('img', class_='fancybox-image')
    featured_image_url = 'https://www.jpl.nasa.gov' + quotes[0]["src"]

    url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url)
    time.sleep(2)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    quotes = soup.find_all('p', class_='TweetTextSize') 
    result = [s.extract() for s in quotes[0]]
    [x.strip() for x in result]
    mars_weather = " ".join([x.strip() for x in result])

    import pandas as pd
    url = 'https://space-facts.com/mars/'
    tables = pd.read_html(url)
    time.sleep(2)
    df = tables[0]
    df = df[["Mars - Earth Comparison", "Mars"]]
    df.set_index("Mars - Earth Comparison", inplace=True)
    html_table = df.to_html()
    html_table = html_table.replace('\n', '')

    hemisphere_image_urls = [
        {"title": "Valles Marineris Hemisphere", "img_url":\
          "https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/valles_marineris_enhanced.tif/full.jpg"},
        {"title": "Cerberus Hemisphere", "img_url":\
          "https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/cerberus_enhanced.tif/full.jpg"},
        {"title": "Schiaparelli Hemisphere", "img_url":\
          "http://astropedia.astrogeology.usgs.gov/download/Mars/Viking/schiaparelli_enhanced.tif/full.jpg"},
        {"title": "Syrtis Major Hemisphere", "img_url":\
          "https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/syrtis_major_enhanced.tif/full.jpg"},
    ]    

    import pymongo
    conn = 'mongodb://localhost:27017'
    client = pymongo.MongoClient(conn)
    db = client.U12_db
    collection = db.scraping1
    post = {
             "news_title":news_title,
             "news_p":news_p,
             "featured_image_url":featured_image_url,
             "mars_weather":mars_weather,
             "html_table":html_table,
             "hemisphere_image_urls":hemisphere_image_urls
            }
    collection.drop()
    collection.insert_one(post)
