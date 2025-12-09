# LightGrid – 90s Style Tilt & Twist Reaction Game

## Overview

LightGrid is a handheld 90s-style reaction game built with a XIAO ESP32-C3, a 9-LED NeoPixel light frame, an ADXL345 accelerometer, a 128×64 OLED display, a rotary encoder, and a passive buzzer.

The game challenges players to react quickly to changing instructions such as tilting, twisting, pressing, and interacting with LED lights. Each correct action advances the player to the next level with increasing difficulty. A failure or timeout ends the game and displays the final score.

This project focuses on physical interaction, real-time feedback, and embedded game logic design using motion, light, sound, and user input.

---

## How the Game Works

### 1. Startup & Title Screen

When the device is powered on:

- The NeoPixel LEDs perform a brief startup animation.
- The OLED displays the game title:
  
  BOP-IT  
  DELUXE  

- The buzzer plays a short confirmation beep.

---

### 2. Difficulty Selection

The player selects the game difficulty using the rotary encoder:

- Rotate the knob to switch between:
  - EASY – Long reaction time, fewer levels
  - MEDIUM – Medium reaction time
  - HARD – Short reaction time, more levels

- Press the encoder button (D0) to confirm the selection.

The difficulty affects:
- The base reaction time for each level
- How fast the time limit shrinks
- The total number of levels in the game

---

### 3. Game Loop Logic

Each level follows this sequence:

1. The LEDs change color based on the level.
2. The OLED shows:
   
   LEVEL X  
   MOVE: <ACTION>  
   TIME: <seconds>  

3. A random action is selected.
4. The player must perform the correct motion before the timer expires.
5. If successful:
   - The buzzer beeps
   - The score increases
   - The game advances to the next level
6. If failed:
   - The score is displayed with pixel characters
   - A long failure tone plays
   - The game waits for restart

---

## Player Actions

Each level randomly selects one of the following actions:

### TILT
Uses the ADXL345 accelerometer.  
Success condition: the device is tilted strongly on the X or Y axis.

### SHAKE
Uses total acceleration magnitude.  
Success condition: a quick shaking motion is detected.

### TWIST
Uses the rotary encoder rotation (D1/D2).  
Success condition: the knob is rotated several steps.

### PRESS
Uses the encoder push button (D0).  
Success condition: the button is pressed within the time limit.

### LIGHT_POS
One LED is lit.  
The player rotates the encoder to move the light to the target position.

### LIGHT_COLOR
The system displays a random color.  
The OLED asks:
  
IS THIS <COLOR>?  
PRESS = YES  

The player confirms by pressing the button.

Infrared (IR) sensors are NOT used in this version of the game.

---

## Visual & Audio Feedback

NeoPixel LEDs (9 total) provide:
- Startup animation
- Level color feedback
- Success flashes
- Failure flashes

OLED Display provides:
- Title screen
- Difficulty menu
- Action prompts
- Score display

Passive Buzzer (D6) provides:
- Start beep
- Success beep
- Failure tone
- Win sequence

---

## Controls & Hardware Mapping

XIAO ESP32-C3  
Main microcontroller for all logic and input processing.

SSD1306 OLED Display (I2C)  
SDA = D8  
SCL = D9  

ADXL345 Accelerometer (I2C)  
SDA = D8  
SCL = D9  

NeoPixel LEDs (9 total)  
Data Pin = D3  

Rotary Encoder  
A/B Pins = D1 / D2  
Push Button = D0  

Passive Buzzer  
Signal Pin = D6  

Battery & Power Switch  
5V + GND with in-line slide switch  
All grounds are shared.

---

## Enclosure Design Concept

The enclosure is designed as a compact handheld 90s-style toy console.

- The OLED screen is centered near the top for readability.
- The NeoPixel lights form a glowing frame around the front panel.
- The rotary encoder is placed on the side for natural thumb control.
- The main button is placed on the front for fast reaction input.
- The buzzer is mounted inside the enclosure with a small sound vent.
- The battery and power switch are located on the back for portability.

The enclosure emphasizes:
- Clear mapping between action and control
- Strong visual feedback
- One-hand operation
- A retro arcade look and feel

---

## Repository Structure

.
├── README.md                    # Project description and documentation
├── src/
│   └── main.py                  # Final game code
└── Documentation/
    ├── final_project.kicad_sch        # Circuit diagram (KiCad)
    ├── system_block_diagram.png      # System block diagram
    └── enclosure_sketches.png        # Enclosure design sketches

---

## Summary

LightGrid combines:

- Motion sensing
- LED-based visual feedback
- Embedded sound effects
- Real-time reaction gameplay
- Physical user interaction

This project demonstrates a complete embedded system pipeline including hardware design, firmware programming, user interface feedback, and enclosure design.
