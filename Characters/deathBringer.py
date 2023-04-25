import pygame
from Characters.playerDefault import Player

class deathBringer(Player):

    def __init__(self, x, y, platforms_group):
        """
        Constructor for the Player Class
        Param x: the starting x position
        Param y: the starting y position
        Param platforms_group: the platforms that check if the player is standing
        """
        super().__init__(x, y, platforms_group)
        image = pygame.image.load(r"images\characters\deathBringer\frontView.PNG").convert_alpha()
        self.image = pygame.Surface((60, 64))
        self.image = pygame.transform.scale(image, (int(image.get_width() * 0.5), int(image.get_height() * 0.5)))
        self.jump_speed = 200