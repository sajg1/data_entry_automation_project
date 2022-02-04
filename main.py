from bs4 import BeautifulSoup
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import os
import requests

GOOGLE_EMAIL = os.environ.get('GOOGLE_EMAIL')
GOOGLE_PASSWORD = os.environ.get('GOOGLE_PASSWORD')
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


# SELENIUM
# ACCESS GOOGLE FORM AND FILL IN FOR EACH LISTING
driver = webdriver.Chrome(executable_path=CHROME_DRIVER_PATH)
driver.get(GOOGLE_FORM_URL)

# FILL IN GOOGLE FORM FOR EACH LISTING
for i in range(len(listings)):
    time.sleep(2)
    address_input = driver.find_element(By.CSS_SELECTOR, "[aria-labelledby='i1']")
    address_input.send_keys(listings[i]['address'])
    time.sleep(2)
    price_input = driver.find_element(By.CSS_SELECTOR, "[aria-labelledby='i5']")
    price_input.send_keys(listings[i]['price'])
    time.sleep(2)
    link_input = driver.find_element(By.CSS_SELECTOR, "[aria-labelledby='i9']")
    link_input.send_keys(listings[i]['link'])
    time.sleep(2)
    submit_button = driver.find_element(By.CLASS_NAME, 'appsMaterialWizButtonPaperbuttonLabel')
    submit_button.click()
    time.sleep(5)
    if i <= (len(listings)-1):
        submit_another_button = driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[1]/div/div[4]/a')
        submit_another_button.click()
    else:
        print("done")


# Attempting to create the spreadsheet after completion of all the forms.
# Think I need to sign back in to google to do this

# SIGNIN TO GOOGLE THROUGH MEDIUM FIRST TO BYPASS GOOGLE SIGNIN FAIL

# driver.get("https://www.medium.com")
# driver.maximize_window()
# time.sleep(3)
# signin_medium = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[3]/div[1]/div/div/div/div[3]/span[4]/div/p/span/a')
# signin_medium.click()
# time.sleep(5)
# signin_with_google = driver.find_element(By.TAG_NAME, 'a')
# signin_with_google.click()
# # time.sleep(10)
# #


# email_input = driver.find_element(By.CSS_SELECTOR, "[aria-label='Email or phone']")
# time.sleep(5)
# next_button = driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div[2]/div/div[2]/div/div/div[2]/div/div[2]'
#                                             '/div/div[1]/div/div/button/span')
# time.sleep(5)
# email_input.send_keys(GOOGLE_EMAIL)
# time.sleep(5)
# next_button.click()
# time.sleep(5)
# password_input = driver.find_element(By.CSS_SELECTOR, "[aria-label='Enter your password']")
# time.sleep(5)
# password_input.send_keys(GOOGLE_PASSWORD)
# time.sleep(10)
#
# create_sheet_button = driver.find_element(By.CLASS_NAME, 'appsMaterialWizButtonPapericonbuttonContentSpan')
# time.sleep(5)
# create_sheet_button.click()
# time.sleep(20)

#