from __future__ import print_function
from lib.game import Game
import atexit
import config


def main():
    game = Game(
        config.game['switches'],
        config.game['columns'],
        config.game['rows'],
        config.game['fps'],
        config.game['countdown'],
        config.game['interval'],
        config.game['score_increment'],
        config.game['level_increment'],
        config.game['interval_increment'],
    )

    game.start()

    atexit.register(game.__exit__)


if __name__ == '__main__':
    main()
