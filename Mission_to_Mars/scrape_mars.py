import pandas as pd
import pymongo
import time
from bs4 import BeautifulSoup as bs
from splinter import Browser


def init_browser():
    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser('chrome', **executable_path, headless=False)

def scrape_info():
    browser = init_browser()
    mars_dict = {}

    #MARS NEWS
    news_url= 'https://mars.nasa.gov/news/'
    browser.visit(news_url)
    html=browser.html
    news_soup = bs(html, 'html.parser')
    news_title = news_soup.find_all('div', class_='content_title')[0].text
    news_p = news_soup.find_all('div', class_='article_teaser_body')[0].text

    #MARS IMAGE
    image_url= 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(image_url)
    html=browser.html
    image_soup = bs(html, 'html.parser')
    section=image_soup.find('div', class_ = "default floating_text_area ms-layer")
    featured_image=section.find('footer')
    featured_image_url = 'https://www.jpl.nasa.gov' + featured_image.find('a')['data-fancybox-href']

    # MARS FACTS
    facts_url = "https://space-facts.com/mars/"
    tables = pd.read_html(facts_url)
    facts_table = tables[0]
    facts_table.columns = ['Description', 'Mars']
    facts_table.set_index('Description')
    html_table = facts_table.to_html()
    html_table = html_table.replace('\n', '')

    #MARS HEMISPHERES
    home_url='https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(home_url)
    html=browser.html
    home_soup=bs(html, 'html.parser')

    base_url = 'https://astrogeology.usgs.gov/'
    page_list = home_soup.find_all('div', class_ = 'item')
    links = []
    hemisphere_image_urls = []

    for page in page_list: 
        href = page.find('a', class_ = 'itemLink product-item')
        link = base_url + href['href']
        links.append(link)

    time.sleep(1)

    for link in links:
        hemisphere_dict = {}
        browser.visit(link)
        html = browser.html
        page_soup = bs(html, 'lxml')
        title_block = page_soup.find('div', class_ = 'content')
        title = title_block.find('h2', class_ = 'title').text
        hemisphere_dict["title"] = title
        img_block = page_soup.find('div', class_ = 'downloads')
        img = img_block.find('a')['href']
        hemisphere_dict['img_url'] = img
        hemisphere_image_urls.append(hemisphere_dict)

    #MARS DICT
    mars_dict = {
            "news_title": news_title,
            "news_p": news_p,
            "featured_image_url": featured_image_url,
            "html_table": str(html_table),
            "hemisphere_image_url": hemisphere_image_urls}

    return mars_dict