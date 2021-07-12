from listings.resources import *

class URICreator:

    '''
    Creates a URI object that denotes the search filter requirements that meet
    the input of the search command provided.
    '''

    def __init__(
        self,
        min_price: int,
        max_price: int,
        min_beds: str,
        max_beds: str,
        retirement: bool,
        shared: bool,
        new_home: bool,
        garden: bool,
        parking: bool,
        auction: bool,
        max_days: str
        ):

        self.uri = None
        self.min_price = '&minPrice={min_price}'.format(min_price=min_price)
        self.max_price = '&maxPrice={max_price}'.format(max_price=max_price)
        self.min_beds = '&minBedrooms={min_beds}'.format(min_beds=min_beds)
        self.max_beds = '&maxBedrooms={max_beds}'.format(max_beds=max_beds)
        self.retirement = retirement
        self.shared = shared
        self.new_home = new_home
        self.garden = garden
        self.parking = parking
        self.auction = auction
        self.max_days = '&maxDaysSinceAdded={max_days}'.format(max_days=max_days)

    def must_have_URI(self):

        '''
        Responsible for qualifying the URI object resources from the boolean
        returns of the command's options selected regarding must have filtering.
        '''

        request = 0

        if self.retirement == True:
            request += 1
            must_options[request] = 'retirement'
        if self.shared == True:
            request += 1
            must_options[request] = 'sharedOwnership'
        if self.new_home == True:
            request += 1
            must_options[request] = 'newHome'
        if self.garden == True:
            request += 1
            must_options[request] = 'garden'
        if self.parking == True:
            request += 1
            must_options[request] = 'parking'
        if self.auction == True:
            request += 1
            must_options[request] = 'auction'

        try:
            # Generates the URI from truly present selections in order of request count.
            # A maximum of 6 possibilities that match a unique URL composition.
            must_have = must_have_options[request].format(
                    option_1=must_options[1],
                    option_2=must_options[2],
                    option_3=must_options[3],
                    option_4=must_options[4],
                    option_5=must_options[5],
                    option_6=must_options[6]
                    )
        except KeyError:
            # No filter parameter has been provided in the command
            return "&mustHave="

        return must_have

    def do_not_show_URI(self):

        '''
        Responsible for qualifying the URI object resources from the boolean
        returns of the command's options selected regarding do not show filtering.
        '''

        request = 0

        if self.retirement == False:
            request += 1
            not_options[request] = 'retirement'
        if self.shared == False:
            request += 1
            not_options[request] = 'sharedOwnership'
        if self.new_home == False:
            request += 1
            not_options[request] = 'newHome'

        try:
            # Equal to the above
            do_not_show = do_not_show_options[request].format(
                    option_1=not_options[1],
                    option_2=not_options[2],
                    option_3=not_options[3])
        except KeyError:
            # No filter parameter has been selected in the command
            return "&dontShow="

        return do_not_show


    def generator(self):

        '''
        Responsible for integrating the creation of the URI string object that
        entails the details of the filter parameters relevant to the selections
        provided in the command.
        '''

        self.uri = '&minPrice={min_price}{max_price}{min_beds}{max_beds}{max_days}{musthave}{dontshow}'.format(
                min_price=self.min_price,
                max_price=self.max_price,
                min_beds=self.min_beds,
                max_beds=self.max_beds,
                max_days=self.max_days,
                musthave=self.must_have_URI(),
                dontshow=self.do_not_show_URI()
                )

        return self.uri
