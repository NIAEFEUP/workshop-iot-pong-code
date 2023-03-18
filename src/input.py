from machine import Pin, ADC
import time

xAxis = ADC(Pin(27))
yAxis = ADC(Pin(26))
button = Pin(17,Pin.IN, Pin.PULL_UP) # probably useless
led = Pin(25, Pin.OUT)

print("Reading joystick input...")

# From what I've tested, these values work well
while True:
    xValue = xAxis.read_u16()
    yValue = yAxis.read_u16()
    buttonValue = button.value()

    if buttonValue == 0:
        print("Middle pressed")
        led.value(1)
    else:
        led.value(0)
        
    if xValue <= 600:
        print("Going right")  
    elif xValue >= 60000:
        print("Going left")
        
    if yValue <= 600:
        print("Going down")
    elif yValue >= 60000:
        print("Going up")

    time.sleep(0.2)
