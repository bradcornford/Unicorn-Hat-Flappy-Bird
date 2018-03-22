from __future__ import print_function
from unicornhatflappybird.lib.pipe import Pipe
import unittest


class PipeTestCase(unittest.TestCase):
    COORDINATES = [
        [1]
    ]

    pipe = None

    def setUp(self):
        self.pipe = Pipe(self.COORDINATES)

    def test__init__(self):
        self.assertIsInstance(self.pipe, Pipe)

    def test_set_coordinates(self):
        self.assertIs(self.pipe.set_coordinates([[0]]), None)
        self.assertEquals(self.pipe.coordinates(), [[0]])

    def test_set_x(self):
        self.assertIs(self.pipe.set_x(1), None)
        self.assertEquals(self.pipe.x(), 1)

    def test_set_y(self):
        self.assertIs(self.pipe.set_y(1), None)
        self.assertEquals(self.pipe.y(), 1)

    def test_set_position(self):
        self.assertIs(self.pipe.set_position((1, 1)), None)
        self.assertEquals(self.pipe.x(), 1)
        self.assertEquals(self.pipe.y(), 1)

    def test_coordinates(self):
        self.assertEquals(self.pipe.coordinates(), self.COORDINATES)

    def test_x(self):
        self.assertEquals(self.pipe.x(), 0)

    def test_y(self):
        self.assertEquals(self.pipe.y(), 0)

    def test_position(self):
        self.assertEquals(self.pipe.position(), (0, 0))

    def test_cleanup(self):
        self.assertIs(self.pipe.cleanup(), None)

    def test__exit__(self):
        self.assertIs(self.pipe.__exit__(), None)


if __name__ == '__main__':
    unittest.main()
