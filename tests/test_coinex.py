import plugin

import unittest

import plugin
import config

class TestCoinex(unittest.TestCase):
    def test_balance(self):
        self.assertTrue(plugin.coinex.balance() != None)  # and here


if __name__ == "__main__":
    unittest.main()