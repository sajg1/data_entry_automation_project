from bs4 import BeautifulSoup
import requests

RIGHTMOVE_URL = 'https://www.rightmove.co.uk/property-to-rent/find.html?searchType' \
                '=RENT&locationIdentifier=REGION%5E475&insId=1&radius=0.0&minPrice=' \
                '&maxPrice=1000&minBedrooms=1&maxBedrooms=&displayPropertyType=flats&maxDaysSinceAdded=' \
                '&sortByPriceDescending=&_includeLetAgreed=on&primaryDisplayPropertyType=' \
                '&secondaryDisplayPropertyType=&oldDisplayPropertyType=&oldPrimaryDisplayPropertyType=' \
                '&letType=&letFurnishType=&houseFlatShare='

GOOGLE_FORM_URL = 'https://docs.google.com/forms/d/e/1FAIpQLSdIYPzH1Aim7R4IFqI4BQeVIbkGcb8pTfEeXbJF-' \
                  'R9KQ5Rtpw/viewform?usp=sf_link'

response = requests.get(RIGHTMOVE_URL)
rightmove_listings = response.text
soup = BeautifulSoup(rightmove_listings, 'html.parser')

print(soup.prettify())