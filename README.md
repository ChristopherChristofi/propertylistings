# PropertyListings

## Description:

New way to gather property sales intel from RightMove.

Simple webscraping command-line tool for archiving property sales record data from RightMove property listings website. Build search query functions that can utilise all search parameter filters made available through the website; make it scale and set how many pages of property sales records you wish to scrape.

## Requirements:

- Python 3+

## Installation:

Install python and:

```sh
pip install --upgrade propertylistings
```

## Quickstart:

Using the command-line interface try this search:

```sh
propertylistings search --pages 5 --region Edinburgh
```

Or use as a library:

```sh
from propertylistings.properties_scraper import PropertiesWebTool as properties

for property in properties(pages=25, region="London", min_price=1000000, garden=True, parking=True):
    print(property)
```

Instead of having all rows of property data printing to the terminal, use the write data to a CSV document option:

```sh
propertylistings --save-file search --pages 10 --region city-of-london --max-price 600000 --min-beds 2 --max-beds 3
```

To set the output filepath yourself, include the '--filepath' option also:

```sh
propertylistings --save-file --filepath my_scraped_data.csv search --region Cardiff
```


## Usage:

This is a webscraping tool that grabs available data presented on the RightMove sales feed by their map region. Through all the options made available in PropertyListings, most of, if not every search parameter that exists on RightMove search functionality can be used to create a search query function with PropertyListings. The data and opportunities with this tool are endless, and when you find what you are looking for, go have a look for the same properties on RightMove itself.

For all the search options available to you on PropertyListings, use the '--help' option:

```sh
propertylistings search --help
```

The response data consists of:
- 'address'
- 'country'
- 'name'
- 'status' (such as: when first 'added' or last 'reduced')
- 'date' (specific to the above)
- 'sales description'

The most amount of data you can collect is limited by the page counts set by the RightMove website, this same limitation is enforced in PropertyListings so you don't have to needlessly continue searching if all has been retrieved. It is important to note that not all sales records are visible even on the website itself, at most there is 40+ pages per search and that is around 1000 to 1100 property records.

All the filter parameters that build the search query function in a PropertyListinngs command can include:
- set pages
- set region
- set maximum and minimum bedroom counts
- set maximum and minimum sales price
- select for garden
- select for auction
- select for retirement or filter out
- select for parking
- select for new build or filter out
- select for shared ownership or filter out
- set the max days from when the property was first added
- set whether the property is under offer or sold

The property type, regarding apartments or detached houses, search feature is yet to be added.

An example that uses a lot of these search parameters can be found here:

```sh
propertylistings --save-file search --pages 30 --region devon --max-beds 8 --min-beds 6 --new-home, --no-retirement --offer-sold
```

Returning sales property records based in Devon, that have bedroom count between 8 and 6, is a new build, is not a retirement property, and the data can also include properties under offer or already sold.

Due to the copius amounts of regions and their own subregions again, not every existing RightMove region is available directly through the PropertyListings '--region' option, although, there are plans to continue adding more batches of regions, for now London and other areas around the United Kingdom are available; however, if you cannot find yours on the list (which you find using the help example from above) you are able to add a region temporarily via the '--add-region' option of the main command, which can see below:

```sh
propertylistings --save-file --add-region 813 search --pages 22 --max-price 750000 --max-days 7 --auction
```

The '813' is an example region code for RightMove that will search properties found in 'Liverpool'. With regards to the other options in this search query command, all property data returned will have a maximum price value of £750,000, will have been added within the past 7 days, and will be an auction property.