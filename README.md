# Web Scraping Homework - Mission to Mars

![mission_to_mars](Images/mission_to_mars.png)

In this assignment, a web application was built that scrapes data from five different websites to gather data related to the Mission to Mars and displays the information in a single HTML page.

## Step 1 - Scraping

Completed the initial scraping using Jupyter Notebook, BeautifulSoup, Pandas, and Requests/Splinter.

https://mars.nasa.gov/news/ website was used to get the latest news on Mars mission using BeautifulSoup, splinter, pandas in a jupyter notebook.
https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars was used to scrape the featured image of mars in full resolution.
https://twitter.com/marswxreport?lang=en was used to get the latest tweet on the mars weather.
https://space-facts.com/mars/ to gather the facts table about Mars
https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars to get the images of 4 hemispheres of Mars

 ### Flask:

A python script to run all of the scraping code was designed and all of the scraped data was put into one Python dictionary.
'/scrape' route which will import the Python script and call the scrape function was created.

#### MongoDB:

A new database and a new collection was created.
All of the scraped data was stored in the above created database.
Root route / that will query the database and pass the mars data into HTML template was created.

#### HTML and BootStrap:

Finally a HTML file called 'index.html' was created that displayed all of the data in HTML elements.
Used Bootstrap to structure the HTML template.
