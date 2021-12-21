import pygame
import pyautogui
import random

from sprites import RoadPart, Snake, load_image


def generate_road_part():
    if not road_parts.sprites():
        # Create first road part sprites that fill the whole length of the road
        first_road_parts = list()
        for y in range(-road_part_side + 1, round(screen_height), road_part_side):
            road_part = RoadPart(screen_width // 5 * 2, y, road_part_side)
            first_road_parts.append(road_part)
        for road_part in reversed(first_road_parts):
            road_parts.add(road_part)
    else:
        possible_x_positions = [0, screen_width // 5, screen_width // 5 * 2,
                                screen_width // 5 * 3, screen_width // 5 * 4]
        choice = random.choice(possible_x_positions)

        # Create a road part sprite
        road_part = RoadPart(choice, road_parts.sprites()[-1].rect.y - 2 * road_part_side,
                             road_part_side)

        road_parts.add(road_part)


def move_road():
    # If the road part sprite is under the bottom edge of the window, delete it
    if road_parts.sprites()[-1].rect.y >= screen_height:
        last_sprite = road_parts.sprites()[-1]
        road_parts.remove(last_sprite)

    cur_x = 0
    prev_x = 0

    # Move all the road part sprites down
    distance = snake.velocity * clock.tick(fps) / 1000
    for road_part in road_parts:
        road_part.rect.y += round(distance)

        # Create a connection between this and previous road part
        cur_x = int(road_part.rect.x)
        cur_y = int(road_part.rect.y)

        if road_part != road_parts.sprites()[0]:
            # If this is not the first road part:
            connection = pygame.sprite.Group()

            if cur_x == prev_x:
                connection_part = RoadPart(cur_x, cur_y + road_part_side, road_part_side)
                connection.add(connection_part)

            elif cur_x > prev_x:
                # Create the first part of the connection (a turn right)
                connection_start = RoadPart(prev_x, cur_y + road_part_side, road_part_side)
                connection_start.image = load_image('textures\\road\\Tiles\\tile_0027.png')
                connection_start.image = pygame.transform.scale(connection_start.image,
                                                               (road_part_side, road_part_side))
                connection.add(connection_start)

                # Create middle parts of the connection
                for connection_part_x in range(prev_x + road_part_side, cur_x, road_part_side):
                    connection_part = RoadPart(connection_part_x, cur_y + road_part_side,
                                               road_part_side)
                    connection_part.image = pygame.transform.rotate(connection_part.image, 90)
                    connection.add(connection_part)

                # Create the last part of the connection (a turn left)
                connection_end = RoadPart(cur_x, cur_y + road_part_side, road_part_side)
                connection_end.image = load_image('textures\\road\\Tiles\\tile_0027.png')
                connection_end.image = pygame.transform.rotate(connection_end.image, 180)
                connection_end.image = pygame.transform.scale(connection_end.image,
                                                              (road_part_side, road_part_side))
                connection.add(connection_end)

            elif cur_x < prev_x:
                # Create the first part of the connection (a turn left)
                connection_start = RoadPart(prev_x, cur_y + road_part_side, road_part_side)
                connection_start.image = load_image('textures\\road\\Tiles\\tile_0028.png')
                connection_start.image = pygame.transform.scale(connection_start.image,
                                                                (road_part_side, road_part_side))
                connection.add(connection_start)

                # Create middle parts of the connection
                for connection_part_x in range(cur_x + road_part_side, prev_x, road_part_side):
                    connection_part = RoadPart(connection_part_x, cur_y + road_part_side,
                                               road_part_side)
                    connection_part.image = pygame.transform.rotate(connection_part.image, -90)
                    connection.add(connection_part)

                # Create the last part of the connection (a turn left)
                connection_end = RoadPart(cur_x, cur_y + road_part_side, road_part_side)
                connection_end.image = load_image('textures\\road\\Tiles\\tile_0028.png')
                connection_end.image = pygame.transform.rotate(connection_end.image, 180)
                connection_end.image = pygame.transform.scale(connection_end.image,
                                                              (road_part_side, road_part_side))
                connection.add(connection_end)

            road_connections.append(connection)

        prev_x = int(road_part.rect.x)


if __name__ == '__main__':
    pygame.init()

    # Set the game screen width to 1/3 of the monitor's width resolution
    # and height to 2/3 of the monitor's height resolution
    screen_size = screen_width, screen_height \
        = pyautogui.size()[0] * (2 / 5), pyautogui.size()[1] * (4 / 5)
    screen = pygame.display.set_mode(screen_size)

    pygame.display.set_caption("Snake Runner")

    fps = 60
    road_part_side = int(screen_width // 5)

    snake_group = pygame.sprite.Group()
    snake = Snake(velocity=50)
    snake.rect.x = 2 * road_part_side + (road_part_side - snake.rect.width) // 2
    snake.rect.y = screen_height - snake.rect.height
    snake_group.add(snake)

    road_parts = pygame.sprite.Group()
    road_connections = list()

    grass_color = pygame.Color('#348C31')

    # Create clock to move the road more smoothly
    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.WINDOWCLOSE:
                running = False

        screen.fill(grass_color)

        if not road_parts.sprites() or road_parts.sprites()[-1].rect.y > 0:
            generate_road_part()

        move_road()
        road_parts.draw(screen)
        for connection in road_connections:
            connection.draw(screen)
        road_connections = list()

        snake_group.draw(screen)

        pygame.display.flip()

    pygame.quit()
