import time
import random
import board
import busio
import digitalio
import neopixel
import adafruit_ssd1306
from adafruit_adxl34x import ADXL345

print("DEBUG: game code loaded")
NUM_PIXELS = 15
pixels = neopixel.NeoPixel(board.D3, 15, brightness=0.3, auto_write=False)
pixels.fill((255,0,255))
pixels.show()
time.sleep(1)
pixels.fill((0,0,0))
pixels.show()
print("DEBUG: pixel init done")

# ============================================================
#  OLED: SSD1306 128x64
# ============================================================

i2c = busio.I2C(board.D9, board.D8)   # SCL=D9, SDA=D8
oled = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c, addr=0x3C)

oled.fill(0)
oled.show()

# ----------------- built-in 5×8 pixel font ------------------

FONT = {
    "A":[124,18,17,18,124],
    "B":[127,73,73,73,54],
    "C":[62,65,65,65,34],
    "D":[127,65,65,34,28],
    "E":[127,73,73,73,65],
    "G":[62,65,73,73,58],
    "H":[127,8,8,8,127],
    "I":[0,65,127,65,0],
    "L":[127,64,64,64,64],
    "M":[127,2,4,2,127],
    "N":[127,4,8,16,127],
    "O":[62,65,65,65,62],
    "P":[127,9,9,9,6],
    "R":[127,9,25,41,70],
    "S":[38,73,73,73,50],
    "T":[1,1,127,1,1],
    "U":[63,64,64,64,63],
    "V":[31,32,64,32,31],
    "W":[127,32,24,32,127],
    "Y":[7,8,120,8,7],
    "0":[62,81,73,69,62],
    "1":[0,66,127,64,0],
    "2":[98,81,73,73,70],
    "3":[34,65,73,73,54],
    "4":[24,20,18,127,16],
    "5":[39,69,69,69,57],
    "6":[60,74,73,73,48],
    "7":[1,113,9,5,3],
    "8":[54,73,73,73,54],
    "9":[6,9,73,41,30],
    " ":[0,0,0,0,0],
    ">":[8,16,32,16,8]
}

def draw_char(x, y, ch):
    patt = FONT.get(ch, FONT[" "])
    for col in range(5):
        line = patt[col]
        for row in range(8):
            if line & (1 << row):
                oled.pixel(x + col, y + row, 1)

def draw_text(x, y, msg):
    for i, c in enumerate(msg):
        draw_char(x + i*6, y, c)

def oled_print(line1, line2=""):
    oled.fill(0)
    draw_text(0, 8, line1)
    if line2:
        draw_text(0, 28, line2)
    oled.show()


# ============================================================
#  ACCELEROMETER
# ============================================================

accel = ADXL345(i2c)

def get_tilt():
    x, y, z = accel.acceleration
    if x > 5: return "RIGHT"
    if x < -5: return "LEFT"
    if y > 5: return "UP"
    if y < -5: return "DOWN"
    return None


# ============================================================
#  ROTARY ENCODER
# ============================================================

clk = digitalio.DigitalInOut(board.D1)
clk.switch_to_input(pull=digitalio.Pull.UP)

dt = digitalio.DigitalInOut(board.D2)
dt.switch_to_input(pull=digitalio.Pull.UP)

# SW BUTTON now on D0
enc_button = digitalio.DigitalInOut(board.D0)
enc_button.switch_to_input(pull=digitalio.Pull.UP)

last_clk = clk.value
enc_pos = 0

def read_encoder():
    global last_clk, enc_pos
    now = clk.value
    if now != last_clk:  # edge
        if dt.value != now:
            enc_pos += 1
        else:
            enc_pos -= 1
    last_clk = now
    return enc_pos


# ============================================================
#  BONUS SWITCH (D4)
# ============================================================

bonus = digitalio.DigitalInOut(board.D4)
bonus.switch_to_input(pull=digitalio.Pull.UP)


# ============================================================
#  BUZZER (D6)
# ============================================================

buzzer = digitalio.DigitalInOut(board.D6)
buzzer.direction = digitalio.Direction.OUTPUT

def beep(t=0.12):
    buzzer.value = True
    time.sleep(t)
    buzzer.value = False


