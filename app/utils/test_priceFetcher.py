from unittest import TestCase
from app.utils.PriceFetcher import PriceFetcher


class TestPriceFetcher(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.pf = PriceFetcher()

    def test_update_rate(self):
        self.pf.exchange_rate = -1
        self.pf.update_rate()
        self.assertNotAlmostEquals(self.pf.exchange_rate, -1)

    def test_convert_to_mtg_goldfish(self):
        comma_test = 'Borrowing 100,000 Arrows'
        apostrophe_test = "Rakdos's Return"
        both_test = "Elspeth, Sun's Champion"
        self.assertEqual(self.pf.convert_to_mtg_goldfish(comma_test), 'Borrowing+100+000+Arrows')
        self.assertEqual(self.pf.convert_to_mtg_goldfish(apostrophe_test), 'Rakdoss+Return')
        self.assertEqual(self.pf.convert_to_mtg_goldfish(both_test), "Elspeth+Suns+Champion")

    def test_get_price_from_mtg_goldfish(self):
        bad_url = "https://www.google.com/qweasdfqeadsc"
        good_url = "https://www.mtggoldfish.com/price/Amonkhet/Nissa+Steward+of+Elements/"
        valid_url_with_no_paper_price = "https://www.mtggoldfish.com/price/Vintage+Masters/Black+Lotus"
        self.assertLess(self.pf.get_price_from_mtg_goldfish(bad_url), 0)
        self.assertGreater(self.pf.get_price_from_mtg_goldfish(good_url), 0)
        self.assertLess(self.pf.get_price_from_mtg_goldfish(valid_url_with_no_paper_price), 0)

    def test_convert_to_cad(self):
        self.assertAlmostEqual(self.pf.convert_to_cad(3), self.pf.exchange_rate * 3)

    def test_get_price(self):
        invalid_card = {
            'name': 'not_a_card_name',
            'set': 'not_a_card_set',
            'is_foil': False,
            'collector_number': 1729,
            'condition': 'MP'
        }
        valid_card = {
            'name': 'Forest',
            'set': 'Shadows over Innistrad',
            'is_foil': False,
            'collector_number': 295,
            'condition': 'NM'
        }
        self.assertLess(self.pf.get_price(invalid_card), 0)
        self.assertGreater(self.pf.get_price(valid_card), 0)

    def test_apply_condition_multiplier(self):
        price = 1
        self.assertAlmostEqual(self.pf.apply_condition_multiplier(price, 'NM'), 1)
        self.assertAlmostEqual(self.pf.apply_condition_multiplier(price, 'SP'), 0.9)
        self.assertAlmostEqual(self.pf.apply_condition_multiplier(price, 'MP'), 0.75)
        self.assertAlmostEqual(self.pf.apply_condition_multiplier(price, 'HP'), 0.5)

    def test_price_adjustment(self):
        price_adjustment = 1.1
        card = {
            'name': 'Tarmogoyf',
            'set': 'Future Sight',
            'is_foil': True,
            'collector_number': 153,
            'condition': 'NM'
        }
        self.assertGreater(self.pf.get_price(card, price_adjustment), self.pf.get_price(card))

