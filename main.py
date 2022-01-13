import pygame
import pyautogui
import random
import sqlite3
import os

from sprites import (Button, RoadPart, Snake, SnakeTail, SnakeHeadPoint, Apple, Monster,
                     load_image, crop_image, SNAKE_DIRECTIONS)

GRASS_COLOR = pygame.Color('#348C31')
START_SCREEN_COLOR = pygame.Color('#348C31')
PAUSE_SCREEN_COLOR = pygame.Color(0, 162, 255, 150)
GAME_OVER_SCREEN_COLOR = pygame.Color(255, 0, 0, 128)
NEW_BEST_SCORE_SCREEN_COLOR = pygame.Color(255, 255, 0, 128)


def start_game() -> None:
    global running

    screen.fill(START_SCREEN_COLOR)  # Fill the screen with green color

    # Create a play button
    play_btn_group = pygame.sprite.Group()
    play_btn = Button(load_image('textures\\buttons\\start_btn.png'))
    play_btn.image = pygame.transform.scale(play_btn.image, (200, 200))
    play_btn.rect = play_btn.image.get_rect()
    play_btn.rect.x = (screen_width - play_btn.rect.width) // 2
    play_btn.rect.y = (screen_height - play_btn.rect.height) // 2
    play_btn_group.add(play_btn)

    play_btn_group.draw(screen)

    # Write "Snake Runner" on the screen
    snake_runner_font = pygame.font.SysFont('comicsansms', 90)
    snake_runner_text = snake_runner_font.render("SNAKE RUNNER", True, (255, 255, 0))
    snake_runner_text_x = (screen_width - snake_runner_text.get_width()) // 2
    snake_runner_text_y = (play_btn.rect.x - snake_runner_text.get_height()) // 2
    screen.blit(snake_runner_text, (snake_runner_text_x, snake_runner_text_y))

    # Display the maximal score
    best_score = get_max_score()
    best_score_font = pygame.font.SysFont('comicsansms', 75)
    best_score_text = best_score_font.render(f"BEST SCORE: {best_score}", True, (255, 255, 0))
    best_score_text_x = (screen_width - best_score_text.get_width()) // 2
    best_score_text_y = play_btn.rect.x + play_btn.rect.height \
        + (screen_height - (play_btn.rect.x + play_btn.rect.height)
           - best_score_text.get_height()) // 2
    screen.blit(best_score_text, (best_score_text_x, best_score_text_y))

    # Display the number of apples
    apples_font = pygame.font.SysFont('comicsansms', 75)
    apples_text = apples_font.render(f"APPLES: {apples}", True, (255, 255, 0))
    apples_text_x = (screen_width - apples_text.get_width()) // 2
    apples_text_y = best_score_text_y + best_score_text.get_height() + 25
    screen.blit(apples_text, (apples_text_x, apples_text_y))

    while running:
        while running:
            for event in pygame.event.get():
                if event.type == pygame.WINDOWCLOSE:
                    running = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()

                    if play_btn.rect.collidepoint(mouse_x, mouse_y):
                        restart_game()
                        return
            pygame.display.flip()


def pause_game() -> None:
    global running, clock

    # Delete the pause button
    pause_btn.kill()
    pygame.draw.rect(screen, GRASS_COLOR, pause_btn.rect)

    # Fill the screen with an RGBA color (red = 0, green = 162, blue = 255, alpha = 150)
    surface = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
    surface.fill(PAUSE_SCREEN_COLOR)
    screen.blit(surface, (0, 0))

    pause_screen_buttons = pygame.sprite.Group()

    # Create a restart button
    restart_btn = Button(load_image('textures\\buttons\\restart_btn.png'))
    restart_btn.rect.x = (screen_width - restart_btn.rect.width) // 2
    restart_btn.rect.y = (screen_height - restart_btn.rect.height) // 2
    pause_screen_buttons.add(restart_btn)

    # Create a resume button
    resume_btn = Button(load_image('textures\\buttons\\start_btn.png'))
    resume_btn.rect.x = (screen_width - resume_btn.rect.width) // 2
    resume_btn.rect.y = restart_btn.rect.y - 50 - resume_btn.rect.height
    pause_screen_buttons.add(resume_btn)

    # Create a home button
    home_btn = Button(load_image('textures\\buttons\\home_btn.png'))
    home_btn.rect.x = (screen_width - home_btn.rect.width) // 2
    home_btn.rect.y = restart_btn.rect.y + restart_btn.rect.height + 50
    pause_screen_buttons.add(home_btn)

    # Write "Pause" on the screen
    pause_font = pygame.font.SysFont('comicsansms', 100)
    pause_text = pause_font.render("PAUSE", True, (255, 255, 255))
    pause_text_x = (screen_width - pause_text.get_width()) // 2
    pause_text_y = (resume_btn.rect.x - pause_text.get_height()) // 2
    screen.blit(pause_text, (pause_text_x, pause_text_y))

    pause_screen_buttons.draw(screen)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.WINDOWCLOSE:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()

                if resume_btn.rect.collidepoint(mouse_x, mouse_y):
                    clock = pygame.time.Clock()  # Restart the clock
                    pause_btn_group.add(pause_btn)
                    return

                if restart_btn.rect.collidepoint(mouse_x, mouse_y):
                    restart_game()
                    return

                if home_btn.rect.collidepoint(mouse_x, mouse_y):
                    start_game()
                    return

        pygame.display.flip()


