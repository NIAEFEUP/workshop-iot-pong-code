# use the diagram.json to run the simulation in https://wokwi.com

import max7219
from machine import Pin, SPI

spi = SPI(0, polarity=1, phase=0, sck=Pin(2), mosi=Pin(3))
cs = Pin(5, Pin.OUT)

display = max7219.Matrix8x8(spi, cs, 4)

player1Pos = 2
player2Pos = 4
playerWidth = 3
ballPos = (10, 3)

# clear display
display.fill(0)
display.show()

# Simulation matrix seems to be inverted for some reason...
display.vline(7, player1Pos, playerWidth, 1)
display.vline(24, player2Pos, playerWidth, 1)
display.pixel(ballPos[0], ballPos[1], 1)
display.show()
