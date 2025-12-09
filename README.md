
3. One random action is chosen from the action set.
4. The player must perform the correct action before the timer expires.
5. If the player **succeeds**:
- The buzzer plays a short success beep.
- The score increases based on the current level (higher levels give more points).
- The game advances to the next level with a slightly shorter time limit.
6. If the player **fails** (wrong move or timeout):
- A failure tone plays.
- The OLED shows a “SCORE” screen with a pair of pixel-art characters and the final score.
- The game checks if the player reached the high score table.
- A high score screen is shown, and the game waits for a button press to return to the difficulty selection menu.

If the player reaches the maximum level for the chosen difficulty, the game plays a simple “win” melody, shows the final score, updates the high score table if needed, and then returns to difficulty selection after a button press.

---

## Player Actions

Each level randomly selects **one** of the following actions:

### 1. TILT

- Uses the ADXL345 accelerometer.
- Success condition: the device is tilted strongly along the X or Y axis (beyond a threshold).

### 2. SHAKE

- Uses the magnitude of the acceleration vector.
- Success condition: a quick shaking motion is detected, causing the total acceleration to exceed a threshold.

### 3. TWIST

- Uses the rotary encoder (pins D1 / D2).
- Success condition: the player twists the knob enough steps within the time limit.
- The game uses a debounced encoder read so that a small twist moves only one logical step, improving control.

### 4. PRESS

- Uses the encoder push button (D0).
- Success condition: the button is pressed while the timer is still running.

### 5. LIGHT_POS

- Only the **first 6 LEDs** (indexes 0–5) are used for gameplay.
- The game randomly chooses a **target index** between 0 and 5.
- One LED is lit at the current position.
- The player rotates the encoder to move the lit LED around the ring.
- Success condition: the lit LED position matches the target index before the time limit expires.

### 6. LIGHT_COLOR

- The system randomly selects a color from: **RED**, **GREEN**, **BLUE**, **YELLOW**.
- The first 6 NeoPixels are filled with the chosen color.
- The OLED displays:
- LEVEL X
- MOVE: <ACTION>
- TIME: <seconds>

3. One random action is chosen from the action set.
4. The player must perform the correct action before the timer expires.
5. If the player **succeeds**:
- The buzzer plays a short success beep.
- The score increases based on the current level (higher levels give more points).
- The game advances to the next level with a slightly shorter time limit.
6. If the player **fails** (wrong move or timeout):
- A failure tone plays.
- The OLED shows a “SCORE” screen with a pair of pixel-art characters and the final score.
- The game checks if the player reached the high score table.
- A high score screen is shown, and the game waits for a button press to return to the difficulty selection menu.

If the player reaches the maximum level for the chosen difficulty, the game plays a simple “win” melody, shows the final score, updates the high score table if needed, and then returns to difficulty selection after a button press.

---

## Player Actions

Each level randomly selects **one** of the following actions:

### 1. TILT

- Uses the ADXL345 accelerometer.
- Success condition: the device is tilted strongly along the X or Y axis (beyond a threshold).

### 2. SHAKE

- Uses the magnitude of the acceleration vector.
- Success condition: a quick shaking motion is detected, causing the total acceleration to exceed a threshold.

### 3. TWIST

- Uses the rotary encoder (pins D1 / D2).
- Success condition: the player twists the knob enough steps within the time limit.
- The game uses a debounced encoder read so that a small twist moves only one logical step, improving control.

### 4. PRESS

- Uses the encoder push button (D0).
- Success condition: the button is pressed while the timer is still running.

### 5. LIGHT_POS

- Only the **first 6 LEDs** (indexes 0–5) are used for gameplay.
- The game randomly chooses a **target index** between 0 and 5.
- One LED is lit at the current position.
- The player rotates the encoder to move the lit LED around the ring.
- Success condition: the lit LED position matches the target index before the time limit expires.

### 6. LIGHT_COLOR

- The system randomly selects a color from: **RED**, **GREEN**, **BLUE**, **YELLOW**.
- The first 6 NeoPixels are filled with the chosen color.
- The OLED displays:

- LIGHT COLOR
- IS THIS <COLOR>?
- PRESS = YES
- 
- For this version of the game, pressing the button confirms the displayed color.
- Success condition: the player presses the button within the time limit.

