from __future__ import print_function


class Board:
    COLUMNS = None

    ROWS = None

    COORDINATES = None

    def __init__(self, columns, rows):
        print("[Board][info] Initialising Board")

        self.COLUMNS = columns
        self.ROWS = rows
        self.__generate()

    def __generate(self):
        self.COORDINATES = [
            [0 for x in xrange(self.COLUMNS)]
            for y in xrange(self.ROWS)
        ]

    def columns(self):
        print("[Board][info] Getting Board columns")

        return self.COLUMNS

    def rows(self):
        print("[Board][info] Getting Board rows")

        return self.ROWS

    def coordinates(self):
        print("[Board][info] Getting Board coordinates")

        return self.COORDINATES

    def check_collision(self, pipe, offset):
        print("[Board][info] Checking for Bird collision")

        offset_x, offset_y = offset

        if 0 > offset_y or offset_y > self.COLUMNS - 1:
            return True
        else:
            if pipe.coordinates()[offset_y][0] > 0 and pipe.x() == offset_x:
                return True

        return False

    def clear(self):
        print("[Board][info] Clearing board")

        self.COORDINATES = None
        self.COLUMNS = None
        self.ROWS = None

    def cleanup(self):
        print("[Board][info] Board clean up")

        self.clear()

    def __exit__(self):
        print("[Board][info] Board exit")

        self.cleanup()
