# -*- coding: utf-8 -*-
#############################################################
#                          IMPORTS                          #
#############################################################
import random
import time
import board
import displayio
import terminalio
import digitalio
from adafruit_debouncer import Debouncer
from adafruit_display_text import label
import adafruit_displayio_sh1107

#############################################################
#                          CONTENT                          #
#############################################################
## CLEARS THE DISPLAY
displayio.release_displays()

## SETUP BUTTON PINS
pin_a = digitalio.DigitalInOut(board.D9)
pin_a.direction = digitalio.Direction.INPUT
pin_a.pull = digitalio.Pull.UP

pin_b = digitalio.DigitalInOut(board.D6)
pin_b.direction = digitalio.Direction.INPUT
pin_b.pull = digitalio.Pull.UP

pin_c = digitalio.DigitalInOut(board.D5)
pin_c.direction = digitalio.Direction.INPUT
pin_c.pull = digitalio.Pull.UP

## DEBOUNCE BUTTONS
button_a = Debouncer(pin_a) #9
button_b = Debouncer(pin_b) #6
button_c = Debouncer(pin_c) #5

## I2C
i2c = board.I2C()
display_bus = displayio.I2CDisplay(i2c, device_address=0x3C)

## SH1107 OLED DISPLAY
WIDTH = 128
HEIGHT = 64

display = adafruit_displayio_sh1107.SH1107(display_bus, width=WIDTH, height=HEIGHT)

group = displayio.Group()
display.show(group)

button_bitmap = displayio.Bitmap(5, 5, 1)
# wifi_bitmap = displayio.OnDiskBitmap("/purple.bmp")

color_palette = displayio.Palette(1)
color_palette[0] = 0xFFFFFF  # White

button_sprite = displayio.TileGrid(button_bitmap, pixel_shader=color_palette, x=0, y=-10)
# wifi_sprite = displayio.TileGrid(wifi_bitmap, pixel_shader=wifi_bitmap.pixel_shader, x=0, y= 130)
group.append(button_sprite)
# group.append(wifi_sprite)

text = "LE FUTUR"
text_area = label.Label(terminalio.FONT, text=text, scale=2, color=0xFFFFFF, x=15, y=28)
group.append(text_area)
time.sleep(1)

# random.seed(0)
#############################################################
#                          FUNCTION                         #
#############################################################
def button(sprite_y, x, y, text):
    button_sprite.y = sprite_y
    text_area.scale = 5
    text_area.x = x
    text_area.y = y
    text_area.text = text

#############################################################
#                         MAIN LOOP                         #
#############################################################
while True:
    # Debounce buttons
    button_a.update()
    button_b.update()
    button_c.update()

    # Check for button presses & set text
    if button_a.fell:
        button(8, 26, 28, f"{random.choice(["OUI", "NON"])}")

    elif button_b.fell:
        button(28, 52, 28, f"{random.randint(1, 6)}")

    elif button_c.fell:
        button(47, 26, 28, f"{random.randint(1, 100):03}")

    display.show(group)
    