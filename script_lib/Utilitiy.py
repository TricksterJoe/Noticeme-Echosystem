import time


class Utility:
    def __init__(self, Game):
        self.__g = Game

    def PlayerBetweenX(self, x1, x2):
        x_player, _ = self.__g.get_player_location()
        high = x1 if x1 >= x2 else x2
        low = x1 if x1 < x2 else x2

        return low <= x_player <= high

    def PlayerBetweenY(self, y1, y2):
        _, y_player = self.__g.get_player_location()
        high = y1 if y1 >= y2 else y2
        low = y1 if y1 < y2 else y2

        return low <= y_player <= high
