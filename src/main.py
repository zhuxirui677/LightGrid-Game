# ============================================================
# FINAL PROJECT - 90s STYLE HANDHELD GAME (FINAL VERSION)
# 9 NeoPixels around frame (no IR)
# LIGHT_POS + LIGHT_COLOR (YES/NO STYLE)
# Longer reaction time, startup animation, difficulty select
# Xiao ESP32-C3 + CircuitPython
# ============================================================

import time
import random
import board
import busio
import digitalio
import neopixel
import adafruit_ssd1306
import adafruit_adxl34x
import pwmio

# ============================================================
# MINI FONT (OLED 5x7)
# ============================================================

mini_font = {
    "A":[0x7C,0x12,0x11,0x12,0x7C],"B":[0x7F,0x49,0x49,0x49,0x36],
    "C":[0x3E,0x41,0x41,0x41,0x22],"D":[0x7F,0x41,0x41,0x22,0x1C],
    "E":[0x7F,0x49,0x49,0x49,0x41],"F":[0x7F,0x09,0x09,0x09,0x01],
    "G":[0x3E,0x41,0x49,0x49,0x7A],"H":[0x7F,0x08,0x08,0x08,0x7F],
    "I":[0x41,0x41,0x7F,0x41,0x41],"J":[0x20,0x40,0x41,0x3F,0x01],
    "K":[0x7F,0x08,0x1C,0x22,0x41],"L":[0x7F,0x40,0x40,0x40,0x40],
    "M":[0x7F,0x02,0x1C,0x02,0x7F],"N":[0x7F,0x04,0x08,0x10,0x7F],
    "O":[0x3E,0x41,0x41,0x41,0x3E],"P":[0x7F,0x09,0x09,0x09,0x06],
    "R":[0x7F,0x09,0x19,0x29,0x46],"S":[0x26,0x49,0x49,0x49,0x32],
    "T":[0x01,0x01,0x7F,0x01,0x01],"U":[0x3F,0x40,0x40,0x40,0x3F],
    "V":[0x3F,0x40,0x40,0x20,0x1F],"W":[0x7F,0x20,0x18,0x20,0x7F],
    "X":[0x63,0x14,0x08,0x14,0x63],
    "0":[0x3E,0x51,0x49,0x45,0x3E],"1":[0x42,0x7F,0x40,0x00,0x00],
    "2":[0x62,0x51,0x49,0x49,0x46],"3":[0x22,0x41,0x49,0x49,0x36],
    " ":[0,0,0,0,0],":":[0x00,0x36,0x36,0x00,0x00]
}

def draw_char(d, ch, x, y, c=1):
    if ch not in mini_font:
        ch = " "
    data = mini_font[ch]
    for col in range(5):
        bits = data[col]
        for row in range(7):
            if (bits >> row) & 1:
                d.pixel(x + col, y + row, c)

def draw_text(d, text, x, y):
    for i, ch in enumerate(text):
        draw_char(d, ch, x + i * 6, y)

def show_text(l1="", l2="", l3=""):
    oled.fill(0)
    draw_text(oled, l1, 0, 0)
    draw_text(oled, l2, 0, 22)
    draw_text(oled, l3, 0, 44)
    oled.show()

# ============================================================
# HARDWARE INIT
# ============================================================

i2c = busio.I2C(board.D9, board.D8)
oled = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c)
oled.rotation = 2

accel = adafruit_adxl34x.ADXL345(i2c)

NUM_PIXELS = 9
pixels = neopixel.NeoPixel(board.D3, NUM_PIXELS, brightness=0.3, auto_write=False)

def leds_off():
    pixels.fill((0, 0, 0))
    pixels.show()

# ============================================================
# BUZZER
# ============================================================

def beep(ms=150, freq=2000):
    b = pwmio.PWMOut(board.D6, duty_cycle=0, frequency=freq)
    b.duty_cycle = 32768
    time.sleep(ms / 1000)
    b.duty_cycle = 0
    b.deinit()

# ============================================================
# STARTUP + LEVEL LED
# ============================================================

def startup_pixels():
    leds_off()
    # simple wipe with green then off
    for i in range(NUM_PIXELS):
        pixels[i] = (0, 180, 0)
        pixels.show()
        time.sleep(0.06)
    time.sleep(0.2)
    leds_off()

def px_level(level):
    # all LEDs same color but随着等级变
    r = (level * 25) % 255
    g = max(0, 255 - level * 18)
    b = 80
    pixels.fill((r, g, b))
    pixels.show()

# ============================================================
# ROTARY + BUTTON
# ============================================================

btn = digitalio.DigitalInOut(board.D0)
btn.switch_to_input(pull=digitalio.Pull.UP)

clk = digitalio.DigitalInOut(board.D1)
clk.switch_to_input(pull=digitalio.Pull.UP)

dt  = digitalio.DigitalInOut(board.D2)
dt.switch_to_input(pull=digitalio.Pull.UP)

last_clk = clk.value
last_btn = btn.value
enc_pos = 0

def read_encoder():
    global last_clk, enc_pos
    c = clk.value
    if last_clk and not c:
        if dt.value != c:
            enc_pos += 1
        else:
            enc_pos -= 1
    last_clk = c

def get_enc_delta():
    global enc_pos
    d = enc_pos
    enc_pos = 0
    return d

def button_pressed():
    global last_btn
    c = btn.value
    pressed = False
    if last_btn and not c:
        time.sleep(0.01)
        if not btn.value:
            pressed = True
    last_btn = c
    return pressed

