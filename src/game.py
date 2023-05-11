import random
import max7219
import time
from machine import Pin, SPI, ADC

DISPLAY_WIDTH = 32
DISPLAY_HEIGHT = 8
FPS = 60
BALL_SPEED = 15
ELEMENT_DISPLAY_SIZE = 1

# Initialize pico
led = Pin(25, Pin.OUT)

yAxis = ADC(Pin(26))
button = Pin(17, Pin.IN, Pin.PULL_UP)

yAxis2 = ADC(Pin(28))
button2 = Pin(19, Pin.IN, Pin.PULL_UP)

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

    leftPaddleOffset = random.randrange(-2, 3)
    rightPaddleOffset = random.randrange(-2, 3)
    
    # Avoid symmetry
    if leftPaddleOffset == rightPaddleOffset:
        leftPaddleOffset += 1

    # Set initial positions
    game[height // 2][width // 2] = Element.BALL

    game[height // 2 - 1 + leftPaddleOffset][0] = Element.LEFT_PADDLE
    game[height // 2 + leftPaddleOffset][0] = Element.LEFT_PADDLE

    game[height // 2 - 1 + rightPaddleOffset][width - 1] = Element.RIGHT_PADDLE
    game[height // 2 + rightPaddleOffset][width - 1] = Element.RIGHT_PADDLE

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

def draw_score(leftScore, rightScore):
    display.fill(0)
    if leftScore < 10:
        display.text(str(leftScore), 8, 0, 1)
    else:
        display.text(str(leftScore), 0, 0, 1)
    display.text(str(rightScore), DISPLAY_WIDTH - 16, 0, 1)
    display.show()

def game_update_ball(game, current_directions, leftScore, rightScore):
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
    restartGame = False
    if ball_pos[0] == 0:
        rightScore += 1
        restartGame = True
    if ball_pos[0] == len(game[0]) - 1:
        leftScore += 1
        restartGame = True

    if restartGame:
        game = init_game(DISPLAY_WIDTH // ELEMENT_DISPLAY_SIZE,
                         DISPLAY_HEIGHT // ELEMENT_DISPLAY_SIZE)
        current_directions[0] = random.choice(
            [Direction.LEFT, Direction.RIGHT])
        current_directions[1] = random.choice(
            [Direction.UP, Direction.DOWN])
    else:
        game_move_ball(game, current_directions)

    return game, current_directions, leftScore, rightScore


def main():
    # Initialize pong game
    game = init_game(DISPLAY_WIDTH // ELEMENT_DISPLAY_SIZE,
                     DISPLAY_HEIGHT // ELEMENT_DISPLAY_SIZE)

    # Main loop
    running = True
    current_directions = [Direction.RIGHT, Direction.DOWN]
    counter = 0

    # Score variables
    leftScore = 0
    rightScore = 0
    showScore = False

    while running:

        if showScore:
            draw_score(leftScore, rightScore)
            showScore = False
            time.sleep(2)

        yValue = yAxis.read_u16()
        yValue2 = yAxis2.read_u16()
            
        # Update ball
        if counter % (FPS // BALL_SPEED) == 0:
            game, current_directions, newLeftScore, newRightScore = game_update_ball(
                game, current_directions, leftScore, rightScore)
            if newLeftScore != leftScore or newRightScore != rightScore:
                showScore = True
                leftScore = newLeftScore
                rightScore = newRightScore

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
