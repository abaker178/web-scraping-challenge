# Import Dependencies
from bs4 import BeautifulSoup as bs
from splinter import Browser
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager

def scrape():
    # Initialize browser
    def init_browser():
        executable_path = {'executable_path': ChromeDriverManager().install()}
        return Browser('chrome', **executable_path, headless=False)

    # Function to scrape websites
    ## INPUT: URL as a string
    ## OUTPUT: BeautifulSoup object with html from the scraped website
    def scrapeHTML(url):
        browser.visit(url)
        return bs(browser.html, "html.parser")

    browser = init_browser()

    #### NASA ####
    # Scrape NASA Mars website
    nasa_url = "https://mars.nasa.gov/news/"
    nasa_soup = scrapeHTML(nasa_url)
    # Get the news articles list and store the first (latest) article's information
    first_article = nasa_soup.find("div", class_="list_text")
    news_title = first_article.find("div", class_="content_title").text
    news_p = first_article.find("div", class_="article_teaser_body").text

    #### JPL ####
    # Scrape JPL
    jpl_url = "https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html"
    jpl_root = "https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/"
    jpl_soup = scrapeHTML(jpl_url)
    # Capture the featured image on the JPL site
    rel_path = jpl_soup.find("img", class_="headerimage")["src"]
    featured_image_url = jpl_root + rel_path

    #### Mars Facts ####
    # Scrape Mars Fact site tables
    facts_url = "https://space-facts.com/mars/"
    facts_tables = pd.read_html(facts_url)
    # Convert each to HTML and store the list
    facts_tables_html = []
    for table in facts_tables:
        facts_tables_html.append(table.to_html())

    #### USGS Astrogeology ####
    # Scrape USGS Astrogeology
    usgs_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    usgs_soup = scrapeHTML(usgs_url)
    # Capture links to each hemisphere page
    item_list = usgs_soup.find_all("a", class_="itemLink")
    title_list = []
    for item in item_list:
        if item.text not in title_list and len(item.text) > 1:
            title_list.append(item.text)
    # Navigate to each hemisphere page, scrape it, and store the full size image url
    img_list = []
    for link in title_list:
        browser.links.find_by_partial_text(link).click()
        img = browser.find_by_css(".wide-image")["src"]
        img_list.append(img)
        browser.visit(usgs_url) # return to the main page
    # Iterate through the titles and image urls and create a dictionary for each
    hemisphere_image_urls = []
    for (t, i) in zip(title_list, img_list):
        hemisphere_image_urls.append({
            "title": t,
            "img_url": i
        })

    #### Package and return data dictionary  ####
    data_dict = {
        "news_title": news_title,
        "news_p": news_p,
        "featured_image_url": featured_image_url,
        "facts_tables_html": facts_tables_html,
        "hemisphere_image_urls": hemisphere_image_urls
    }
    browser.quit()

    return data_dict