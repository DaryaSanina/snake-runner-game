import pygame
import os
import sys
from PIL import Image

DIRECTIONS = ["up", "left", "right"]


def load_image(name, color_key=None):
    fullname = os.path.abspath(os.path.join('snake-runner-game\\data', name))
    if not os.path.isfile(fullname):
        print(f"File '{fullname}' not found")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


def crop_image(image, left, top, right, bottom):
    rect = image.get_rect()
    pil_string_image = pygame.image.tostring(image, "RGBA", False)
    pil_image = Image.frombytes("RGBA", (rect.width, rect.height), pil_string_image)
    pil_image = pil_image.crop((left, top, right, bottom))
    pil_bytes_image = pil_image.tobytes()
    image = pygame.image.fromstring(pil_bytes_image, pil_image.size, pil_image.mode)
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


class Snake(pygame.sprite.Sprite):
    def __init__(self, velocity, *group):
        super(Snake, self).__init__(*group)
        self.velocity = velocity
        self.direction = DIRECTIONS[0]  # DIRECTIONS[0] = "up"
        self.column = 3

        self.animation_frame = 0
        self.image = load_image('textures\\snake\\snakeSlime.png')
        self.rect = self.image.get_rect()

    def turn_left(self, full_turned_snake_image):
        if self.direction == 'up':
            x = self.rect.x
            y = self.rect.y
            snake_length = self.rect.height
            snake_width = self.rect.width

            # Prepare the turning animation
            self.image = crop_image(full_turned_snake_image,
                                    0, 0, snake_width, snake_width)
            self.rect = self.image.get_rect()
            self.rect.x = x - snake_width
            self.rect.y = y

            self.direction = DIRECTIONS[1]  # DIRECTIONS[1] = "left"

    def turn_right(self, full_turned_snake_image):
        if self.direction == 'up' and self.column < 5:
            x = self.rect.x
            y = self.rect.y

            # Prepare the turning animation
            snake_length = self.rect.height
            snake_width = self.rect.width
            self.image = crop_image(full_turned_snake_image,
                                    snake_length - snake_width, 0, snake_length, snake_width)
            self.rect = self.image.get_rect()
            self.rect.x = x + snake_width
            self.rect.y = y
            self.direction = DIRECTIONS[2]  # DIRECTIONS[2] = "right"

    def turn_forward(self, full_snake_image):
        x = self.rect.x
        y = self.rect.y

        # Prepare the turning animation
        snake_length = self.rect.width
        snake_width = full_snake_image.get_width()
        self.image = crop_image(full_snake_image, 0, 0, snake_width, snake_width)
        self.rect = self.image.get_rect()
        if self.direction == 'left':
            self.rect.x = x
        elif self.direction == 'right':
            self.rect.x = x + snake_length - snake_width
        self.rect.y = y
        self.direction = DIRECTIONS[0]  # DIRECTIONS[0] = "up"

    def move_left(self, full_turned_snake_image, distance):
        x = self.rect.x
        y = self.rect.y
        snake_width = self.rect.width
        self.image = crop_image(full_turned_snake_image,
                                0, 0, snake_width + distance, snake_width)
        self.rect = self.image.get_rect()
        self.rect.x = round(x - distance)
        self.rect.y = y

    def move_right(self, full_turned_snake_image, distance):
        x = self.rect.x
        y = self.rect.y
        full_turned_snake_rect = full_turned_snake_image.get_rect()
        snake_width = self.rect.width
        snake_length = full_turned_snake_rect.width
        self.image = crop_image(full_turned_snake_image,
                                snake_length - snake_width - distance,
                                0, snake_length, snake_width)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def move_forward_after_turning(self, full_snake_image, distance):
        x = self.rect.x
        y = self.rect.y
        snake_length = self.rect.height
        snake_width = self.rect.width
        self.image = crop_image(full_snake_image, 0, 0, snake_width, snake_length + distance)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
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
