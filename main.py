import pygame
import pyautogui
import random


class Snake:
    def __init__(self, velocity):
        self.velocity = velocity
    # TODO


class Monster:
    # TODO
    pass


class Apple:
    # TODO
    pass


def generate_road_part():
    if not road_part_coords:
        road_part_coords.append([screen_width // 5 * 2, screen_height - road_part_height])
    else:
        possible_x_positions = [0, screen_width // 5, screen_width // 5 * 2,
                                screen_width // 5 * 3, screen_width // 5 * 4]
        choice = random.choice(possible_x_positions)

        road_part_coords.append([choice, road_part_coords[-1][1] - road_part_height])
    road_part_widths.append(screen_width // 5)


def draw_road():
    if road_part_coords[-1][1] >= screen_height:
        road_part_coords.pop()

    distance = snake.velocity * clock.tick() / 1000
    for i in range(len(road_part_coords)):
        # Change the y coordinate of the part of the road
        road_part_coords[i][1] += distance
        cur_x = road_part_coords[i][0]
        cur_y = road_part_coords[i][1]

        # Draw the part of the road
        pygame.draw.rect(screen, road_color,
                         (cur_x, cur_y, road_part_widths[i], road_part_height))

        # Draw the connection of the parts
        if i > 0:
            prev_x = road_part_coords[i - 1][0]
            if cur_x > prev_x:
                pygame.draw.rect(screen, road_color,
                                 (prev_x, cur_y, cur_x - prev_x, road_part_height))
            elif cur_x < prev_x:
                pygame.draw.rect(screen, road_color,
                                 (cur_x + road_part_height, cur_y, prev_x - cur_x, road_part_height))


if __name__ == '__main__':
    pygame.init()

    # Set the game screen width to 1/3 of the monitor's width resolution
    # and height to 2/3 of the monitor's height resolution
    screen_size = screen_width, screen_height \
        = pyautogui.size()[0] * (2 / 5), pyautogui.size()[1] * (4 / 5)
    screen = pygame.display.set_mode(screen_size)

    pygame.display.set_caption("Snake Runner")

    snake = Snake(velocity=100)
    road_part_coords = list()
    road_part_widths = list()
    road_part_height = screen_width // 5

    grass_color = pygame.Color('#348C31')
    road_color = pygame.Color('#C2B280')

    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.WINDOWCLOSE:
                running = False

        screen.fill(grass_color)

        if not road_part_coords or road_part_coords[-1][1] > 0:
            generate_road_part()

        draw_road()

        pygame.display.flip()

    pygame.quit()
