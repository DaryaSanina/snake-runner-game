import pygame
import os
import sys
import random
from PIL import Image

SNAKE_DIRECTIONS = ["up", "left", "right"]
BUTTON_DIAMETER = 100


def load_image(name, color_key=None):
    fullname = os.path.abspath(os.path.join('snake-runner-game\\data', name))
    if not os.path.isfile(fullname):
        print(f"File '{fullname}' not found")
        sys.exit()
    image = pygame.image.load(fullname)
    image.set_colorkey(color_key)
    return image


def crop_image(image, left, top, right, bottom):
    rect = image.get_rect()
    pil_string_image = pygame.image.tostring(image, "RGBA", False)
    pil_image = Image.frombytes("RGBA", (rect.width, rect.height), pil_string_image)
    pil_image = pil_image.crop((left, top, right, bottom))
    pil_bytes_image = pil_image.tobytes()
    image = pygame.image.fromstring(pil_bytes_image, pil_image.size, pil_image.mode)
    return image


class Button(pygame.sprite.Sprite):
    def __init__(self, image: pygame.Surface, *group, size=(BUTTON_DIAMETER, BUTTON_DIAMETER)):
        super(Button, self).__init__(*group)
        self.image = image
        self.image = pygame.transform.scale(self.image, size)
        self.rect = self.image.get_rect()


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
        self.direction = SNAKE_DIRECTIONS[0]  # SNAKE_DIRECTIONS[0] = "up"

        self.animation_frame = 0
        self.image = load_image('textures\\snake\\snakeSlime.png')
        self.rect = self.image.get_rect()

    def turn_left(self, full_turned_snake_image):
        x = self.rect.x
        y = self.rect.y
        snake_width = self.rect.width

        # Prepare the tail turning animation

        # Prepare the head turning animation
        self.image = crop_image(full_turned_snake_image,
                                0, 0, snake_width, snake_width)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.direction = SNAKE_DIRECTIONS[1]  # SNAKE_DIRECTIONS[1] = "left"

    def turn_right(self, full_turned_snake_image):
        x = self.rect.x
        y = self.rect.y

        # Prepare the head turning animation
        snake_length = self.rect.height
        snake_width = self.rect.width
        self.image = crop_image(full_turned_snake_image,
                                snake_length - snake_width, 0, snake_length, snake_width)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.direction = SNAKE_DIRECTIONS[2]  # SNAKE_DIRECTIONS[2] = "right"

        # Prepare the tail turning animation

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
        self.direction = SNAKE_DIRECTIONS[0]  # DIRECTIONS[0] = "up"

    def move_left(self, full_turned_snake_image, distance):
        x = self.rect.x
        y = self.rect.y
        snake_width = self.rect.width
        snake_height = self.rect.height

        self.image = crop_image(full_turned_snake_image,
                                0, 0, snake_width + distance, snake_width)

        self.rect = self.image.get_rect()
        self.rect.x = round(x - distance)
        self.rect.y = y
        self.rect.height = snake_height

    def move_right(self, full_turned_snake_image, distance):
        x = self.rect.x
        y = self.rect.y
        full_turned_snake_rect = full_turned_snake_image.get_rect()
        snake_width = self.rect.width
        snake_length = full_turned_snake_rect.width
        snake_height = self.rect.height

        self.image = crop_image(full_turned_snake_image,
                                snake_length - snake_width - distance,
                                0, snake_length, snake_width)

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.rect.height = snake_height

    def move_forward_after_turning(self, full_snake_image, distance):
        x = self.rect.x
        y = self.rect.y
        snake_length = self.rect.height
        snake_width = self.rect.width

        self.image = crop_image(full_snake_image, 0, 0, snake_width, snake_length + distance)

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class SnakeTail(pygame.sprite.Sprite):
    def __init__(self, *group):
        super(SnakeTail, self).__init__(*group)
        self.image = load_image('textures\\snake\\snakeSlime.png')
        self.rect = self.image.get_rect()

        self.direction = SNAKE_DIRECTIONS[0]  # SNAKE_DIRECTIONS[0] = "up"

    def turn_left_or_right(self, full_snake_image, snake_x, snake_y):
        # Turn the snake's tail when the snake turns left or right
        y = self.rect.y
        self.image = full_snake_image
        self.rect = self.image.get_rect()
        self.rect.x = snake_x
        self.rect.y = snake_y

    def turn_forward(self, full_turned_snake_image, snake_x, snake_y, snake_width):
        # Turn the snake's tail when the snake turns forward
        full_snake_length = full_turned_snake_image.get_width()
        self.image = full_turned_snake_image
        self.rect = self.image.get_rect()
        if self.direction == 'left':
            self.rect.x = snake_x
        if self.direction == 'right':
            self.rect.x = snake_x + snake_width - full_snake_length
        self.rect.y = snake_y

    def move_left_or_right(self, full_snake_image, distance):
        # Move the snake's tail when the snake turns left or right
        x = self.rect.x
        y = self.rect.y
        tail_length = self.rect.height
        tail_width = self.rect.width
        full_snake_length = full_snake_image.get_height()

        self.image = crop_image(full_snake_image, 0,
                                round(full_snake_length - tail_length + distance), tail_width,
                                full_snake_length)

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def move_forward_after_turning(self, full_turned_snake_image, distance):
        # Move the snake's tail when the snake turns forward
        x = self.rect.x
        y = self.rect.y
        tail_length = self.rect.width
        tail_width = self.rect.height
        full_turned_snake_length = full_turned_snake_image.get_width()

        if self.direction == 'left':
            self.image = crop_image(full_turned_snake_image,
                                    full_turned_snake_length - tail_length + distance, 0,
                                    full_turned_snake_length, tail_width)

            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = round(y + distance)

        if self.direction == 'right':
            self.image = crop_image(full_turned_snake_image,
                                    0, 0, tail_length - distance,
                                    tail_width)

            self.rect = self.image.get_rect()
            self.rect.x = round(x + distance)
            self.rect.y = round(y + distance)


