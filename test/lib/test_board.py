from __future__ import print_function
from unicornhatflappybird.lib.board import Board
from unicornhatflappybird.lib.bird import Bird
import unittest


class BoardTestCase(unittest.TestCase):
    COLUMNS = 2
    ROWS = 2

    board = None

    def setUp(self):
        self.board = Board(self.COLUMNS, self.ROWS)

    def test__init__(self):
        self.assertIsInstance(self.board, Board)

    def test_columns(self):
        self.assertEquals(self.board.columns(), self.COLUMNS)

    def test_rows(self):
        self.assertEquals(self.board.rows(), self.ROWS)

    def test_coordinates(self):
        self.assertEquals(self.board.coordinates(), [[0, 0], [0, 0]])

    def test_check_collision(self):
        bird = Bird([[1]])
        self.assertIs(self.board.check_collision(bird, (bird.x(), bird.y())), True)

    def test_clear(self):
        self.assertIs(self.board.clear(), None)

    def test_cleanup(self):
        self.assertIs(self.board.cleanup(), None)

    def test__exit__(self):
        self.assertIs(self.board.__exit__(), None)


if __name__ == '__main__':
    unittest.main()
