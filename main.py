from bs4 import BeautifulSoup
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import requests

RIGHTMOVE_URL = 'https://www.rightmove.co.uk/property-to-rent/find.html?searchType' \
                '=RENT&locationIdentifier=REGION%5E475&insId=1&radius=0.0&minPrice=' \
                '&maxPrice=1000&minBedrooms=1&maxBedrooms=&displayPropertyType=flats&maxDaysSinceAdded=' \
                '&sortByPriceDescending=&_includeLetAgreed=on&primaryDisplayPropertyType=' \
                '&secondaryDisplayPropertyType=&oldDisplayPropertyType=&oldPrimaryDisplayPropertyType=' \
                '&letType=&letFurnishType=&houseFlatShare='

GOOGLE_FORM_URL = 'https://docs.google.com/forms/d/e/1FAIpQLSdIYPzH1Aim7R4IFqI4BQeVIbkGcb8pTfEeXbJF-' \
                  'R9KQ5Rtpw/viewform?usp=sf_link'

CHROME_DRIVER_PATH = '/Users/admin/Development/chromedriver'

# BEAUTIFULSOUP
# FIND ALL RESULTING LISTINGS DOM ELEMENTS
response = requests.get(RIGHTMOVE_URL)
rightmove_listings = response.text
soup = BeautifulSoup(rightmove_listings, 'html.parser')
property_results = soup.find_all(name='div', class_="l-searchResult")


listings = []
for result in property_results:
    new_dict = {}
    price = result.find(name="span", class_="propertyCard-priceValue")
    address = result.find(name="address", class_="propertyCard-address")
    link = result.find(name="a", class_="propertyCard-img-link")['href']
    new_dict["address"] = address.text.replace("\n", "")
    new_dict["price"] = price.text.split(" ")[0]
    new_dict["link"] = f"https://www.rightmove.co.uk/{link}"
    listings.append(new_dict)
print(listings)

# SELENIUM
# ACCESS GOOGLE FORM AND FILL IN FOR EACH LISTING
driver = webdriver.Chrome(executable_path=CHROME_DRIVER_PATH)
driver.get(GOOGLE_FORM_URL)

time.sleep(2)
address_input = driver.find_element(By.CSS_SELECTOR, "[aria-labelledby='i1']")
address_input.send_keys(listings[0]['address'])
time.sleep(2)
price_input = driver.find_element(By.CSS_SELECTOR, "[aria-labelledby='i5']")
price_input.send_keys(listings[0]['price'])
time.sleep(2)
link_input = driver.find_element(By.CSS_SELECTOR, "[aria-labelledby='i9']")
link_input.send_keys(listings[0]['link'])
time.sleep(10)

# for listing in listings:
#     time.sleep(2)
#     address_input = driver.find_element(By.CSS_SELECTOR, "[aria-labelledby='i1']")
#     address_input.send_keys(listing['address'])


# <input type="text" class="quantumWizTextinputPaperinputInput exportInput" jsname="YPqjbf" autocomplete="off" tabindex="0" aria-labelledby="i1" aria-describedby="i2 i3" required="" dir="auto" data-initial-dir="auto" data-initial-value="">
#
# <input type="text" class="quantumWizTextinputPaperinputInput exportInput" jsname="YPqjbf" autocomplete="off" tabindex="0" aria-labelledby="i5" aria-describedby="i6 i7" required="" dir="auto" data-initial-dir="auto" data-initial-value="" >
#
# <input type="text" class="quantumWizTextinputPaperinputInput exportInput" jsname="YPqjbf" autocomplete="off" tabindex="0" aria-labelledby="i9" aria-describedby="i10 i11" required="" dir="auto" data-initial-dir="auto" data-initial-value="" >