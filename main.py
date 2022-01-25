import random
import time
import board
import displayio
import terminalio
import digitalio
from adafruit_debouncer import Debouncer

# can try import bitmap_label below for alternative
from adafruit_display_text import label
import adafruit_displayio_sh1107

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

## SH1107 is vertically oriented 64x128
WIDTH = 128
HEIGHT = 64

display = adafruit_displayio_sh1107.SH1107(display_bus, width=WIDTH, height=HEIGHT)

## Make the display context
group = displayio.Group()
display.show(group)

color_bitmap = displayio.Bitmap(WIDTH, HEIGHT, 1)
color_palette = displayio.Palette(1)
color_palette[0] = 0xFFFFFF  # White

text = "LE FUTUR"
x =42 # START X POSITION
y = 30 # START Y POSITION
text_area = label.Label(terminalio.FONT, text=text, scale=1, color=0xFFFFFF, x=x, y=y)
group.append(text_area)
time.sleep(1)
min_x = 0
max_x = 80
min_y = 3
max_y = 58

## Random start direction
if random.random() > 0.5:
    horizontral_direction = 1
else:
    horizontral_direction = -1
if random.random() > 0.5:
    vertical_direction = 1
else:
    vertical_direction = -1


while True:
    # Debounce buttons
    button_a.update()
    button_b.update()
    button_c.update()

    # Check for button presses & set text
    if button_a.fell:
        text_area.scale = 1
        text_area.text = "SET TEXT"
        text_area.text = input("Set text : ")
        min_x = 0
        max_x = 96
        min_y = 3
        max_y = 58
    elif button_b.fell:
        text_area.text = f"{random.choice(["OUI", "NON"])}"
        text_area.scale = 2
        min_x = 0
        max_x = 93
        min_y = 6
        max_y = 53
    elif button_c.fell:
        text_area.text = f"{random.randint(1, 100):03}"
        text_area.scale = 2
        min_x = 0
        max_x = 93
        min_y = 6
        max_y = 53

    if (text_area.x <= min_x) or (text_area.x > max_x):
        horizontral_direction *= -1
        
    if (text_area.y <= min_y) or (text_area.y > max_y):
        vertical_direction *= -1

    text_area.x = text_area.x + horizontral_direction
    text_area.y = text_area.y + vertical_direction

    time.sleep(0.02)

    display.show(group)
    