def beep_fail():
    buzzer.value = True
    time.sleep(0.35)
    buzzer.value = False


def beep_win():
    for _ in range(3):
        beep(0.12)
        time.sleep(0.05)


# ============================================================
#  NEOPIXEL HELPERS
# ============================================================

def clear_pixels():
    pixels.fill((0,0,0))
    pixels.show()

def show_pattern(indices, color):
    clear_pixels()
    for i in indices:
        if 0 <= i < NUM_PIXELS:
            pixels[i] = color
    pixels.show()

def flash(color, times=2):
    for _ in range(times):
        pixels.fill(color)
        pixels.show()
        time.sleep(0.15)
        clear_pixels()
        time.sleep(0.10)


# ============================================================
#  LED ZONES
# ============================================================

ZONE1 = [0,1,2,3]
ZONE2 = [4,5,6]
ZONE3 = [7,8,9,10]
ZONE4 = [11,12,13,14]

PATTERNS = [
    ZONE1,
    ZONE2,
    ZONE3,
    ZONE4,
    [0,4,7,11],
    [3,6,9,14],
]

COLORS = [
    (255,0,0),
    (0,255,0),
    (0,0,255),
    (255,255,0),
    (0,255,255),
    (255,0,255),
]


# ============================================================
#  DIFFICULTY SELECT
# ============================================================

def choose_difficulty():
    options = ["EASY", "NORMAL", "HARD"]
    speeds = [2.0, 1.4, 1.0]
    idx = 0

    while True:
        pos = abs(read_encoder())
        idx = pos % 3

        oled.fill(0)
        draw_text(0, 0, "SELECT LEVEL")
        draw_text(0, 16, (">" if idx==0 else " ") + "EASY")
        draw_text(0, 26, (">" if idx==1 else " ") + "NORMAL")
        draw_text(0, 36, (">" if idx==2 else " ") + "HARD")
        oled.show()

        if not enc_button.value:
            beep()
            time.sleep(0.25)
            return speeds[idx]

        time.sleep(0.03)


# ============================================================
#  GAME LOGIC
# ============================================================

ACTIONS = ["TILT", "TWIST", "PRESS", "COLOR", "BONUS"]

def play_game(base_time):
    score = 0

    for level in range(1, 11):

        pattern = random.choice(PATTERNS)
        target_color = random.choice(COLORS)
        action = random.choice(ACTIONS)

        oled_print("LEVEL "+str(level), "MEMORIZE")
        show_pattern(pattern, target_color)
        time.sleep(1)
        clear_pixels()

        oled_print("MOVE:", action)
        beep()

        timeout = max(0.6, base_time - (level-1)*0.1)
        start_t = time.monotonic()
        start_pos = read_encoder()
        success = False

        while time.monotonic() - start_t < timeout:

            if action == "TILT":
                if get_tilt():
                    success = True
                    break

            elif action == "TWIST":
                if abs(read_encoder() - start_pos) >= 2:
                    success = True
                    break

            elif action == "PRESS":
                if not enc_button.value:
                    success = True
                    break

            elif action == "COLOR":
                idx = abs(read_encoder()) % len(COLORS)
                show_pattern(pattern, COLORS[idx])
                if COLORS[idx] == target_color:
                    success = True
                    break

            elif action == "BONUS":
                if not bonus.value:
                    score += 1
                    success = True
                    break

            time.sleep(0.02)

        clear_pixels()

        if success:
            flash((0,255,0),2)
            beep()
            score += 1
        else:
            flash((255,0,0),3)
            beep_fail()
            oled_print("GAME OVER", "SCORE "+str(score))
            time.sleep(2)
            return

    oled_print("YOU WIN!", "SCORE "+str(score))
    pixels.fill((0,80,255))
    pixels.show()
    beep_win()
    time.sleep(2)
    clear_pixels()


# ============================================================
#  MAIN LOOP
# ============================================================

while True:
    oled_print("LIGHT GRID", "PRESS TO START")
    clear_pixels()

    if not enc_button.value:
        beep()
        time.sleep(0.25)
        base = choose_difficulty()
        play_game(base)

