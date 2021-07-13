import click, csv
from listings.archive import logger
from listings.resources import region_options
from listings.scraper import Scraper

class Config(object):

    def __init__(self):
        self.save_file = False

pass_config = click.make_pass_decorator(Config, ensure=True)

@click.group()
@click.option(
        '--save-file',
        is_flag=True,
        help='Provide option to save scraped data into an output file.'
        )
@click.option('--filepath',
        type=click.Path(()),
        help='Provide an output filepath for saved data, otherwise will be default.'
        )
@click.option('--log',
        default='listings.log',
        type=click.Path(()),
        help='Provide a output filepath for a log file.'
        )
@pass_config
def cli(config, save_file, filepath, log):

    '''
    Generate webscraped property data from RightMove that can be saved into an output CSV file.
    '''
    config.save_file = save_file
    config.filepath = filepath

    # TODO move to scraper command
    logger(log)

@cli.command()
@click.option(
        '--pages',
        default=1,
        help='Select the number of pages you wish to scrape'
        )
@click.option(
        '--region',
        default='London',
        type=click.Choice(region_options, case_sensitive=False),
        help='Select a region to search for property listings.'
        )
@click.option(
        '--min-price',
        default=None,
        type=int,
        help='Provide an integer value that is the minimun sales price that you want to search by.'
        )
@click.option(
        '--max-price',
        default=None,
        type=int,
        help='Provide an integer value that is the maximum sales price that you want to search by.'
        )
@click.option(
        '--max-beds',
        default=None,
        type=click.Choice(['0','1','2','3','4','5','6','7','8','9','10']),
        help='Define the maximum amount of bedrooms a proerty should require in the search.'
        )
@click.option(
        '--min-beds',
        default=None,
        type=click.Choice(['0','1','2','3','4','5','6','7','8','9','10']),
        help='Define the minimum amount of bedrooms a proerty should require in the search.'
        )
@click.option(
        '--retirement/--no-retirement',
        default=None,
        help='Filter for or filter out retirement properties in your search.'
        )
@click.option(
        '--shared/--no-shared',
        default=None,
        help='Filter for or filter out shared-ownership properties in your search.'
        )
@click.option(
        '--new-home/--no-new-home',
        default=None,
        help='Filter for or filter out new build properties in your search.'
        )
@click.option(
        '--garden',
        is_flag=True,
        help='Select so that each property record searched for must have a garden.'
        )
@click.option(
        '--parking',
        is_flag=True,
        help='Select so that each property record searched for must have parking.'
        )
@click.option(
        '--auction',
        is_flag=True,
        help='Select so that each property record searched for is an auction property.'
        )
@click.option(
        '--max-days',
        default=None,
        type=click.Choice(['1','3','7','14']),
        help='Select the maximum days for when a property was first added.'
        )
@click.option(
        '--offer-sold',
        is_flag=True,
        help='Select so that property records that are either under offer or sold are also returned.'
        )
@pass_config
def search(
        config,
        pages,
        region,
        min_price,
        max_price,
        min_beds,
        max_beds,
        retirement,
        shared,
        new_home,
        garden,
        parking,
        auction,
        max_days,
        offer_sold
        ):

    '''
    Scrape RightMove for-sale property data listings.
    '''

    scrape = Scraper(
            pages,
            region,
            min_price,
            max_price,
            min_beds,
            max_beds,
            retirement,
            shared,
            new_home,
            garden,
            parking,
            auction,
            max_days,
            offer_sold
            )

    listings = scrape.generate_data()

    # Qualify if save-file option has been provided, otherwise echo gathered dataset.
    if config.save_file:

        if config.filepath is None:
            config.filepath = './scraped_data.csv'

        with open(file=config.filepath, mode="w", newline="") as f:
            write = csv.writer(f)
            write.writerows(listings)

    else:
        click.echo(listings)


