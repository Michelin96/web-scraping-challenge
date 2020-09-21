# web-scraping-challenge
Scraping sites with Mars information and creating a single web page of the data.

# System Setup
The webscraping funcionality utilizes Chrome Driver. If using a Mac, all that is needed is to install Chrome Driver with no further changes to the code. 
To use on a PC you will also need to change the following code block in scrape_mars.py to reflect the install location of your Chrome Driver.

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)
    
* Scraped data is stored in a Mongo Database. You will need to have MongoDB inslalled, and the database running. Additionaly scraping tools include Beautiful Soup and Splinter.

* Initial webscraping was tested in a Jupyter Notebook file. 

## Scraping and Display

* Run app.py in a Python environment that has the additional depdendendancies installed
* Sample screen shots of the rendered web page are in the this repository root folder. 
