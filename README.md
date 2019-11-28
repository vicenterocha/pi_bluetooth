# Pi Bluetooth

This project was done so I can play music via bluetooth on my car, automatically and with physical buttons to control the tracks.

The raspberry pi sits on my car, hidden inside a compartiment between the two front seats. It is connected via a USB car charger and to a 3.5mm audio jack.

When the car is powered on, the raspberry receives power via the car charger and is automatically powered up. When it boots, it searches for the bluetooth address of my smartphone, and enters a loop trying to connect. When it does, it sends the play music command via bluetooth to my smartphone.

## Buttons Controller 

I also built a controller using pushbuttons and the GPIOs of rasperry. They allow me play/pause, previous and next. An extra and experimental button, when pressed twice ~~reads the name of the song outloud.~~ shuts the raspberry pie down.


![Controller](https://i.ibb.co/q7BX9Pn/image.png "Controller")


## TODO

[] Create a tutorial, because some files need to be modified and are not mentioned here.

[] Add a battery to the raspberry pie, so when it detects that it is being powered by it, instead of the power from the car, it shutsdown automatically.


## CREDITS

* https://www.raspberrypi.org/forums/viewtopic.php?t=161944
* https://ukbaz.github.io/howto/Bluetooth_speakers.html
* https://raspberrypihq.com/use-a-push-button-with-raspberry-pi-gpio/

and many more during troubleshooting..
