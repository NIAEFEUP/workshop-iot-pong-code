## Theoretical part

The slides are available [here](https://workshop-pong-niaefeup.netlify.app/#1). 
The estimated duration is 30 minutes, so they can understand everything calmly.

## Required Components

1x Raspberry Pi Pico
5x LED Matrix 8x8
2x Joystick 
1x Micro-usb cable

## Software Requirements

- [Visual Studio Code](https://code.visualstudio.com/)
- [Python 3](https://www.python.org/downloads/)
- [MicroPico Extension](https://marketplace.visualstudio.com/items?itemName=paulober.pico-w-go)
- [Git](https://git-scm.com/downloads) (optional - you can download the repository as a zip file)

## Connecting the wires

If you need to rebuild the system, copy the [diagram.json](diagram.json) and paste it in the [simulation](https://wokwi.com/projects/new/pi-pico). You can follow all the ports you see there.

## Install the VSCode extension

To intereact with the Raspberry Pi Pico, you need to install the [MicroPico Extension](https://marketplace.visualstudio.com/items?itemName=paulober.pico-w-go) for Visual Studio Code.

Connect the Raspberry Pi Pico to your computer and check if the VSCode extension detects the device. If it doesn't, you need to flash the Pico.

## How to flash the Raspberry Pi Pico

Press the BOOTSEL button on the Raspberry Pi Pico and connect it to your computer. The Pico will appear as a USB mass storage device. Drag and drop the `RPI_PICO_FLASH.uf2` file to the device. The Pico will reboot and run the new code.

## How to run the code

Open the `game.py` file and press run on the VSCode footer. The code will be uploaded to the Raspberry Pi Pico and run.