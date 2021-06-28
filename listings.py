import re
import csv
import requests
import click
from bs4 import BeautifulSoup
from resources import regions, region_options

#regions = {
 #   "London": "5E93917",
  #  "Greater-Manchester": "5E79192",
   # "Devon": "5E61297"
#}

class Config(object):

    def __init__(self):
        self.save_file = False

pass_config = click.make_pass_decorator(Config, ensure=True)

@click.group()
@click.option(
        '--save-file',
        is_flag=True,
        help='Provide option if you want to save scrape into a output file.'
        )
@click.option('--filepath',
        type=click.Path(()),
        help='Provide a output filepath for saved data.'
        )
@pass_config
def cli(config, save_file, filepath):

    '''
    Generate webscraped property data from RightMove that can be saved into an output CSV file.
    '''
    config.save_file = save_file
    config.filepath = filepath


@cli.command()
@click.option(
        '--pages',
        default=1,
        help='Select the number of pages you wish to scrape'
        )
@click.option(
        '--region',
        default='London',
        type=click.Choice(region_options),#['London', 'Greater-Manchester', 'Devon']),
        help='Select a region to search for property listings.'
        )
@pass_config
def scraper(config, pages, region):

    '''
    Scrape RightMove for-sale property data listings.
    '''
    
    def parse_data(table=None, data=None):
        
        '''
        Function to parse gathered html objects and delimit tags by set find parameters. Returning aggregated list dataset.
        '''
        # specific html segment content for web scraping
        for tag in data.find_all('div', { 'class': 'l-searchResult is-list' }):      
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

            table.append(row)

        return table

    listings = []
    header_row = [ 'address', 'country', 'name', 'date_added', 'price', 'description' ]
    listings.append(header_row)

    record = 0
    for i in range(0, pages): 
        html = requests.get(
            'https://www.rightmove.co.uk/property-for-sale/find.html?locationIdentifier=REGION%5E{region}&index={pg}'
            .format(region=regions[region], pg=record)
            ).text

        soup = BeautifulSoup(html, 'html.parser')

        parse_data(table=listings, data=soup)

        record += 24

    # Qualify if save-file option has been provided, otherwise echo gathered dataset.
    if config.save_file:

        if config.filepath is None:
            config.filepath = './scraped_data.csv'

        with open(file=config.filepath, mode="w", newline="") as f:
            write = csv.writer(f)
            write.writerows(listings)

    else:
        click.echo(listings)

