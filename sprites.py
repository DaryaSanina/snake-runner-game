import pygame
import os
import sys


def load_image(name, color_key=None):
    fullname = os.path.abspath(os.path.join('snake-runner-game\\data', name))
    if not os.path.isfile(fullname):
        print(f"File '{fullname}' not found")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


class RoadPart(pygame.sprite.Sprite):
    def __init__(self, x, y, side, *group):
        super(RoadPart, self).__init__(*group)

        self.image = load_image('textures\\road\\Tiles\\tile_0029.png')
        self.image = pygame.transform.scale(self.image, (side, side))

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.rect.width = self.rect.height = side
    # TODO
    pass


class Snake(pygame.sprite.Sprite):
    def __init__(self, velocity, *group):
        super(Snake, self).__init__(*group)
        self.velocity = velocity

        self.image = load_image('textures\\snake\\snakeSlime.png')
        self.rect = self.image.get_rect()
    # TODO


class Monster(pygame.sprite.Sprite):
    def __init__(self, *group):
        super(Monster, self).__init__(*group)
    # TODO
    pass


class Apple(pygame.sprite.Sprite):
    def __init__(self, *group):
        super(Apple, self).__init__(*group)
    # TODO
    pass