def restart_game() -> None:
    global pause_btn_group, pause_btn, snake_group, snake, full_turned_snake_image, \
        full_snake_image, snake_tail, snake_head_point, road_parts, road_connections, clock,\
        frames, score, apple_group, monster_group

    # Create a pause button
    pause_btn_group = pygame.sprite.Group()
    pause_btn = Button(load_image('textures\\buttons\\pause_btn.png'))
    pause_btn.rect.x = screen_width - pause_btn.rect.width - 10
    pause_btn.rect.y = 10
    pause_btn_group.add(pause_btn)

    snake_group = pygame.sprite.Group()

    snake = Snake(velocity=50)
    snake.rect.x = 2 * road_part_side + (road_part_side - snake.rect.width) // 2
    snake.rect.y = screen_height * 3 // 4

    full_turned_snake_image = None
    full_snake_image = load_image('textures\\snake\\snakeSlime.png')

    snake_tail = SnakeTail()
    snake_tail.rect.x = 2 * road_part_side + (road_part_side - snake_tail.rect.width) // 2
    snake_tail.rect.y = screen_height * 3 // 4

    snake_head_point = SnakeHeadPoint()
    snake_head_point.rect.x = snake.rect.x + snake.rect.width // 2
    snake_head_point.rect.y = snake.rect.y

    snake_group.add(snake)

    road_parts = pygame.sprite.Group()
    road_connections = list()

    apple_group = pygame.sprite.Group()
    monster_group = pygame.sprite.Group()

    score = 0

    # Create clock to move the road more smoothly
    clock = pygame.time.Clock()

    frames = 0


def end_game() -> None:
    global running

    # Change the snake's image to a dead snake
    snake_x = snake.rect.x
    snake_y = snake.rect.y

    snake.image = load_image('textures\\snake\\snakeSlime_dead.png')

    if snake.direction == 'up':
        snake.image = crop_image(snake.image, 0, 0, snake.rect.width, snake.rect.height)

    if snake.direction == 'left':
        snake.image = pygame.transform.rotate(snake.image, 90)
        snake.image = crop_image(snake.image, 0, 0, snake.rect.width, snake.rect.height)

    if snake.direction == 'right':
        snake.image = pygame.transform.rotate(snake.image, -90)
        snake.image = crop_image(snake.image, snake.image.get_width() - snake.rect.width, 0,
                                 snake.image.get_width(), snake.image.get_height())

    snake.rect = snake.image.get_rect()
    snake.rect.x = snake_x
    snake.rect.y = snake_y

    snake_group.draw(screen)

    # Delete the pause button
    pause_btn.kill()
    pygame.draw.rect(screen, GRASS_COLOR, pause_btn.rect)

    if score > get_max_score():
        end_game_new_best_score()
    else:
        end_game_game_over()

    add_score_to_database()
    update_database_apples()
    print(apples)

    game_over_screen_buttons = pygame.sprite.Group()

    # Display current score
    cur_score_font = pygame.font.SysFont('comicsansms', 80)
    cur_score_text = cur_score_font.render(f"SCORE: {score}", True, (255, 255, 255))
    cur_score_text_x = (screen_width - cur_score_text.get_width()) // 2
    cur_score_text_y = screen_height // 4 + (screen_height // 4 - cur_score_text.get_height()) // 2
    screen.blit(cur_score_text, (cur_score_text_x, cur_score_text_y))

    # Create a restart button
    restart_btn = Button(load_image('textures\\buttons\\restart_btn.png'))
    restart_btn.rect.x = (screen_width - restart_btn.rect.width) // 2
    restart_btn.rect.y = screen_height // 2 + (screen_height // 4 - restart_btn.rect.height) // 2
    game_over_screen_buttons.add(restart_btn)

    # Create a home button
    home_btn = Button(load_image('textures\\buttons\\home_btn.png'))
    home_btn.rect.x = (screen_width - home_btn.rect.width) // 2
    home_btn.rect.y = 3 * screen_height // 4 + (screen_height // 4 - restart_btn.rect.height) // 2
    game_over_screen_buttons.add(home_btn)

    game_over_screen_buttons.draw(screen)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.WINDOWCLOSE:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()

                if restart_btn.rect.collidepoint(mouse_x, mouse_y):
                    restart_game()
                    return

                if home_btn.rect.collidepoint(mouse_x, mouse_y):
                    start_game()
                    return

        pygame.display.flip()


