# ============================================================
# FINAL PROJECT – HANDHELD GAME (STABLE FINAL BUILD)
# LightGrid – Tilt & Twist Reaction Game
# Xiao ESP32-C3 + CircuitPython
# 6 NeoPixels ONLY (0–5)
# Smooth 2.5s Startup + Difficulty + High Score + Initials
# ============================================================

import time, random
import board, busio, digitalio, neopixel, pwmio, microcontroller
import adafruit_ssd1306
import adafruit_adxl34x

# ================= FULL OLED FONT =================

mini_font = {
"A":[0x7C,0x12,0x11,0x12,0x7C],"B":[0x7F,0x49,0x49,0x49,0x36],
"C":[0x3E,0x41,0x41,0x41,0x22],"D":[0x7F,0x41,0x41,0x22,0x1C],
"E":[0x7F,0x49,0x49,0x49,0x41],"F":[0x7F,0x09,0x09,0x09,0x01],
"G":[0x3E,0x41,0x49,0x49,0x7A],"H":[0x7F,0x08,0x08,0x08,0x7F],
"I":[0x41,0x41,0x7F,0x41,0x41],"J":[0x20,0x40,0x41,0x3F,0x01],
"K":[0x7F,0x08,0x1C,0x22,0x41],"L":[0x7F,0x40,0x40,0x40,0x40],
"M":[0x7F,0x02,0x1C,0x02,0x7F],"N":[0x7F,0x04,0x08,0x10,0x7F],
"O":[0x3E,0x41,0x41,0x41,0x3E],"P":[0x7F,0x09,0x09,0x09,0x06],
"Q":[0x3E,0x41,0x51,0x21,0x5E],"R":[0x7F,0x09,0x19,0x29,0x46],
"S":[0x26,0x49,0x49,0x49,0x32],"T":[0x01,0x01,0x7F,0x01,0x01],
"U":[0x3F,0x40,0x40,0x40,0x3F],"V":[0x3F,0x40,0x40,0x20,0x1F],
"W":[0x7F,0x20,0x18,0x20,0x7F],"X":[0x63,0x14,0x08,0x14,0x63],
"Y":[0x03,0x04,0x78,0x04,0x03],"Z":[0x61,0x51,0x49,0x45,0x43],
"0":[0x3E,0x51,0x49,0x45,0x3E],"1":[0x42,0x7F,0x40,0x00,0x00],
"2":[0x62,0x51,0x49,0x49,0x46],"3":[0x22,0x41,0x49,0x49,0x36],
" ":[0,0,0,0,0],":":[0x00,0x36,0x36,0x00,0x00]
}

def draw_char(d, ch, x, y):
    if ch not in mini_font: ch=" "
    bits = mini_font[ch]
    for col in range(5):
        for row in range(7):
            if (bits[col] >> row) & 1:
                d.pixel(x+col, y+row, 1)

def draw_text(d, t, x, y):
    for i,ch in enumerate(t):
        draw_char(d,ch,x+i*6,y)

def show_text(a="",b="",c=""):
    oled.fill(0)
    draw_text(oled,a,0,0)
    draw_text(oled,b,0,22)
    draw_text(oled,c,0,44)
    oled.show()

# ================= HARDWARE =================

i2c = busio.I2C(board.D9, board.D8)
oled = adafruit_ssd1306.SSD1306_I2C(128,64,i2c)
oled.rotation=2

accel = adafruit_adxl34x.ADXL345(i2c)

NUM_PIXELS = 6   
pixels = neopixel.NeoPixel(board.D3, NUM_PIXELS, brightness=0.3, auto_write=False)

btn=digitalio.DigitalInOut(board.D0); btn.switch_to_input(pull=digitalio.Pull.UP)
clk=digitalio.DigitalInOut(board.D1); clk.switch_to_input(pull=digitalio.Pull.UP)
dt =digitalio.DigitalInOut(board.D2); dt.switch_to_input(pull=digitalio.Pull.UP)

last_clk=clk.value
last_btn=btn.value
enc_pos=0

def leds_off():
    pixels.fill((0,0,0))
    pixels.show()

def beep(ms=120,f=2000):
    try:
        b=pwmio.PWMOut(board.D6,duty_cycle=0,frequency=f)
        b.duty_cycle=32768
        time.sleep(ms/1000)
        b.deinit()
    except:
        pass

# ================= 2.5s STARTUP =================

def startup_pixels():
    leds_off()
    for i in range(25):
        v = int((i/25)*120)
        pixels.fill((0,v,0))
        pixels.show()
        time.sleep(0.05)
    time.sleep(0.3)
    for i in range(25,-1,-1):
        v = int((i/25)*120)
        pixels.fill((0,v,0))
        pixels.show()
        time.sleep(0.04)
    leds_off()

# ================= ENCODER =================

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


# ================= HIGH SCORE =================

SCORE_ADDR=0
NAME_ADDR=16

def load_high_scores():
    s=[]
    for i in range(3):
        lo=microcontroller.nvm[SCORE_ADDR+2*i]
        hi=microcontroller.nvm[SCORE_ADDR+2*i+1]
        v=0 if lo==0xFF else lo|(hi<<8)
        name=""
        for j in range(3):
            b=microcontroller.nvm[NAME_ADDR+i*3+j]
            if b==0xFF: break
            name+=chr(b)
        s.append([v,name if name!="" else "---"])
    return s

