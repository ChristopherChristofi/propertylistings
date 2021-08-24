import re, requests, logging
from bs4 import BeautifulSoup
from propertylistings.utilities import URICreator

class PropertiesWebTool:

    data = []
    max_pages = 42

    def __init__(
        self,
        pages: int = None,
        region: str = None,
        min_price: int = None,
        max_price: int = None,
        min_beds: str = None,
        max_beds: str = None,
        retirement: bool = None,
        shared: bool = None,
        new_home: bool = None,
        garden: bool = None,
        parking: bool = None,
        auction: bool = None,
        max_days: str = None,
        offer_sold: bool = False
        ):

        self.pages = pages
        self.region = region
        self.uri = URICreator(
                min_price=min_price,
                max_price=max_price,
                min_beds=min_beds,
                max_beds=max_beds,
                retirement=retirement,
                shared=shared,
                new_home=new_home,
                garden=garden,
                parking=parking,
                auction=auction,
                max_days=max_days,
                offer_sold=offer_sold
                ).generator()

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
            # scrape sales update status data
            status = tag.find('span', { 'class': 'propertyCard-branchSummary-addedOrReduced' }).text.split()
            # qualify 3 part string tag: status space date
            if len(status) == 3:
                row.append(status[0])
                row.append(status[2])
            if len(status) != 3:
                row.append('NA')
                row.append('NA')
            # display data for sale price
            row.append(re.sub('£|,', '', tag.find('div', { 'class': 'propertyCard-priceValue' }).text.rstrip()))
            # sales description for the property. Punctuation handling and CSV delimitation
            row.append(''.join(('"',re.sub('\n|\r', '', tag.find('span', { 'itemprop': 'description' }).text),'"')))

            self.data.append(row)

            logging.info('Property record added: {address}'.format(address=str(row[2])))

    def scrape_origin(self):

        '''
        Responsible for initiating the html requests connection that is used in the build of the webscraping tool,
        with user defined settings. Contains the callable data parsing function generating the complete dataset.
        '''

        # typically 24 for-sale property records per distinct webpage (from source maximum pages is '42')
        record = 0

        if self.pages > self.max_pages: self.pages = self.max_pages

        for i in range(0, self.pages):
            html = requests.get(
                'https://www.rightmove.co.uk/property-for-sale/find.html?locationIdentifier=REGION%5E{region}&index={pg}{uri}'
                .format(
                    region=self.region,
                    pg=record,
                    uri=self.uri
                    )
                ).text

            soup = BeautifulSoup(html, 'html.parser')

            self.parse_data(scrape = soup)

            logging.info('Page: {page_index} scraped'.format(page_index=i+1))

            record += 24

    def generate_data(self):

        '''
        Initiates webscraping call to action and data generation, returning complete dataset.
        '''

        logging.info('Start. Searching region: {region}'.format(region=self.region))

        header_row = [ 'address', 'country', 'name', 'update_status', 'date', 'price', 'description' ]

        self.data.append(header_row)

        self.scrape_origin()

        logging.info('Complete')

        return self.data
