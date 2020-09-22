# Dependencies
import lxml.html as lh
import pandas as pd
from bs4 import BeautifulSoup as bs
import requests
from splinter import Browser
import time

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)

def scrape_info():

    #Create a dictionary to load in mongo
    marsmission = {}

    #Put the feature image link in our mars data dictionary using the feature function
    feature_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    marsmission['feature'] = feature()

    #Run the funciion to get the list of key vaues for the hemisphere name and image url
    marsmission['hemispheres'] = hemispheres()

    #Run the funciion to get the Mars Facts Table
    marsmission['factsTable'] = facts()

    #Initialize browser for the news page
    browser = init_browser()
    
    #Retrieve the top news headline and snipit
    news_url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    response = requests.get(news_url)

    # Create a Beautiful Soup object
    soup = bs(response.text, 'html.parser')
    
    # Put the news title in our mars data dictionary
    news_title = soup.find('div', class_="content_title").text
    marsmission['headline'] = news_title

    # Put the news snipit in our mars data dictionary
    news_snipit = soup.find('div', class_="rollover_description_inner").text
    marsmission['snipit'] = news_snipit

    # Close the browser after scraping
    browser.quit()

    # Return results
    return marsmission

def feature():
    #Initialize browser for the feature image page
    browser = init_browser()
    feature_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(feature_url)

    #Click the full image button to get to the image URL
    browser.links.find_by_partial_text('FULL').click()
    time.sleep(3)
    # Create a Beautiful Soup object
    soup = bs(browser.html, 'html.parser')

    #Get the URL of the full image
    relative_image_url = soup.find_all('img', class_='fancybox-image')[0]['src']

    #Create the full URL
    featured_image_url = 'https://www.jpl.nasa.gov' + relative_image_url

    # Close the browser after scraping
    browser.quit()

    return featured_image_url

def hemispheres():
     
    browser = init_browser()
    # URL of page to be scraped
    images_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"

    names = []
    urls = []

    #Cycle through hemisphere image list and collect the names and image links
    for item in range(4):
        browser.visit(images_url)

        #Wait for the page to load
        time.sleep(5)
        browser.links.find_by_partial_text('Hemisphere')[item].click()

        # Create a Beautiful Soup object
        soup = bs(browser.html, 'html.parser')
    
        #Get the name of the hemisphere
        title = soup.find('h2', class_='title')
        name = title.text.strip()
        names.append(name)
    
        #Get the URL of the full size hemisphere image
        url = 'https://astrogeology.usgs.gov'+ soup.find('img', class_='wide-image')['src']
        urls.append(url)

    #Making the name and URL dictionary using list comprehension
    hemispheres = [ {'title': names[item], 'image_url': urls[item] } for item in range(len(urls)) ]

    # Close the browser after scraping
    browser.quit()

    return hemispheres

def facts():

    browser = init_browser()

    # URL of page to be scraped
    facts_url = "https://space-facts.com/mars/"

    # Retrieve page with the requests module
    response = requests.get(facts_url)

    # Create a Beautiful Soup object
    soup = bs(response.text, 'html.parser')

    #Thanks to https://www.pluralsight.com/guides/extracting-data-html-beautifulsoup for some table extraction tips
    facts_table = soup.find("table", attrs={"class": "tablepress"})
    facts_table_data = facts_table.tbody.find_all("tr")

    all_facts_data = []

    #Put the all the fact data in a list
    for item in range(9): #tabel row range is easily made static based on the small size
        for td in facts_table_data[item].find_all("td"):
            #Remove all the markup from the text
            all_facts_data.append(td.text.strip())

    #Split the list with help from stackoverflow.com
    #Make a list of the fact items in the even indicies
    fact_item = all_facts_data[::2] 

    #Make a list of the fact data in the odd indicies
    fact_data = all_facts_data[1::2]

    facts_table_df = pd.DataFrame({'Description':fact_item,'Data':fact_data}).set_index('Description', drop=True)
    # Use Pandas to convert the data to a HTML table string.
    factsTable = pd.DataFrame.to_html(facts_table_df)

    browser.quit()

    return factsTable