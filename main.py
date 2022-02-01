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

all_properties = soup.find_all(name='div', class_="l-searchResult")

print(len(all_properties))

data = []
for property in all_properties:
    new_dict = {}
    price = property.find(name="span", class_="propertyCard-priceValue")
    address = property.find(name="address", class_="propertyCard-address")
    link = property.find(name="a", class_="propertyCard-img-link")['href']
    new_dict["price"] = price.text.split(" ")[0]
    new_dict["address"] = address.text.replace("\n", "")
    new_dict["link"] = f"https://www.rightmove.co.uk/{link}"

    print(new_dict)
    data.append(new_dict)


print(data[0])