# ============================================================
# LIGHT POS (单灯位置)
# ============================================================

def wait_light_pos(limit):
    target = random.randint(0, NUM_PIXELS - 1)
    pos = random.randint(0, NUM_PIXELS - 1)
    start = time.monotonic()

    while time.monotonic() - start < limit:
        leds_off()
        pixels[pos] = (255, 255, 255)
        pixels.show()

        show_text("LIGHT POS", "TARGET:" + str(target), "")

        read_encoder()
        pos = (pos + get_enc_delta()) % NUM_PIXELS

        if pos == target:
            return True

        time.sleep(0.08)

    return False

# ============================================================
# LIGHT COLOR (系统出颜色，你确认)
# ============================================================

def wait_light_color(limit):
    color_names = ["RED", "GREEN", "BLUE", "YELLOW"]
    color_values = {
        "RED":    (255,   0,   0),
        "GREEN":  (0,   255,   0),
        "BLUE":   (0,     0, 255),
        "YELLOW": (255, 255,   0),
    }

    shown = random.choice(color_names)
    r, g, b = color_values[shown]

    pixels.fill((r, g, b))
    pixels.show()

    start = time.monotonic()
    while time.monotonic() - start < limit:
        show_text("LIGHT COLOR", "IS THIS " + shown + "?", "PRESS = YES")

        if button_pressed():
            # you always accept what you see -> success
            return True

        time.sleep(0.05)

    return False

# ============================================================
# OTHER ACTIONS
# ============================================================

def wait_press(limit):
    start = time.monotonic()
    while time.monotonic() - start < limit:
        if button_pressed():
            return True
    return False

def wait_twist(limit):
    total = 0
    start = time.monotonic()
    while time.monotonic() - start < limit:
        read_encoder()
        total += abs(get_enc_delta())
        if total >= 3:
            return True
    return False

def wait_tilt(limit):
    start = time.monotonic()
    while time.monotonic() - start < limit:
        x, y, _ = accel.acceleration
        if abs(x) > 3 or abs(y) > 3:
            return True
    return False

def wait_shake(limit):
    start = time.monotonic()
    while time.monotonic() - start < limit:
        x, y, z = accel.acceleration
        mag = (x*x + y*y + z*z) ** 0.5
        if mag > 8:
            return True
    return False

ACTIONS = ["TILT", "SHAKE", "TWIST", "PRESS", "LIGHT_POS", "LIGHT_COLOR"]

def run_action(act, limit):
    if act == "PRESS":      return wait_press(limit)
    if act == "TWIST":      return wait_twist(limit)
    if act == "TILT":       return wait_tilt(limit)
    if act == "SHAKE":      return wait_shake(limit)
    if act == "LIGHT_POS":  return wait_light_pos(limit)
    if act == "LIGHT_COLOR":return wait_light_color(limit)
    return False

# ============================================================
# 可爱像素小人 + SCORE
# ============================================================

def draw_cute_character(x, y):
    for dx in [1, 2, 3]:
        oled.pixel(x + dx, y, 1)
        oled.pixel(x + dx, y + 4, 1)
    oled.pixel(x,     y + 1, 1)
    oled.pixel(x + 4, y + 1, 1)
    oled.pixel(x,     y + 3, 1)
    oled.pixel(x + 4, y + 3, 1)
    oled.pixel(x + 1, y + 2, 1)
    oled.pixel(x + 3, y + 2, 1)
    oled.pixel(x + 2, y + 5, 1)
    oled.pixel(x + 2, y + 6, 1)
    oled.pixel(x + 1, y + 7, 1)
    oled.pixel(x + 3, y + 7, 1)

def show_score(score):
    leds_off()
    oled.fill(0)
    draw_text(oled, "SCORE", 0, 0)
    draw_text(oled, str(score), 0, 22)
    draw_cute_character(88, 18)
    draw_cute_character(108, 18)
    oled.show()

# ============================================================
# DIFFICULTY (反应时间拉长)
# ============================================================

DIFFS = [
    {"name": "EASY",   "time": 5.0, "levels": 8},
    {"name": "MEDIUM", "time": 4.0, "levels": 10},
    {"name": "HARD",   "time": 3.2, "levels": 12},
]

def select_diff():
    idx = 0
    leds_off()
    show_text("SELECT MODE", DIFFS[idx]["name"], "ROTATE + PRESS")
    while True:
        read_encoder()
        d = get_enc_delta()
        if d != 0:
            idx = (idx + d) % len(DIFFS)
            leds_off()
            show_text("SELECT MODE", DIFFS[idx]["name"], "PRESS TO START")
        if button_pressed():
            beep(200, 2500)
            return DIFFS[idx]
        time.sleep(0.05)

# ============================================================
# MAIN
# ============================================================

startup_pixels()
show_text("BOP-IT", "DELUXE", "")
beep(200, 2000)
time.sleep(1)

while True:
    cfg = select_diff()
    base_time = cfg["time"]
    max_level = cfg["levels"]

    level = 1
    score = 0

    while level <= max_level:
        limit = max(1.5, base_time * (0.92 ** level))

        px_level(level)
        act = random.choice(ACTIONS)
        show_text("LEVEL " + str(level),
                  "MOVE:" + act,
                  "TIME:" + str(round(limit, 1)))

        if run_action(act, limit):
            beep(150, 1800)
            score += level * 10
            level += 1
        else:
            show_score(score)
            beep(400, 900)
            while not button_pressed():
                pass
            break
