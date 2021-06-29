import re
import requests
from bs4 import BeautifulSoup
from dataclasses import dataclass
from resources import regions

@dataclass
class Dataset:
    
    address: str
    country: str
    name: str
    date_added: str
    price: int
    description: str

@dataclass
class Scraper:

    def __init__(self, pages: int, region: str, table: list[Dataset]):

        self.pages = pages
        self.region = region
        self.table = table

    def parse_data(self, scrape):

        '''
        Responsible for generating an aggregated list of gathered data objects defined by set parsing parameters.
        Returng a dataset for each scraped page.
        '''

        # specific html segment content for web scraping
        for tag in scrape.find_all('div', { 'class': 'l-searchResult is-list' }):      
            row = []

            # public property for sale address
            row.append(re.sub(',|\r|\n', '', tag.find('meta', { 'itemprop': 'streetAddress' })['content']))
            # country for property on sale
            row.append(tag.find('meta', { 'itemprop': 'addressCountry' })['content'])
            # name type for property, for example: 5 bed house 
            row.append(re.sub('\n|\r', '', tag.find('h2', { 'class': 'propertyCard-title' }).text).strip())
            # date property was first added or reduced for sale
            row.append(tag.find('span', { 'class': 'propertyCard-branchSummary-addedOrReduced' }).text)
            # display data for sale price
            row.append(re.sub('£|,', '', tag.find('div', { 'class': 'propertyCard-priceValue' }).text.rstrip()))
            # sales description for the property. Punctuation handling and CSV delimitation 
            row.append(''.join(('"',re.sub('\n|\r', '', tag.find('span', { 'itemprop': 'description' }).text),'"')))

            self.table.append(row)

    def scrape_origin(self):
        
        '''
        Contains the callable data parsing function and returns the complete dataset. Responsible for initiating the html
        requests connection that is used in the build of the webscraping tool, with user defined settings.
        '''

        # typically 24 for-sale property records per distinct webpage
        record = 0

        for i in range(0, self.pages): 
            html = requests.get(
                'https://www.rightmove.co.uk/property-for-sale/find.html?locationIdentifier=REGION%5E{region}&index={pg}'
                .format(region=regions[self.region], pg=record)
                ).text

            soup = BeautifulSoup(html, 'html.parser')

            self.parse_data(scrape = soup)

            record += 24

        return self.table

