import pygame
from Characters.playerDefault import Player

class blazeFist(Player):

    def __init__(self, x, y, platforms_group):
        """
        Constructor for the Player Class
        Param x: the starting x position
        Param y: the starting y position
        Param platforms_group: the platforms that check if the player is standing
        """
        super().__init__(x, y, platforms_group)
        self.imageLib = [r"images\characters\blazefist\leftView.PNG", r"images\characters\blazefist\frontView.PNG", r"images\characters\blazefist\rightView.PNG"]
        self.jump_speed = 200