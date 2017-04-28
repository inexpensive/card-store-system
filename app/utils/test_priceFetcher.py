from unittest import TestCase
from app.utils.PriceFetcher import PriceFetcher, round_price


class TestPriceFetcher(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.pf = PriceFetcher()
        cls._set = 'BFZ'
        cls.prices = cls.pf.get_set_prices(cls._set)
        cls.test_card = 'Gideon, Ally of Zendikar'

    def test_update_rate(self):
        self.pf.exchange_rate = -1
        self.pf.update_rate()
        self.assertNotAlmostEquals(self.pf.exchange_rate, -1)

    def test_convert_to_cad(self):
        self.assertAlmostEqual(self.pf.convert_to_cad(3), self.pf.exchange_rate * 3)

    def test_apply_condition_multiplier(self):
        price = 1
        self.assertAlmostEqual(self.pf.apply_condition_multiplier(price, 'NM'), 1)
        self.assertAlmostEqual(self.pf.apply_condition_multiplier(price, 'SP'), 0.9)
        self.assertAlmostEqual(self.pf.apply_condition_multiplier(price, 'MP'), 0.75)
        self.assertAlmostEqual(self.pf.apply_condition_multiplier(price, 'HP'), 0.5)

    def test_get_set_prices_works_for_valid_set(self):
        self.assertGreater(self.prices.__len__(), 0)
        self.assertGreater(self.prices[self.test_card][0], 0)

    def test_get_set_prices_works_for_valid_and_foil_set(self):
        foil_prices = self.pf.get_set_prices(self._set, foil=True)
        self.assertGreater(foil_prices.__len__(), 0)
        self.assertGreater(foil_prices[self.test_card], self.prices[self.test_card])

    def test_get_set_prices_does_not_work_for_invalid_set(self):
        _set = 'not_a_set'
        prices = self.pf.get_set_prices(_set)
        self.assertEqual(prices.__len__(), 0)

    def test_price_adjustment(self):
        price_adjustment = 1.1
        with_adj = self.pf.get_set_prices(self._set, price_adjustment)
        self.assertGreater(with_adj[self.test_card][0], self.prices[self.test_card][0])

    def test_round_price(self):
        self.assertAlmostEqual(round_price(0.1), 0.25)
        self.assertAlmostEqual(round_price(0.45), 0.5)
        self.assertAlmostEqual(round_price(0.77), 0.75)
        self.assertAlmostEqual(round_price(2.33), 2.29)
        self.assertAlmostEqual(round_price(8.33), 8.49)
        self.assertAlmostEqual(round_price(27.44), 26.99)
        self.assertAlmostEqual(round_price(277.55), 279.99)
