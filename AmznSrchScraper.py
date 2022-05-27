import csv
from bs4 import BeautifulSoup
from selenium import webdriver
import datetime

def get_url(search_word, pageNum):
    """Generate URL that will search for specified item"""
    default = 'https://www.amazon.in/s?k={}&page={-}&ref=sr_pg_1'
    url_replaced = default.replace('{}',search_word)
    url_replaced_page = url_replaced.replace('{-}',str(pageNum))
    
    return url_replaced_page

#prototype for 'parsing' one result

def parse_record(item):
    """parse releveant information from HTML of Product"""
    #item NAME
    atag = item.h2.a 
    itemName = atag.text.strip()

    #item URL
    itemURL = 'https://www.amazon.in' + atag.get('href') #get item URL

    try:
        #item PRICE
        price_parent = item.find('span', 'a-price')
        price = price_parent.find('span', 'a-offscreen').text #get price
    except AttributeError:
        return

    try:
        
        #item RATINGS
        rating = item.i.text #get rating /5
        numRatings = item.find('span', {'class': 'a-size-base', 'dir': 'auto'}).text #get number of ratings
    except AttributeError:
        rating = ''
        numRatings = ''
    result = (itemName, price, rating, numRatings, itemURL)
    return result

def main():
    
    #Start the webdriver
    driver = webdriver.Chrome('C:\\Users\\"Your PC Name"\\chromedriver')

    search_term = input("Enter item to search Amazon.in for: ")
    numPages = int(input("Enter how many pages to parse through: "))

    records = []

    for page in range(1,numPages):
        url = get_url(search_term, page)
        driver.get(url)

        #WEBPAGE IS OPEN

        #HTML parser
        #initialize
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        #Find all 'div' items with property 'data-component-type' and value 's-search-result'
        #results will contain the information for each search result on the page
        results = soup.find_all('div', {'data-component-type': 's-search-result'})

        #Parse records for info, place into itemInfos[]
        itemInfos = []
        
        for item in results:
            itemInfos = parse_record(item)
            if itemInfos:
                records.append(itemInfos)
    driver.close()

    #save data
    with open('ScrapData.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Description', 'Price', 'Rating', 'RatingCount', 'Link'])
        writer.writerows(records)