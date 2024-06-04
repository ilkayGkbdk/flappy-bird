import pygame.sprite

import assets
import configs
from layer import Layer


class GameStart(pygame.sprite.Sprite):
    def __init__(self, *groups):
        self._layer = Layer.UI
        self.image = assets.get_sprites("message")
        self.rect = self.image.get_rect(center=(configs.SCREEN_WIDTH / 2, configs.SCREEN_HEIGHT / 2))

        self.mask = pygame.mask.from_surface(self.image)

        super().__init__(*groups)
