from __future__ import print_function
from unicornhatflappybird.lib.bird import Bird
import unittest


class BirdTestCase(unittest.TestCase):
    COORDINATES = [
        [1]
    ]

    COLUMNS = 2
    ROWS = 2

    bird = None

    def setUp(self):
        self.bird = Bird(self.COORDINATES)

    def test__init__(self):
        self.assertIsInstance(self.bird, Bird)

    def test_set_coordinates(self):
        self.assertIs(self.bird.set_coordinates([[0]]), None)
        self.assertEquals(self.bird.coordinates(), [[0]])

    def test_set_direction(self):
        self.assertIs(self.bird.set_direction(self.bird.DIRECTION_UP), None)
        self.assertEquals(self.bird.direction(), self.bird.DIRECTION_UP)

    def test_set_x(self):
        self.assertIs(self.bird.set_x(1), None)
        self.assertEquals(self.bird.x(), 1)

    def test_set_y(self):
        self.assertIs(self.bird.set_y(1), None)
        self.assertEquals(self.bird.y(), 1)

    def test_set_position(self):
        self.assertIs(self.bird.set_position((1, 1)), None)
        self.assertEquals(self.bird.x(), 1)
        self.assertEquals(self.bird.y(), 1)

    def test_coordinates(self):
        self.assertEquals(self.bird.coordinates(), self.COORDINATES)
        self.assertEquals(self.bird.coordinates(self.COLUMNS, self.ROWS), [[self.COORDINATES[0][0], False], [False, False]])

    def test_direction(self):
        self.assertEquals(self.bird.direction(), self.bird.DIRECTION_DOWN)

    def test_x(self):
        self.assertEquals(self.bird.x(), 0)

    def test_y(self):
        self.assertEquals(self.bird.y(), 0)

    def test_position(self):
        self.assertEquals(self.bird.position(), (0, 0))

    def test_cleanup(self):
        self.assertIs(self.bird.cleanup(), None)

    def test__exit__(self):
        self.assertIs(self.bird.__exit__(), None)


if __name__ == '__main__':
    unittest.main()