class SnakeHeadPoint(pygame.sprite.Sprite):
    def __init__(self, *group):
        super(SnakeHeadPoint, self).__init__(*group)
        self.rect = pygame.Rect(0, 0, 1, 1)

    def update(self, snake: Snake):
        if snake.direction == 'up':
            self.rect.x = snake.rect.x + snake.rect.width / 2
            self.rect.y = snake.rect.y
        if snake.direction == 'left':
            self.rect.x = snake.rect.x
            self.rect.y = snake.rect.y + snake.rect.height / 2
        if snake.direction == 'right':
            self.rect.x = snake.rect.x + snake.rect.width
            self.rect.y = snake.rect.y + snake.rect.height / 2


class Monster(pygame.sprite.Sprite):
    def __init__(self, *group):
        super(Monster, self).__init__(*group)

        possible_images = [load_image('textures\\monsters\\alienBeige.png'),
                           load_image('textures\\monsters\\alienBlue.png'),
                           load_image('textures\\monsters\\alienGreen.png'),
                           load_image('textures\\monsters\\alienPink.png'),
                           load_image('textures\\monsters\\alienYellow.png')]
        self.image = random.choice(possible_images)
        self.rect = self.image.get_rect()

    def attack_monster(self):
        self.kill()


class Apple(pygame.sprite.Sprite):
    def __init__(self, *group):
        super(Apple, self).__init__(*group)

        self.image = load_image('textures\\apple\\apple.png')
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()


class Booster(pygame.sprite.Sprite):
    def __init__(self, image, duration, *group):
        super(Booster, self).__init__(*group)

        self.image = pygame.transform.scale(image, (50, 50))
        self.rect = self.image.get_rect()

        self.duration = duration


class InsufficientApplesWindow(pygame.sprite.Sprite):
    def __init__(self, *group):
        super(InsufficientApplesWindow, self).__init__(*group)

        self.image = load_image('textures\\popups\\insufficient_apples_popup.png')
        self.rect = self.image.get_rect()
