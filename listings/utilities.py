class URICreator:

    '''
    Creates a URI object that denotes the search filter requirements that meet
    the input of the search command provided.
    '''

    uri_object = {
            1 : "{option_1}",
            2 : "{option_1}%2C{option_2}",
            3 : "{option_1}%2C{option_2}%2C{option_3}"
            }

    selection = { 1 : '', 2 : '', 3 : '' }

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
        max_days: str,
        offer_sold: bool
        ):

        self.uri = None
        self.min_price = min_price
        self.max_price = max_price
        self.min_beds = min_beds
        self.max_beds = max_beds
        self.retirement = retirement
        self.shared = shared
        self.new_home = new_home
        self.garden = garden
        self.parking = parking
        self.auction = auction
        self.max_days = '&maxDaysSinceAdded={max_days}'.format(max_days=max_days)
        self.offer_sold = '&includeSSTC={under_offer_sold}'.format(under_offer_sold=offer_sold)

    def must_have_switch_bools_URI(self):

        '''
        Responsible for qualifying the URI object resources from the boolean
        returns of the command's options selected regarding must have filtering.
        '''

        request = 0

        if self.retirement == True:
            request += 1
            self.selection[request] = 'retirement'
        if self.shared == True:
            request += 1
            self.selection[request] = 'sharedOwnership'
        if self.new_home == True:
            request += 1
            self.selection[request] = 'newHome'

        try:
            # Generates the URI from truly present selections in order of request count.
            must_have = self.uri_object[request].format(
                    option_1=self.selection[1],
                    option_2=self.selection[2],
                    option_3=self.selection[3]
                    )
        except KeyError:
            # No filter parameter has been provided in the command
            return None

        return must_have


    def must_have_flag_bools_URI(self):

        '''
        Responsible for qualifying the URI object resources from the boolean
        returns of the command's options selected regarding must have filtering.
        '''

        request = 0

        if self.garden == True:
            request += 1
            self.selection[request] = 'garden'
        if self.parking == True:
            request += 1
            self.selection[request] = 'parking'
        if self.auction == True:
            request += 1
            self.selection[request] = 'auction'

        try:
            # Generates the URI from truly present selections in order of request count.
            must_have = self.uri_object[request].format(
                    option_1=self.selection[1],
                    option_2=self.selection[2],
                    option_3=self.selection[3]
                    )
        except KeyError:
            # No filter parameter has been provided in the command
            return None

        return must_have

    def must_have_URI(self):

        '''
        Responsible for combining the must have URI objects that persist from two different
        boolean type classifiers.
        '''

        part_1 = self.must_have_switch_bools_URI()

        part_2 = self.must_have_flag_bools_URI()

        if part_1 and part_2: return part_1 + "%2C" + part_2
        elif part_1 and not part_2: return part_1
        elif part_2 and not part_1: return part_2
        else: return None

    def do_not_show_URI(self):

        '''
        Responsible for qualifying the URI object resources from the boolean
        returns of the command's options selected regarding do not show filtering.
        '''

        request = 0

        if self.retirement == False:
            request += 1
            self.selection[request] = 'retirement'
        if self.shared == False:
            request += 1
            self.selection[request] = 'sharedOwnership'
        if self.new_home == False:
            request += 1
            self.selection[request] = 'newHome'

        try:
            # Generates the URI from truly present selections in order of request count.
            do_not_show = self.uri_object[request].format(
                    option_1=self.selection[1],
                    option_2=self.selection[2],
                    option_3=self.selection[3])
        except KeyError:
            # No filter parameter has been selected in the command
            return None

        return do_not_show

    def qualify_price(self):

        '''
        Responsible for validating price parameters and generating URI object, switches illogical price parameters.
        '''

        if self.min_price and self.max_price:
            if self.min_price > self.max_price:
                actual_max = self.min_price
                self.min_price = self.max_price
                self.max_price = actual_max

        price = '&minPrice={min_price}&maxPrice={max_price}'.format(min_price=self.min_price, max_price=self.max_price)

        return price

    def qualify_bedrooms(self):

        '''
        Responsible for validating bedrooms parameters and generating URI object, switches illogical room counts parameters.
        '''

        if self.min_beds and self.max_beds:
            if self.min_beds > self.max_beds:
                actual_max = self.min_beds
                self.min_beds = self.max_beds
                self.max_beds = actual_max

        bedrooms = '&minBedrooms={min_beds}&maxBedrooms={max_beds}'.format(min_beds=self.min_beds, max_beds=self.max_beds)

        return bedrooms

    def generator(self):

        '''
        Responsible for integrating the creation of the URI string object that
        entails the details of the filter parameters relevant to the selections
        provided in the command.
        '''

        self.uri = '{price}{beds}{max_days}{under_offer_sold}&mustHave={musthave}&dontShow={dontshow}'.format(
                price=self.qualify_price(),
                beds=self.qualify_bedrooms(),
                max_days=self.max_days,
                under_offer_sold=self.offer_sold,
                musthave=self.must_have_URI(),
                dontshow=self.do_not_show_URI()
                )

        return self.uri
