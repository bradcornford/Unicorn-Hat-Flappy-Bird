

class Bird:
    COORDINATES = None

    X = None
    Y = None

    DIRECTION = None

    DIRECTION_UP = 'up'
    DIRECTION_DOWN = 'down'

    def __init__(self, coordinates, x=0, y=0, direction=DIRECTION_DOWN):
        print("[Bird][info] Initialising Bird")

        self.COORDINATES = coordinates
        self.X = x
        self.Y = y
        self.DIRECTION = direction

    def set_coordinates(self, coordinates):
        print("[Bird][info] Setting Bird coordinates")

        self.COORDINATES = coordinates

    def set_direction(self, direction):
        print("[Bird][info] Setting Bird direction")

        self.DIRECTION = direction

    def set_x(self, x):
        print("[Bird][info] Setting Bird X position")

        self.X = x

    def set_y(self, y):
        print("[Bird][info] Setting Bird Y position")

        self.Y = y

    def set_position(self, coordinates):
        print("[Bird][info] Setting Bird X, Y position")

        x, y = coordinates

        self.X = x
        self.Y = y

    def coordinates(self, columns=0, rows=0):
        print("[Bird][info] Getting Bird coordinates")

        if columns == 0 and rows == 0:
            return self.COORDINATES

        coordinates = [
            [False for x in xrange(columns)]
            for y in xrange(rows)
        ]

        coordinates[self.y()][self.x()] = self.COORDINATES[0][0]

        return coordinates

    def direction(self):
        print("[Bird][info] Getting Bird direction")

        return self.DIRECTION

    def x(self):
        print("[Bird][info] Getting Bird X position")

        return self.X

    def y(self):
        print("[Bird][info] Getting Bird Y position")

        return self.Y

    def position(self):
        print("[Bird][info] Getting Bird X,Y position")

        return (self.X, self.Y)

    def clear(self):
        print("[Bird][info] Clearing Bird")

        self.COORDINATES = None
        self.X = None
        self.Y = None
        self.DIRECTION = None

    def cleanup(self):
        print("[Bird][info] Bird clean up")

        self.clear()

    def __exit__(self):
        print("[Bird][info] Bird exit")

        self.cleanup()
