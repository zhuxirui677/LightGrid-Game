# LightGrid-Game
LightGrid-Game
# LIGHT GRID – Tilt & Twist Reaction Game

## Overview

LIGHT GRID is a small handheld reaction game built with a XIAO ESP32-C3, a 9-LED NeoPixel strip (3 segments of 3 LEDs), an accelerometer, an OLED display, a rotary encoder, and a buzzer.

On each level, the device shows a light pattern and asks the player to perform a random action:
- **Tilt** the whole device
- **Twist** the rotary knob
- **Press** the encoder button
- **Match a color** with the knob
- **Hit the BONUS button**

If the player performs the correct move before the timer runs out, they score a point and go to the next level. If they fail or are too slow, the game ends with a red flash and a “GAME OVER” screen.

---

## How the Game Works

### 1. Startup & Main Screen

When powered on, the NeoPixels flash briefly and then turn off.  
The OLED shows:


- The **rotary encoder button (D0)** is the main start button.
- The buzzer plays a short beep when the game starts.

### 2. Difficulty Selection

After pressing the encoder button, the game enters a level selection menu:

- Rotate the knob to choose between:
  - `EASY` – Slow timer (base time = 2.0 s)
  - `NORMAL` – Medium timer (base time = 1.4 s)
  - `HARD` – Fast timer (base time = 1.0 s)

The current option is shown with a `>` on the OLED:


Press the encoder button again to confirm.  
The chosen difficulty controls how much time the player has for each action. The time window gets slightly shorter on higher levels.

### 3. LED Patterns & Colors

The 9 NeoPixel LEDs are grouped into “zones” and patterns in the code:

- `ZONE1`, `ZONE2`, `ZONE3`, `ZONE4` and some diagonal patterns.
- A random pattern is chosen every level.
- A random color is also chosen from a list of preset RGB colors.

Flow of each level:

1. The OLED shows: `LEVEL N` / `MEMORIZE`
2. The LEDs light up in that pattern and color for 1 second.
3. The LEDs turn off.
4. The OLED shows the required **action**, for example:


5. The buzzer beeps once to indicate that the timer has started.

### 4. Actions (Game Inputs)

Each level randomly chooses one of the following actions:

- `TILT` – Read from the **ADXL345 accelerometer** (on I2C D8/D9).  
- If the device is tilted far enough on X or Y (>|5 m/s²|), the move succeeds.

- `TWIST` – Use the **rotary encoder A/B signals (D1/D2)**.  
- If the knob is rotated by at least 2 encoder steps, the move succeeds.

- `PRESS` – Use the **encoder push button (D0)**.  
- If the button is pressed before the timer runs out, the move succeeds.

- `COLOR` – Use the encoder to cycle through colors.  
- Turning the knob changes the LED color.
- When the displayed color matches the original target color, the move succeeds.

- `BONUS` – Use the **separate BONUS push button (D4)**.  
- Pressing this button gives an **extra score point** and completes the level.

If the action is detected in time:

- NeoPixels flash green quickly.
- The buzzer beeps.
- `score += 1` and the game goes to the next level.

If the player fails or times out:

- NeoPixels flash red several times.
- A long “fail” sound plays.
- The OLED shows:


- All LEDs turn blue.
- The buzzer plays a small “victory” pattern.

Then the device returns to the main screen.

---

## Controls & Hardware Mapping

- **XIAO ESP32-C3**
- Drives all logic and animations.
- Handles NeoPixel timing, input reading, and game state.

- **SSD1306 128x64 OLED (I2C SCL=D9, SDA=D8)**
- Shows game title, menu, level number, and current required action.
- Displays score on game over / win.

- **ADXL345 Accelerometer (I2C SCL=D9, SDA=D8)**
- Provides tilt detection for the `TILT` action.

- **Rotary Encoder with Push Button**
- **A/B → D1/D2**: rotation for `TWIST` and color selection in `COLOR`.
- **SW → D0**: main confirm / start button and `PRESS` action.

- **BONUS Button (D4)**
- A separate push button used for the special `BONUS` action.
- Gives an extra point when pressed in time.

- **NeoPixel LEDs (9 total, chained)**
- Visual feedback for patterns, colors, success (green flash) and failure (red flash).
- First DIN is driven from **D3** (with a series resistor).

- **Buzzer (D6)**
- Simple audio feedback:
  - Short beeps for start/OK.
  - Long tone for failure.
  - Repeated beeps for win.

- **Battery & Power Switch**
- External battery pack connected to the XIAO 5V pin through a small slide switch.
- Allows the device to be turned on/off without unplugging the battery.
- All grounds are shared.

---

## Enclosure Design Thoughts

The enclosure is designed as a small handheld “90s-style” game device:

- The **OLED** is placed near the top so text is easy to read while holding the device.
- The **9 NeoPixel LEDs** are arranged together as a “light grid”, making patterns and colors clearly visible.
- The **rotary encoder** is placed on the side or lower front, so the player can twist and press it with one hand.
- The **BONUS button** is positioned away from the encoder, creating a separate, special action that feels distinct.
- The **buzzer** is inside the case, with a small sound hole so feedback is audible but not too loud.
- The **battery and slide power switch** are on the back or side, making it easy to power the device on/off and replace the battery.

The overall goal of the enclosure is to:
- Encourage active interaction (tilting, twisting, pressing).
- Make the mapping from actions → hardware very clear.
- Keep the form factor compact so it feels like a small toy/game console you can hold and shake.

---

## Repository Structure

```text
.
├── README.md              # Project overview and game description
├── src/
│   └── light_grid_game.py # Main game code (this file)
└── Documentation/
  ├── final_project.kicad_sch  # Circuit diagram (KiCad schematic)
  ├── system_block_diagram.png # System block diagram
  └── enclosure_sketches.png   # Enclosure concept images (optional)
