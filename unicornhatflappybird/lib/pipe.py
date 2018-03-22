from __future__ import print_function


class Pipe:
    COORDINATES = None

    X = None
    Y = None

    def __init__(self, coordinates, x=0, y=0):
        print("[Pipe][info] Initialising Pipe")

        self.COORDINATES = coordinates
        self.X = x
        self.Y = y

    def set_coordinates(self, coordinates):
        print("[Pipe][info] Setting Pipe coordinates")

        self.COORDINATES = coordinates

    def set_x(self, x):
        print("[Pipe][info] Setting Pipe X position")

        self.X = x

    def set_y(self, y):
        print("[Pipe][info] Setting Pipe Y position")

        self.Y = y

    def set_position(self, coordinates):
        print("[Pipe][info] Setting Pipe X, Y position")

        x, y = coordinates

        self.X = x
        self.Y = y

    def coordinates(self):
        print("[Pipe][info] Getting Pipe coordinates")

        return self.COORDINATES

    def x(self):
        print("[Pipe][info] Getting Pipe X position")

        return self.X

    def y(self):
        print("[Pipe][info] Getting Pipe Y position")

        return self.Y

    def position(self):
        print("[Pipe][info] Getting Pipe X, Y position")

        return (self.X, self.Y)

    def clear(self):
        print("[Pipe][info] Clearing Pipe")

        self.COORDINATES = None
        self.X = None
        self.Y = None

    def cleanup(self):
        print("[Pipe][info] Pipe clean up")

        self.clear()

    def __exit__(self):
        print("[Pipe][info] Pipe exit")

        self.cleanup()
