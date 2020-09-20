# Dependencies
import pandas as pd
import lxml.html as lh
from bs4 import BeautifulSoup as bs
import requests
from splinter import Browser
import time

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)

def scrape_info():
    browser = init_browser()

    #Create a dictionary to load in mongo
    mars_data = {}

    #Put the feature image link in our mars data dictionary using the feature function
    feature_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    mars_data['feature_image'] = feature(feature_url)

    #Retrieve the top news headline and snipit
    news_url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    response = requests.get(news_url)

    # Create a Beautiful Soup object
    soup = bs(response.text, 'html.parser')
    
    # Put the news title in our mars data dictionary
    news_title = soup.find('div', class_="content_title").text
    mars_data['headline'] = news_title

    # Put the news snipit in our mars data dictionary
    news_snipit = soup.find('div', class_="rollover_description_inner").text
    mars_data['snipit'] = news_snipit

    # Close the browser after scraping
    browser.quit()

    # Return results
    return mars_data

def feature(feature_url):

    browser.visit(feature_url)

    #Click the full image button to get to the image URL
    browser.links.find_by_partial_text('FULL').click()

    # Create a Beautiful Soup object
    soup = bs(browser.html, 'html.parser')

    featured_image_url = "https://www.jpl.nasa.gov" + soup.find_all('img', class_='fancybox-image')[0]["src"]

    return featured_image_url