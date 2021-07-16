import unittest
from listings.scraper import Scraper
from listings.utilities import URICreator

class TestListings(unittest.TestCase):

    def test_search(self):
        count=0
        for record in Scraper(pages=1, region="London").generate_data():
            assert record[0]
            count += 1
            if count == 5: break
        assert count == 5

    def test_qualify_prices(self):

        '''
        Tests wether price inputs are correctly swapped and that records returned match set parameters.
        '''

        count = 0
        for record in Scraper(pages=1, region="London", min_price=1500000, max_price=100000).generate_data():
            if count == 0:
                count += 1
                continue
            if record[4] == "POA" or "poa":
                continue
            self.assertGreaterEqual(int(record[4]), 100000) and self.assertLessEqual(int(record[4]), 1500000)
            count += 1
            if count == 25: break

    def test_must_have(self):

        self.assertEqual(URICreator(
            min_price=None,
            max_price=None,
            max_beds=None,
            min_beds=None,
            retirement=True,
            shared=False,
            new_home=False,
            garden=True,
            parking=False,
            auction=False,
            max_days=None,
            offer_sold=None
            ).must_have_URI(), "retirement%2Cgarden")

        self.assertEqual(URICreator(
            min_price=None,
            max_price=None,
            max_beds=None,
            min_beds=None,
            retirement=True,
            shared=True,
            new_home=True,
            garden=True,
            parking=True,
            auction=True,
            max_days=None,
            offer_sold=None
            ).must_have_URI(), "retirement%2CsharedOwnership%2CnewHome%2Cgarden%2Cparking%2Cauction")

    def test_must_have_empty(self):

        self.assertEqual(URICreator(
            min_price=None,
            max_price=None,
            max_beds=None,
            min_beds=None,
            retirement=False,
            shared=False,
            new_home=False,
            garden=False,
            parking=False,
            auction=False,
            max_days=None,
            offer_sold=None
            ).must_have_URI(), None)

    def test_do_not_show_URI(self):

        self.assertEqual(URICreator(
            min_price=None,
            max_price=None,
            max_beds=None,
            min_beds=None,
            garden=None,
            auction=None,
            max_days=None,
            offer_sold=None,
            parking=None,
            retirement=False,
            shared=False,
            new_home=False
            ).do_not_show_URI(), "retirement%2CsharedOwnership%2CnewHome")

        self.assertEqual(URICreator(
            min_price=None,
            max_price=None,
            max_beds=None,
            min_beds=None,
            garden=None,
            auction=None,
            max_days=None,
            offer_sold=None,
            parking=None,
            retirement=None,
            shared=None,
            new_home=False
            ).do_not_show_URI(), "newHome")

    def test_do_not_show_URI_empty(self):

        self.assertEqual(URICreator(
            min_price=None,
            max_price=None,
            max_beds=None,
            min_beds=None,
            garden=None,
            auction=None,
            max_days=None,
            offer_sold=None,
            parking=None,
            retirement=True,
            shared=True,
            new_home=True
            ).do_not_show_URI(), None)

unittest.main()