def save_high_scores(s):
    for i in range(3):
        v=s[i][0]
        microcontroller.nvm[SCORE_ADDR+2*i]=v&0xFF
        microcontroller.nvm[SCORE_ADDR+2*i+1]=(v>>8)&0xFF
        for j in range(3):
            microcontroller.nvm[NAME_ADDR+i*3+j]=ord(s[i][1][j])

def enter_initials():
    letters="ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    name=""
    for i in range(3):
        idx=0
        while True:
            read_encoder()
            d=get_enc_delta()
            if d!=0:
                idx=(idx+d)%26
                beep(40,2600)
            show_text("NEW HIGH!","LETTER "+str(i+1),letters[idx])
            if button_pressed():
                name+=letters[idx]
                beep(160,3000)
                break
            time.sleep(0.05)
    return name

def show_high_scores(s):
    oled.fill(0)
    draw_text(oled,"HIGH SCORES",0,0)
    for i in range(3):
        draw_text(oled,str(i+1)+":"+s[i][1]+" "+str(s[i][0]),0,20+i*14)
    oled.show()

def check_new_high(score):
    s=load_high_scores()
    for i in range(3):
        if score>s[i][0]:
            name=enter_initials()
            s.insert(i,[score,name])
            s=s[:3]
            save_high_scores(s)
            return s
    return s

# ================= GAME ACTIONS =================

def wait_press(t):
    s=time.monotonic()
    while time.monotonic()-s<t:
        if button_pressed(): return True
    return False

def wait_twist(t):
    s=time.monotonic(); tot=0
    while time.monotonic()-s<t:
        read_encoder()
        tot+=abs(get_enc_delta())
        if tot>2: return True
    return False

def wait_tilt(t):
    s=time.monotonic()
    while time.monotonic()-s<t:
        x,y,_=accel.acceleration
        if abs(x)>3 or abs(y)>3: return True
    return False

def wait_shake(t):
    s=time.monotonic()
    while time.monotonic()-s<t:
        x,y,z=accel.acceleration
        if (x*x+y*y+z*z)**0.5>8: return True
    return False

def wait_light_pos(t):
    tgt=random.randint(0,NUM_PIXELS-1)
    pos=random.randint(0,NUM_PIXELS-1)
    s=time.monotonic()
    while time.monotonic()-s<t:
        leds_off()
        pixels[pos]=(255,255,255)
        pixels.show()
        show_text("LIGHT POS","TARGET:"+str(tgt),"")
        read_encoder()
        pos=(pos+get_enc_delta())%NUM_PIXELS
        if pos==tgt: return True
    return False

def wait_light_color(t):
    colors={"RED":(255,0,0),"GREEN":(0,255,0),
            "BLUE":(0,0,255),"YELLOW":(255,255,0)}
    k=random.choice(list(colors))
    pixels.fill(colors[k])
    pixels.show()
    s=time.monotonic()
    while time.monotonic()-s<t:
        show_text("LIGHT COLOR","IS THIS "+k+"?","PRESS = YES")
        if button_pressed(): return True
    return False

ACTIONS=["PRESS","TWIST","TILT","SHAKE","LIGHT_POS","LIGHT_COLOR"]

def run_action(a,t):
    if a=="PRESS": return wait_press(t)
    if a=="TWIST": return wait_twist(t)
    if a=="TILT": return wait_tilt(t)
    if a=="SHAKE": return wait_shake(t)
    if a=="LIGHT_POS": return wait_light_pos(t)
    if a=="LIGHT_COLOR": return wait_light_color(t)
    return False

# ================= SCORE DISPLAY =================

def draw_cute(x,y):
    for dx in [1,2,3]:
        oled.pixel(x+dx,y,1)
        oled.pixel(x+dx,y+4,1)
    for p in [(0,1),(4,1),(0,3),(4,3),
              (1,2),(3,2),(2,5),(2,6),(1,7),(3,7)]:
        oled.pixel(x+p[0],y+p[1],1)

def show_score(s):
    leds_off()
    oled.fill(0)
    draw_text(oled,"SCORE",0,0)
    draw_text(oled,str(s),0,22)
    draw_cute(88,18)
    draw_cute(108,18)
    oled.show()

# ================= MAIN =================

DIFF=[("EASY",5,8),("MEDIUM",4,10),("HARD",3.2,12)]

def select_diff():
    i=0
    while True:
        show_text("SELECT MODE",DIFF[i][0],"ROTATE + PRESS")
        read_encoder()
        d=get_enc_delta()
        if d:
            i=(i+d)%3
        if button_pressed():
            return DIFF[i]
        time.sleep(0.05)

startup_pixels()
show_text("BOP-IT","DELUXE","")
beep(200,2000)
time.sleep(0.6)

while True:
    name,tmax,lvlmax=select_diff()
    level=1
    score=0
    over=False

    while level<=lvlmax and not over:
        limit=max(1.5,tmax*(0.92**level))
        pixels.fill(((level*30)%255,80,80))
        pixels.show()

        a=random.choice(ACTIONS)
        show_text("LEVEL "+str(level),"MOVE:"+a,"TIME:"+str(round(limit,1)))

        if run_action(a,limit):
            beep(120,1900)
            score+=level*10
            level+=1
        else:
            show_score(score)
            beep(400,900)
            s=check_new_high(score)
            time.sleep(0.6)
            show_high_scores(s)
            while not button_pressed():
                time.sleep(0.05)
            over=True

    if not over:
        show_score(score)
        beep(200,1800)
        beep(200,2200)
        beep(250,2600)
        s=check_new_high(score)
        time.sleep(0.6)
        show_high_scores(s)
        while not button_pressed():
            time.sleep(0.05)


