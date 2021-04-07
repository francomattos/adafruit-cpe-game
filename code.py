# Circuit Playground NeoPixel game
# Press button as fast as you can and race against someone pressing the opposite button
import time
import board
import neopixel
import digitalio

# Defines pixels object variable to set board color, defines brightness.
pixels = neopixel.NeoPixel(board.NEOPIXEL, 10, brightness=0.005, auto_write=False)

# Defines button variables and behavior
button_a = digitalio.DigitalInOut(board.BUTTON_A)
button_a.direction = digitalio.Direction.INPUT
button_a.pull = digitalio.Pull.DOWN

button_b = digitalio.DigitalInOut(board.BUTTON_B)
button_b.direction = digitalio.Direction.INPUT
button_b.pull = digitalio.Pull.DOWN

# Defines colors used and array which dictates the color progression.
OFF = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
MAGENTA = (255, 0, 255)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)

color_selection = [OFF, BLUE, CYAN, MAGENTA, RED, GREEN, YELLOW, WHITE]

# Indicator for starting game, all colors turn red for half a second and game starts.
def start_game():
    pixels.fill(RED)
    pixels.show()
    time.sleep(0.5)
    pixels.fill(OFF)
    pixels.show()

# Indicator for winning game.
# Winning side flashes three times with winning color, then game restarts.
def win_game(winning_side, COLOR):
    for _ in range(3):
        pixels[winning_side] = [COLOR] * 5
        pixels.show()
        time.sleep(1)
        pixels[winning_side] = [OFF] * 5
        pixels.show()
        time.sleep(1)

    start_game()
 
# Interates through the 5 neopixels on the side of button clicked
# Changes color based on its index on color_selection, when full goes to next pixel
# Once side is filled, lights up winning side with color choice
def a_click():
    for i in range(4, -1, -1):
        index = color_selection.index(pixels[i])

        if index < len(color_selection) - 1:
            index += 1
            pixels[i] = color_selection[index]
            pixels.show()
            break

        if i == 0: win_game(slice(0, 5), YELLOW)

def b_click():
    for i in range(5, 10, 1):
        index = color_selection.index(pixels[i])

        if index < len(color_selection) - 1:
            index += 1
            pixels[i] = color_selection[index]
            pixels.show()
            break

        if i == 9: win_game(slice(5, 10), BLUE)

start_game()

# Keeps track if button is pressed, prevents repetitive action if button held
a_button_pressed = True
b_button_pressed = True

while True:
    if button_a.value:
        if a_button_pressed: a_click()
        a_button_pressed = False
    else:
        a_button_pressed = True

    if button_b.value:
        if b_button_pressed == True: b_click()
        b_button_pressed = False
    else:
        b_button_pressed = True
        
    time.sleep(0.01)