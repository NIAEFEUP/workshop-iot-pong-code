import random
import max7219
import time
from machine import Pin, SPI, ADC

DISPLAY_WIDTH = 32
DISPLAY_HEIGHT = 8
FPS = 60
BALL_SPEED = 15
ELEMENT_DISPLAY_SIZE = 1

yAxis = ADC(Pin(26)) # Joystick 1
yAxis2 = ADC(Pin(28)) # Joystick 2

# Initialize LED matrix
spi = SPI(0, polarity=1, phase=0, sck=Pin(2), mosi=Pin(3))
cs = Pin(5, Pin.OUT)
display = max7219.Matrix8x8(spi, cs, 4)

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

    # Set the Ball
    game[height // 2][width // 2] = Element.BALL

    # Set the Players
    game[height // 2 - 1][0] = Element.LEFT_PADDLE
    game[height // 2][0] = Element.LEFT_PADDLE

    game[height // 2 - 1][width - 1] = Element.RIGHT_PADDLE
    game[height // 2][width - 1] = Element.RIGHT_PADDLE

    return game


def get_ball_position(game):
    ball_pos = None
    for y, row in enumerate(game):
        for x, element in enumerate(row):
            if element == Element.BALL:
                ball_pos = (x, y)
                break
        if ball_pos is not None:
            break
    return ball_pos if ball_pos != None else [0,0]


def game_move_ball(game, directions):
    ball_pos = get_ball_position(game)

    for direction in directions:
        game[ball_pos[1]][ball_pos[0]] = Element.EMPTY
        if direction == Direction.UP:
            game[ball_pos[1] - 1][ball_pos[0]] = Element.BALL
        elif direction == Direction.DOWN:
            game[ball_pos[1] + 1][ball_pos[0]] = Element.BALL
        elif direction == Direction.LEFT:
            game[ball_pos[1]][ball_pos[0] - 1] = Element.BALL
        elif direction == Direction.RIGHT:
            game[ball_pos[1]][ball_pos[0] + 1] = Element.BALL
        ball_pos = get_ball_position(game)


def game_move_paddle(game, direction, paddle):
    # Get paddle position
    pos = []
    for y, row in enumerate(game):
        for x, element in enumerate(row):
            if element == paddle and pos == []:
                pos = (x, y)

    # Check if paddle is at top or bottom of screen
    if pos[1] == 0 and direction == Direction.UP:
        return
    if pos[1] >= len(game) - 2 and direction == Direction.DOWN:
        return

    # Move paddle
    if direction == Direction.UP and game[pos[1] - 1][pos[0]] == Element.EMPTY:
        game[pos[1] + 1][pos[0]] = Element.EMPTY
        game[pos[1] - 1][pos[0]] = paddle
    elif direction == Direction.DOWN and game[pos[1] + 2][pos[0]] == Element.EMPTY:
        game[pos[1]][pos[0]] = Element.EMPTY
        game[pos[1] + 2][pos[0]] = paddle


def draw_game(game):
    # clear display
    display.fill(0)

    # draw game
    for y, row in enumerate(game):
        for x, element in enumerate(row):
            if element != Element.EMPTY:
                display.pixel(x, y, 1)

    display.show()


def game_update_ball(game, current_directions):
    ball_pos = get_ball_position(game)

    # Handle ball at top
    if ball_pos[1] == 0:
        current_directions = [current_directions[0], toogleDirection(current_directions[1])]
    # Handle ball at bottom
    elif ball_pos[1] == len(game) - 1:
        current_directions = [current_directions[0], toogleDirection(current_directions[1])]

    # Handle ball at paddles
    if ball_pos[0] == 1:
        if game[ball_pos[1]][ball_pos[0] - 1] == Element.LEFT_PADDLE:
            current_directions = [toogleDirection(current_directions[0]), current_directions[1]]
    elif ball_pos[0] == len(game[0]) - 2:
        if game[ball_pos[1]][ball_pos[0] + 1] == Element.RIGHT_PADDLE:
            current_directions = [toogleDirection(current_directions[0]), current_directions[1]]

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


def toogleDirection(direction):
    if(direction == Direction.UP):
        return Direction.DOWN
    elif(direction == Direction.DOWN):
        return Direction.UP
    elif(direction == Direction.LEFT):
        return Direction.RIGHT
    elif(direction == Direction.RIGHT):
        return Direction.LEFT


def main():
    # Initialize pong game
    game = init_game(DISPLAY_WIDTH // ELEMENT_DISPLAY_SIZE,
                     DISPLAY_HEIGHT // ELEMENT_DISPLAY_SIZE)

    # Main loop
    running = True
    current_directions = [Direction.RIGHT, Direction.DOWN]
    counter = 0
    while running:

        yValue = yAxis.read_u16()
        yValue2 = yAxis2.read_u16()
            
        # Update ball
        if counter % (FPS // BALL_SPEED) == 0:
            game, current_directions = game_update_ball(
                game, current_directions)
            counter = 0
            
        # Move paddles (numbers calibrated according to the joystick used)
        if counter % 2 == 0:
            if yValue <= 1000:
                game_move_paddle(game, Direction.DOWN, Element.LEFT_PADDLE)
            elif yValue >= 40000:
                game_move_paddle(game, Direction.UP, Element.LEFT_PADDLE)
            if yValue2 <= 1000:
                game_move_paddle(game, Direction.DOWN, Element.RIGHT_PADDLE)
            elif yValue2 >= 40000:
                game_move_paddle(game, Direction.UP, Element.RIGHT_PADDLE) 

        # Draw game
        draw_game(game)
        time.sleep(1 / FPS)
        counter += 1
        


if __name__ == "__main__":
    main()
