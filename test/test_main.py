from __future__ import print_function
import unicornhatflappybird.main
import unittest


class MainTestCase(unittest.TestCase):
    def test__init__(self):
        self.assertTrue("main" in dir(unicornhatflappybird.main))
