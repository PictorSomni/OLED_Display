import random
import time
import board
import displayio
import terminalio
import digitalio
from adafruit_debouncer import Debouncer
from adafruit_display_text import label
import adafruit_displayio_sh1107
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
import adafruit_ducky

displayio.release_displays()

# Set up button pins
pin_a = digitalio.DigitalInOut(board.D9)
pin_a.direction = digitalio.Direction.INPUT
pin_a.pull = digitalio.Pull.UP

pin_b = digitalio.DigitalInOut(board.D6)
pin_b.direction = digitalio.Direction.INPUT
pin_b.pull = digitalio.Pull.UP

pin_c = digitalio.DigitalInOut(board.D5)
pin_c.direction = digitalio.Direction.INPUT
pin_c.pull = digitalio.Pull.UP

button_a = Debouncer(pin_a) #9
button_b = Debouncer(pin_b) #6
button_c = Debouncer(pin_c) #5

# Use for I2C
i2c = board.I2C()
display_bus = displayio.I2CDisplay(i2c, device_address=0x3C)

## Keyboard
time.sleep(1)
keyboard = Keyboard(usb_hid.devices)
keyboard_layout = KeyboardLayoutUS(keyboard)

## DUCKY
duck = adafruit_ducky.Ducky("wifi_grabber_limited.txt", keyboard, keyboard_layout)

## SH1107 is vertically oriented 64x128
WIDTH = 128
HEIGHT = 64

display = adafruit_displayio_sh1107.SH1107(display_bus, width=WIDTH, height=HEIGHT)

## Make the display context
group = displayio.Group()
display.show(group)

button_bitmap = displayio.Bitmap(5, 5, 1)
color_palette = displayio.Palette(1)
color_palette[0] = 0xFFFFFF  # White

button_sprite = displayio.TileGrid(button_bitmap, pixel_shader=color_palette, x=0, y=-10)
group.append(button_sprite)

text = "LE FUTUR"
text_area = label.Label(terminalio.FONT, text=text, scale=2, color=0xFFFFFF, x=15, y=28)
group.append(text_area)
time.sleep(1)


while True:
    # Debounce buttons
    button_a.update()
    button_b.update()
    button_c.update()

    # Check for button presses & set text
    if button_a.fell:
        button_sprite.y = 10
        text_area.scale = 3
        text_area.x = 28
        text_area.y = 28
        text_area.text = "WiFi"

        result = True
        while result is not False:
            result = duck.loop()
        result = True

    elif button_b.fell:
        button_sprite.y = 28
        text_area.scale = 5
        text_area.x = 26
        text_area.y = 28
        text_area.text = f"{random.choice(["OUI", "NON"])}"

    elif button_c.fell:
        button_sprite.y = 48
        text_area.scale = 5
        text_area.x = 26
        text_area.y = 28
        text_area.text = f"{random.randint(1, 100):03}"

    display.show(group)
    