def end_game_game_over() -> None:
    # Fill the screen with red color (alpha = 150)
    surface = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
    surface.fill(GAME_OVER_SCREEN_COLOR)
    screen.blit(surface, (0, 0))

    # Write "Game over" on the screen
    game_over_font = pygame.font.SysFont('comicsansms', 100)
    game_over_text = game_over_font.render("GAME OVER!", True, (255, 255, 255))
    game_over_text_x = (screen_width - game_over_text.get_width()) // 2
    game_over_text_y = (screen_height // 4 - game_over_text.get_height()) // 2
    screen.blit(game_over_text, (game_over_text_x, game_over_text_y))


def end_game_new_best_score() -> None:
    # Fill the screen with yellow color (alpha = 128)
    surface = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
    surface.fill(NEW_BEST_SCORE_SCREEN_COLOR)
    screen.blit(surface, (0, 0))

    # Write "New best score!" on the screen
    new_best_score_font = pygame.font.SysFont('comicsansms', 80)
    new_best_score_text = new_best_score_font.render("NEW BEST SCORE!", True, (255, 255, 255))
    new_best_score_text_x = (screen_width - new_best_score_text.get_width()) // 2
    new_best_score_text_y = (screen_height // 4 - new_best_score_text.get_height()) // 2
    screen.blit(new_best_score_text, (new_best_score_text_x, new_best_score_text_y))


def add_score_to_database() -> None:
    global score

    con = sqlite3.connect(os.path.abspath('snake-runner-game\\data\\databases\\user_data.db'))
    cur = con.cursor()

    cur.execute('INSERT INTO score VALUES (?)', (score,))
    con.commit()


def get_max_score():
    """
    :returns current maximal score from the database (int)
    """
    con = sqlite3.connect(os.path.abspath('snake-runner-game\\data\\databases\\user_data.db'))
    cur = con.cursor()

    all_scores = cur.execute('SELECT score FROM score').fetchall()

    if len(all_scores) == 0:
        return 0
    else:
        max_score = max(all_scores)
        return max_score[0]


def update_database_apples():
    con = sqlite3.connect(os.path.abspath('snake-runner-game\\data\\databases\\user_data.db'))
    cur = con.cursor()

    cur.execute('UPDATE apples SET apples = (?)', (apples,))
    con.commit()


def get_number_of_apples():
    con = sqlite3.connect(os.path.abspath('snake-runner-game\\data\\databases\\user_data.db'))
    cur = con.cursor()

    return cur.execute('SELECT apples FROM apples').fetchall()[0][0]


def generate_road_part() -> None:
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


def move_road(distance: int) -> None:
    # If the road part sprite is under the bottom edge of the window, delete it
    if road_parts.sprites()[-1].rect.y >= screen_height:
        last_sprite = road_parts.sprites()[-1]
        last_sprite.kill()

    cur_x = 0
    prev_x = 0

    # Move all the road part sprites down
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


def generate_apple():
    apple = Apple()

    left_road_part = min(road_connections[-1].sprites(), key=lambda road_part: road_part.rect.x)
    if road_parts.sprites()[-1].rect.y < left_road_part.rect.y:
        left_road_part = road_parts.sprites()[-1]

    right_road_part = max(road_connections[-1].sprites(), key=lambda road_part: road_part.rect.x)
    if road_parts.sprites()[-1].rect.y < right_road_part.rect.y:
        right_road_part = road_parts.sprites()[-1]

    apple.rect.x = random.randint(left_road_part.rect.x,
                                  right_road_part.rect.x + right_road_part.rect.width
                                  - apple.rect.width)
    apple.rect.y = (left_road_part.rect.y + apple.rect.height) // 2

    apple_group.add(apple)


def move_apples():
    for apple in apple_group.sprites():
        apple.rect.y += round(distance)
        if apple.rect.y > screen_height:
            apple.kill()


def generate_monster():
    monster = Monster()

    left_road_part = min(road_connections[-1].sprites(), key=lambda road_part: road_part.rect.x)
    if road_parts.sprites()[-1].rect.y < left_road_part.rect.y:
        left_road_part = road_parts.sprites()[-1]

    right_road_part = max(road_connections[-1].sprites(), key=lambda road_part: road_part.rect.x)
    if road_parts.sprites()[-1].rect.y < right_road_part.rect.y:
        right_road_part = road_parts.sprites()[-1]

    monster.rect.x = random.randint(left_road_part.rect.x,
                                    right_road_part.rect.x + right_road_part.rect.width
                                    - monster.rect.width)
    monster.rect.y = (left_road_part.rect.y + monster.rect.height) // 2

    monster_group.add(monster)


def move_monsters():
    for monster in monster_group.sprites():
        monster.rect.y += round(distance)
        if monster.rect.y > screen_height:
            monster.kill()


if __name__ == '__main__':
    pygame.init()

    # Set the game screen width to 1/3 of the monitor's width resolution
    # and height to 2/3 of the monitor's height resolution
    screen_size = screen_width, screen_height \
        = pyautogui.size()[0] * (2 / 5), pyautogui.size()[1] * (4 / 5)
    screen = pygame.display.set_mode(screen_size)

    pygame.display.set_caption("Snake Runner")

    # Create a pause button
    pause_btn_group = pygame.sprite.Group()
    pause_btn = Button(load_image('textures\\buttons\\pause_btn.png'))
    pause_btn.rect.x = screen_width - pause_btn.rect.width - 10
    pause_btn.rect.y = 10
    pause_btn_group.add(pause_btn)

    road_part_side = int(screen_width // 5)

    snake_group = pygame.sprite.Group()

    snake = Snake(velocity=50)
    snake.rect.x = 2 * road_part_side + (road_part_side - snake.rect.width) // 2
    snake.rect.y = screen_height * 3 // 4

    full_turned_snake_image = None
    full_snake_image = load_image('textures\\snake\\snakeSlime.png')

    snake_tail = SnakeTail()
    snake_tail.rect.x = 2 * road_part_side + (road_part_side - snake_tail.rect.width) // 2
    snake_tail.rect.y = screen_height * 3 // 4

    snake_head_point = SnakeHeadPoint()
    snake_head_point.rect.x = snake.rect.x + snake.rect.width // 2
    snake_head_point.rect.y = snake.rect.y

    snake_group.add(snake)

    road_parts = pygame.sprite.Group()
    road_connections = list()

    apple_group = pygame.sprite.Group()
    monster_group = pygame.sprite.Group()

    score = 0
    apples = get_number_of_apples()

    # Create clock to move the road more smoothly
    clock = pygame.time.Clock()

    frames = 0
    fps = 60

    running = True
    start_game()
    while running:
        tick = clock.tick(fps)
        for event in pygame.event.get():
            if event.type == pygame.WINDOWCLOSE:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if pause_btn.rect.collidepoint(mouse_x, mouse_y):
                    pause_game()

            if event.type == pygame.KEYDOWN:
                if (event.key == pygame.K_LEFT or event.key == pygame.K_a) \
                        and snake.direction == 'up':
                    # The user has pressed the left arrow on the keyboard:
                    if snake.animation_frame == 0:
                        full_turned_snake_image = pygame.transform.rotate(
                            load_image('textures\\snake\\snakeSlime.png'), 90)
                    else:
                        full_turned_snake_image = pygame.transform.rotate(
                            load_image('textures\\snake\\snakeSlime_ani.png'), 90)

                    snake.turn_left(full_turned_snake_image)

                    snake_tail.turn_left_or_right(full_snake_image,
                                                  snake_x=snake.rect.x, snake_y=snake.rect.y)
                    snake_tail.direction = SNAKE_DIRECTIONS[1]  # SNAKE_DIRECTIONS[1] = "left"

                    # Add the snake's tail
                    snake.kill()
                    snake_group.add(snake_tail)
                    snake_group.add(snake)

                if (event.key == pygame.K_RIGHT or event.key == pygame.K_d) \
                        and snake.direction == 'up':
                    # The user has pressed the right arrow on the keyboard:
                    if snake.animation_frame == 0:
                        full_turned_snake_image = pygame.transform.rotate(
                            load_image('textures\\snake\\snakeSlime.png'), -90)
                    else:
                        full_turned_snake_image = pygame.transform.rotate(
                            load_image('textures\\snake\\snakeSlime_ani.png'), -90)

                    snake.turn_right(full_turned_snake_image)

                    snake_tail.turn_left_or_right(full_snake_image,
                                                  snake_x=snake.rect.x, snake_y=snake.rect.y)
                    snake_tail.direction = SNAKE_DIRECTIONS[2]  # SNAKE_DIRECTIONS[2] = "right"

                    # Add the snake's tail
                    snake.kill()
                    snake_group.add(snake_tail)
                    snake_group.add(snake)

                if (event.key == pygame.K_UP or event.key == pygame.K_w) \
                        and (snake.direction == 'left' or snake.direction == 'right'):
                    # The user has pressed the up arrow on the keyboard
                    # and the snake is turned left or right:
                    snake.turn_forward(full_snake_image)

                    snake_tail.turn_forward(full_turned_snake_image,
                                            snake_x=snake.rect.x, snake_y=snake.rect.y,
                                            snake_width=snake.rect.width)

                    # Add the snake's tail
                    snake.kill()
                    snake_group.add(snake_tail)
                    snake_group.add(snake)

                    # Update the clock
                    clock = pygame.time.Clock()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()

                for monster in monster_group.sprites():
                    if monster.rect.collidepoint(mouse_x, mouse_y):
                        # If the user click on a monster
                        monster.attack_monster()

        if snake.direction == "up":
            # Generate and move the road
            distance = tick * snake.velocity / 1000
            screen.fill(GRASS_COLOR)
            if not road_parts.sprites() or road_parts.sprites()[-1].rect.y > 0:
                generate_road_part()

            move_road(distance=distance)
            road_parts.draw(screen)
            for connection in road_connections:
                connection.draw(screen)

            # If current score >= 1000, generate or not generate an apple
            if score >= 1000:
                if random.randint(0, 100) == 0:
                    generate_apple()

            move_apples()

            # If current score >= 1500, generate or not generate a monster
            if score >= 1500:
                if random.randint(0, 200) == 0:
                    generate_monster()

            move_monsters()

            # If the snake touches an apple, this apple disappears
            for apple in apple_group.sprites():
                if pygame.sprite.collide_mask(snake, apple):
                    apples += 1
                    apple.kill()

            # Snake animation
            if frames % 10 == 0:
                snake_x = snake.rect.x
                snake_width = snake.rect.width
                snake_length = snake.rect.height

                if snake.animation_frame == 0:
                    snake.animation_frame = 1

                    full_snake_image = load_image('textures\\snake\\snakeSlime_ani.png')
                    snake.image = crop_image(full_snake_image, 0, 0, snake_width, snake_length)

                    snake.rect = snake.image.get_rect()
                    snake.rect.x = snake_x
                    snake.rect.y = screen_height * 3 // 4
                else:
                    snake.animation_frame = 0

                    full_snake_image = load_image('textures\\snake\\snakeSlime.png')
                    snake.image = crop_image(full_snake_image, 0, 0, snake_width, snake_length)

                    snake.rect = snake.image.get_rect()
                    snake.rect.x = snake_x
                    snake.rect.y = screen_height * 3 // 4

            # If the snake is fully turned forward:
            if snake_tail.rect.height == snake_tail.rect.width \
                    or snake_tail.rect.y >= screen_height:
                snake_tail.direction = SNAKE_DIRECTIONS[0]  # SNAKE_DIRECTIONS[0] = "up"
                snake_tail.kill()

            elif full_turned_snake_image is not None:
                # Move the snake's tail
                snake_tail.move_forward_after_turning(full_turned_snake_image, distance=distance)

                # Snake's tail animation
                if frames % 10 == 0:
                    x = snake_tail.rect.x
                    y = snake_tail.rect.y
                    snake_tail_width = snake_tail.rect.height
                    snake_tail_length = snake_tail.rect.width

                    if snake.animation_frame == 0:
                        if snake_tail.direction == 'left':
                            full_turned_snake_image = pygame.transform.rotate(
                                load_image('textures\\snake\\snakeSlime.png'), 90)
                            full_turned_snake_length = full_turned_snake_image.get_width()
                            snake_tail.image = crop_image(full_turned_snake_image,
                                                          full_turned_snake_length
                                                          - snake_tail_length,
                                                          0, full_turned_snake_length,
                                                          snake_tail_width)
                        if snake_tail.direction == 'right':
                            full_turned_snake_image = pygame.transform.rotate(
                                load_image('textures\\snake\\snakeSlime.png'), -90)
                            snake_tail.image = crop_image(full_turned_snake_image,
                                                          0, 0, snake_tail_length,
                                                          snake_tail_width)
                    if snake.animation_frame == 1:
                        if snake_tail.direction == 'left':
                            full_turned_snake_image = pygame.transform.rotate(
                                load_image('textures\\snake\\snakeSlime_ani.png'), 90)
                            full_turned_snake_length = full_turned_snake_image.get_width()
                            snake_tail.image = crop_image(full_turned_snake_image,
                                                          full_turned_snake_length
                                                          - snake_tail_length,
                                                          0, full_turned_snake_length,
                                                          snake_tail_width)
                        if snake_tail.direction == 'right':
                            full_turned_snake_image = pygame.transform.rotate(
                                load_image('textures\\snake\\snakeSlime_ani.png'), -90)
                            snake_tail.image = crop_image(full_turned_snake_image,
                                                          0, 0, snake_tail_length,
                                                          snake_tail_width)

                    snake_tail.rect = snake_tail.image.get_rect()
                    snake_tail.rect.x = x
                    snake_tail.rect.y = y

                # Move the snake forward
                snake.move_forward_after_turning(full_snake_image,
                                                 distance=distance)

        if snake.direction == 'left':
            snake_moving_distance = tick * snake.velocity / 1000

            # Draw grass and the road
            screen.fill(GRASS_COLOR)
            move_road(distance=0)
            road_parts.draw(screen)
            for connection in road_connections:
                connection.draw(screen)

            # Move the snake's tail
            if snake_tail.rect.height > snake_tail.rect.width:
                snake_tail.move_left_or_right(full_snake_image, distance=snake_moving_distance)
            else:
                snake_tail.kill()

            # Move the snake
            snake.move_left(full_turned_snake_image,
                            distance=snake_moving_distance)

            # Snake and snake's tail animation
            if frames % 10 == 0:
                snake_x = snake.rect.x
                snake_y = snake.rect.y
                snake_length = snake.rect.width
                snake_width = snake.rect.height

                snake_tail_x = snake_tail.rect.x
                snake_tail_y = snake_tail.rect.y
                snake_tail_length = snake_tail.rect.height

                if snake.animation_frame == 0:
                    snake.animation_frame = 1

                    # Change the snake image
                    full_turned_snake_image = pygame.transform.rotate(
                        load_image('textures\\snake\\snakeSlime_ani.png'), 90)
                    snake.image = crop_image(full_turned_snake_image, 0, 0,
                                             snake_length, snake_width)

                    snake.rect = snake.image.get_rect()
                    snake.rect.x = snake_x
                    snake.rect.y = snake_y

                    # Change the snake's tail image
                    full_snake_image = load_image('textures\\snake\\snakeSlime_ani.png')
                    snake_tail.image = crop_image(full_snake_image,
                                                  0, 0, snake_width, snake_tail_length)

                    snake_tail.rect = snake_tail.image.get_rect()
                    snake_tail.rect.x = snake_tail_x
                    snake_tail.rect.y = snake_tail_y

                else:
                    snake.animation_frame = 0

                    # Change the snake image
                    full_turned_snake_image = pygame.transform.rotate(
                        load_image('textures\\snake\\snakeSlime.png'), 90)
                    snake.image = crop_image(full_turned_snake_image, 0, 0,
                                             snake_length, snake_width)

                    snake.rect = snake.image.get_rect()
                    snake.rect.x = snake_x
                    snake.rect.y = snake_y

                    # Change the snake's tail image
                    full_snake_image = load_image('textures\\snake\\snakeSlime.png')
                    snake_tail.image = crop_image(full_snake_image,
                                                  0, 0, snake_width, snake_tail_length)

                    snake_tail.rect = snake_tail.image.get_rect()
                    snake_tail.rect.x = snake_tail_x
                    snake_tail.rect.y = snake_tail_y

        if snake.direction == 'right':
            snake_moving_distance = tick * snake.velocity / 1000

            # Draw grass and the road
            screen.fill(GRASS_COLOR)
            move_road(distance=0)
            road_parts.draw(screen)
            for connection in road_connections:
                connection.draw(screen)

            # Move the snake's tail
            if snake_tail.rect.height > snake_tail.rect.width:
                snake_tail.move_left_or_right(full_snake_image, distance=snake_moving_distance)
            else:
                snake_tail.kill()

            # Move the snake
            snake.move_right(full_turned_snake_image,
                             distance=snake_moving_distance)

            # Snake and snake's tail animation
            if frames % 10 == 0:
                snake_x = snake.rect.x
                snake_y = snake.rect.y
                snake_length = snake.rect.width
                snake_width = snake.rect.height

                snake_tail_x = snake_tail.rect.x
                snake_tail_y = snake_tail.rect.y
                snake_tail_length = snake_tail.rect.height

                if snake.animation_frame == 0:
                    snake.animation_frame = 1

                    # Change the snake image
                    full_turned_snake_image = pygame.transform.rotate(
                        load_image('textures\\snake\\snakeSlime_ani.png'), -90)
                    full_turned_snake_length = full_turned_snake_image.get_width()
                    snake.image = crop_image(full_turned_snake_image,
                                             full_turned_snake_length - snake_length, 0,
                                             full_turned_snake_length, snake_width)

                    snake.rect = snake.image.get_rect()
                    snake.rect.x = snake_x
                    snake.rect.y = snake_y

                    # Change the snake's tail image
                    full_snake_image = load_image('textures\\snake\\snakeSlime_ani.png')
                    snake_tail.image = crop_image(full_snake_image,
                                                  0, 0, snake_width, snake_tail_length)

                    snake_tail.rect = snake_tail.image.get_rect()
                    snake_tail.rect.x = snake_tail_x
                    snake_tail.rect.y = snake_tail_y

                else:
                    snake.animation_frame = 0

                    # Change the snake image
                    full_turned_snake_image = pygame.transform.rotate(
                        load_image('textures\\snake\\snakeSlime.png'), -90)
                    full_turned_snake_length = full_turned_snake_image.get_width()
                    snake.image = crop_image(full_turned_snake_image,
                                             full_turned_snake_length - snake_length, 0,
                                             full_turned_snake_length, snake_width)

                    snake.rect = snake.image.get_rect()
                    snake.rect.x = snake_x
                    snake.rect.y = snake_y

                    # Change the snake's tail image
                    full_snake_image = load_image('textures\\snake\\snakeSlime.png')
                    snake_tail.image = crop_image(full_snake_image,
                                                  0, 0, snake_width, snake_tail_length)

                    snake_tail.rect = snake_tail.image.get_rect()
                    snake_tail.rect.x = snake_tail_x
                    snake_tail.rect.y = snake_tail_y

        snake_head_point.update(snake)  # Move the snake's head point
        snake_group.draw(screen)  # Draw the snake
        apple_group.draw(screen)  # Draw apples
        monster_group.draw(screen)  # Draw monsters
        pause_btn_group.draw(screen)  # Draw the pause button

        # Display the score
        score_font = pygame.font.SysFont('comicsansms', 90)
        score_text = score_font.render(str(int(score)), True, (255, 255, 255))
        score_text_x = 10
        score_text_y = 10
        screen.blit(score_text, (score_text_x, score_text_y))

        # If the snake is not on the road, exit the program
        if not pygame.sprite.spritecollideany(snake_head_point, road_parts) \
                and not any([pygame.sprite.spritecollideany(snake_head_point, connection)
                             for connection in road_connections]):
            end_game()

        pygame.display.flip()
        frames = (frames + 1) % 10 ** 9

        road_connections = list()
        snake.velocity += 0.1
        score += 1

    pygame.quit()
