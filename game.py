import pygame as pg
import random

DISPLAY_WIDTH = 1280
DISPLAY_HEIGHT = 400
FPS = 60
BALL_SPEED = 10
ELEMENT_DISPLAY_SIZE = 40


class Element:
    LEFT_PADDLE = 0
    RIGHT_PADDLE = 1
    BALL = 2
    EMPTY = 3


class Direction:
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3


def init_game(width, height):
    # Check if width and height are valid
    if width < 5 or width % 2 != 0 or width*ELEMENT_DISPLAY_SIZE > DISPLAY_WIDTH:
        raise ValueError(
            "Width must be an even number greater than 5; must not exceed display width")
    if height < 5 or height % 2 != 0 or height*ELEMENT_DISPLAY_SIZE > DISPLAY_HEIGHT:
        raise ValueError(
            "Height must be an even number greater than 5; must not exceed display height")

    # Create game matrix with empty elements
    game = []
    for _ in range(height):
        game.append([Element.EMPTY] * width)

    # Set initial positions
    game[height // 2][width // 2] = Element.BALL

    game[height // 2 - 1][0] = Element.LEFT_PADDLE
    game[height // 2][0] = Element.LEFT_PADDLE

    game[height // 2 - 1][width - 1] = Element.RIGHT_PADDLE
    game[height // 2][width - 1] = Element.RIGHT_PADDLE

    return game


def get_ball_position(game):
    # Get ball position
    ball_pos = None
    for y, row in enumerate(game):
        for x, element in enumerate(row):
            if element == Element.BALL:
                ball_pos = (x, y)
                break
        if ball_pos is not None:
            break

    # Check if ball position is valid
    if ball_pos is None:
        raise ValueError("Ball not found in game matrix")

    return ball_pos


def game_move_ball(game, directions):
    # Get ball position
    ball_pos = get_ball_position(game)

    # Move ball
    for direction in directions:
        if direction == Direction.UP:
            game[ball_pos[1]][ball_pos[0]] = Element.EMPTY
            game[ball_pos[1] - 1][ball_pos[0]] = Element.BALL
        elif direction == Direction.DOWN:
            game[ball_pos[1]][ball_pos[0]] = Element.EMPTY
            game[ball_pos[1] + 1][ball_pos[0]] = Element.BALL
        elif direction == Direction.LEFT:
            game[ball_pos[1]][ball_pos[0]] = Element.EMPTY
            game[ball_pos[1]][ball_pos[0] - 1] = Element.BALL
        elif direction == Direction.RIGHT:
            game[ball_pos[1]][ball_pos[0]] = Element.EMPTY
            game[ball_pos[1]][ball_pos[0] + 1] = Element.BALL
        ball_pos = get_ball_position(game)


def game_move_left_paddle(game, direction):
    # Get left paddle positions
    pos = []
    for y, row in enumerate(game):
        for x, element in enumerate(row):
            if element == Element.LEFT_PADDLE and pos == []:
                pos = (x, y)

    # Check if left paddle positions are valid
    if pos == []:
        raise ValueError("Left paddle not found in game matrix")

    # Check if left paddle is at top or bottom of screen
    if pos[1] == 0 and direction == Direction.UP:
        return
    if pos[1] == len(game) - 2 and direction == Direction.DOWN:
        return

    # Move left paddle
    if direction == Direction.UP:
        game[pos[1] + 1][pos[0]] = Element.EMPTY
        game[pos[1] - 1][pos[0]] = Element.LEFT_PADDLE
    elif direction == Direction.DOWN:
        game[pos[1]][pos[0]] = Element.EMPTY
        game[pos[1] + 2][pos[0]] = Element.LEFT_PADDLE


def game_move_right_paddle(game, direction):
    # Get right paddle positions
    pos = []
    for y, row in enumerate(game):
        for x, element in enumerate(row):
            if element == Element.RIGHT_PADDLE and pos == []:
                pos = (x, y)

    # Check if right paddle positions are valid
    if pos == []:
        raise ValueError("Right paddle not found in game matrix")

    # Check if right paddle is at top or bottom of screen
    if pos[1] == 0 and direction == Direction.UP:
        return
    if pos[1] == len(game) - 2 and direction == Direction.DOWN:
        return

    # Move right paddle
    if direction == Direction.UP:
        game[pos[1] + 1][pos[0]] = Element.EMPTY
        game[pos[1] - 1][pos[0]] = Element.RIGHT_PADDLE
    elif direction == Direction.DOWN:
        game[pos[1]][pos[0]] = Element.EMPTY
        game[pos[1] + 2][pos[0]] = Element.RIGHT_PADDLE


def draw_game(game, screen):
    # Draw game matrix
    for y, row in enumerate(game):
        for x, element in enumerate(row):
            if element == Element.LEFT_PADDLE:
                pg.draw.rect(screen, (255, 255, 255), (x * ELEMENT_DISPLAY_SIZE, y *
                             ELEMENT_DISPLAY_SIZE, ELEMENT_DISPLAY_SIZE, ELEMENT_DISPLAY_SIZE))
            elif element == Element.RIGHT_PADDLE:
                pg.draw.rect(screen, (255, 255, 255), (x * ELEMENT_DISPLAY_SIZE, y *
                             ELEMENT_DISPLAY_SIZE, ELEMENT_DISPLAY_SIZE, ELEMENT_DISPLAY_SIZE))
            elif element == Element.BALL:
                pg.draw.circle(screen, (255, 255, 255),
                               (x * ELEMENT_DISPLAY_SIZE + ELEMENT_DISPLAY_SIZE // 2, y * ELEMENT_DISPLAY_SIZE + ELEMENT_DISPLAY_SIZE // 2), ELEMENT_DISPLAY_SIZE // 2)


def game_update_ball(game, current_directions):
    ball_pos = get_ball_position(game)

    # Handle ball at top/bottom of screen
    if ball_pos[1] == 0:
        current_directions = [Direction.DOWN if x ==
                              Direction.UP else x for x in current_directions]
    elif ball_pos[1] == len(game) - 1:
        current_directions = [Direction.UP if x ==
                              Direction.DOWN else x for x in current_directions]

    # Handle ball at paddles
    if ball_pos[0] == 1:
        if game[ball_pos[1]][ball_pos[0] - 1] == Element.LEFT_PADDLE:
            current_directions = [Direction.RIGHT if x ==
                                  Direction.LEFT else x for x in current_directions]
            if game[ball_pos[1] - 1][ball_pos[0] - 1] == Element.LEFT_PADDLE:
                current_directions = [Direction.UP if x ==
                                      Direction.DOWN else x for x in current_directions]
            elif game[ball_pos[1] + 1][ball_pos[0] - 1] == Element.LEFT_PADDLE:
                current_directions = [Direction.DOWN if x ==
                                      Direction.UP else x for x in current_directions]
    elif ball_pos[0] == len(game[0]) - 2:
        if game[ball_pos[1]][ball_pos[0] + 1] == Element.RIGHT_PADDLE:
            current_directions = [Direction.LEFT if x ==
                                  Direction.RIGHT else x for x in current_directions]
            if game[ball_pos[1] - 1][ball_pos[0] + 1] == Element.RIGHT_PADDLE:
                current_directions = [Direction.UP if x ==
                                      Direction.DOWN else x for x in current_directions]
            elif game[ball_pos[1] + 1][ball_pos[0] + 1] == Element.RIGHT_PADDLE:
                current_directions = [Direction.DOWN if x ==
                                      Direction.UP else x for x in current_directions]

    # Move ball
    if ball_pos[0] == 0 or ball_pos[0] == len(game[0]) - 1:
        game = init_game(DISPLAY_WIDTH // ELEMENT_DISPLAY_SIZE,
                         DISPLAY_HEIGHT // ELEMENT_DISPLAY_SIZE)
        current_directions[0] = random.choice(
            [Direction.LEFT, Direction.RIGHT])
        current_directions[1] = random.choice(
            [Direction.UP, Direction.DOWN])
    else:
        game_move_ball(game, current_directions)

    return game, current_directions


def main():
    # Initialize pygame
    pg.init()
    screen = pg.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
    clock = pg.time.Clock()

    # Initialize pong game
    game = init_game(DISPLAY_WIDTH // ELEMENT_DISPLAY_SIZE,
                     DISPLAY_HEIGHT // ELEMENT_DISPLAY_SIZE)

    # Main loop
    running = True
    current_directions = [Direction.RIGHT, Direction.DOWN]
    counter = 0
    while running:
        counter += 1

        # Handle events
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_w:
                    game_move_left_paddle(game, Direction.UP)
                elif event.key == pg.K_s:
                    game_move_left_paddle(game, Direction.DOWN)
                elif event.key == pg.K_UP:
                    game_move_right_paddle(game, Direction.UP)
                elif event.key == pg.K_DOWN:
                    game_move_right_paddle(game, Direction.DOWN)

        # Update ball
        if counter % (FPS // BALL_SPEED) == 0:
            game, current_directions = game_update_ball(
                game, current_directions)

        # Draw game
        screen.fill((0, 0, 0))
        draw_game(game, screen)
        pg.display.flip()
        clock.tick(FPS)

    # Quit pygame
    pg.quit()


if __name__ == "__main__":
    main()
