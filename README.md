# web-scraping-challenge
Scraping sites with Mars information and creating a single web page of the data.

# System Setup
The webscraping funcionality utilizes Chrome Driver. If using a Mac, all that is needed is to install Chrome Driver with no further changes to the code. 
To use on a PC you will also need to change the following code block in scrape_mars.py to refelect the install location of your Chrome Driver.

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)