> Note: Infrared (IR) sensors are **not** used in this version of the game. All interaction is handled via motion, the encoder, the button, and the LEDs.

---

## High Score System

The game includes a **three-slot high score table** that is saved in the XIAO ESP32-C3’s onboard non-volatile memory (`microcontroller.nvm`). No external SD card or storage module is used.

### High Score Features

- The game tracks the **top three scores** along with a **three-letter player initial** for each score.
- High score data persists **across power cycles** because it is stored in onboard NVM.

### When High Score Entry Appears

After **Game Over** or **You Win**:

1. The game compares the current score with the stored top three scores.
2. If the new score is high enough to enter the list:
 - A **“NEW HIGH!”** screen appears.
 - The player is asked to enter a **three-letter initial** using the rotary encoder and button.

### Entering Initials

For each of the three characters:

- The OLED shows:

- NEW HIGH!
- LETTER N
- <CURRENT LETTER>

- Rotate the encoder to scroll through letters **A–Z**.
- Press the encoder button to confirm the current letter and move to the next position.
- After three letters are selected, the game inserts the new score and initials into the high score list in the correct sorted position and saves them to NVM.

### High Score Screen

After updating, or if no new high score is achieved:

- The game shows a **high score table**:

- HIGH SCORES
- 1:ABC 120
- 2:XYZ 100
- 3:--- 50
- 
- The game waits for one button press, then returns to the difficulty selection screen.

---

## Visual & Audio Feedback

### NeoPixel LEDs (9 physical, first 6 used in game logic)

- Smooth 2.5-second startup animation (green fade in/out).
- Level color feedback (LED color changes as level increases).
- Single-LED movement for **LIGHT_POS**.
- Solid color display for **LIGHT_COLOR**.
- All LEDs off during score screens for clarity.

### OLED Display (128×64)

- Title screen (BOP-IT DELUXE).
- Difficulty selection menu.
- Per-level status:

- LEVEL X
- MOVE:<ACTION>
- TIME:<seconds>

- Light-based prompts:

- `LIGHT POS` & target index
- `LIGHT COLOR` & color name

- Score screen with pixel-art characters.
- High score table screen.
- “NEW HIGH!” initial input screens.

### Passive Buzzer (D6)

- Startup beep on title screen.
- Short beep for correct actions.
- Longer tone for failure.
- Simple ascending sequence for winning the game.
- Short clicks when scrolling through initials (optional, depending on configuration).

---

## Controls & Hardware Mapping

**XIAO ESP32-C3**  
Main microcontroller running CircuitPython and all game logic.

**SSD1306 OLED Display (I2C)**  
- SDA = D8  
- SCL = D9  

**ADXL345 Accelerometer (I2C)**  
- SDA = D8  
- SCL = D9  

**NeoPixel LED Strip (9 LEDs total)**  
- Data Pin = D3  
- Game uses **LED 0–5** as the active light positions.

**Rotary Encoder**  
- A / B Pins = D1 / D2 (rotation sensing)  
- Push Button = D0 (press actions & menu select)

**Passive Buzzer**  
- Signal Pin = D6

**Battery & Power Switch**  
- 5V + GND via inline slide switch  
- All grounds are shared between ESP32-C3, LEDs, display, accelerometer, and encoder.

---

## Enclosure Design Concept

The enclosure is designed as a compact handheld reaction toy:

- The OLED screen is centered near the top for easy reading.
- The NeoPixel LEDs form a light “frame” around the front panel, with the active 6 LEDs arranged to give a sense of direction and position.
- The rotary encoder is placed where the player’s thumb can comfortably twist and press.
- The main button (encoder press) is easily reachable for quick reactions.
- The buzzer is mounted inside with a sound vent.
- The battery and power switch are placed at the back or side for portability and easy charging/switching.

The enclosure design emphasizes:

- Clear mapping between on-screen instructions and physical controls.
- Strong, colorful visual feedback through the LEDs.
- One-hand operation with thumb-controlled twisting and pressing.
- A playful, retro arcade aesthetic.

---

## Repository Structure

```text
.
├── README.md                      # Project description and documentation
├── src/
│   └── main.py                    # Final game code (CircuitPython)
└── Documentation/
  ├── final_project.kicad_sch    # Circuit diagram (KiCad)
  ├── system_block_diagram.png   # System block diagram
  └── enclosure_sketches.png     # Enclosure design sketches
