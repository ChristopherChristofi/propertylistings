import re
import requests
from bs4 import BeautifulSoup
from resources import regions

class Scraper:

    data = []

    def __init__(self, pages: int, region: str):

        self.pages = pages
        self.region = region

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

            self.data.append(row)

    def scrape_origin(self):
        
        '''
        Responsible for initiating the html requests connection that is used in the build of the webscraping tool,
        with user defined settings. Contains the callable data parsing function generating the complete dataset.
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

    def generate_data(self):

        '''
        Initiates webscraping call to action and data generation, returning complete dataset.
        '''

        header_row = [ 'address', 'country', 'name', 'date_added', 'price', 'description' ]

        self.data.append(header_row)

        self.scrape_origin()

        return self.data

