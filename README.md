## Introduction

LightGrid is a handheld interactive reaction game designed to explore real-time physical interaction, motion sensing, and embedded game logic using a compact microcontroller platform. Inspired by classic arcade-style reflex games such as Bop-It, LightGrid transforms simple hardware components—lights, motion, sound, and mechanical input—into a fast-paced, skill-based interactive experience.

The project is built around the XIAO ESP32-C3 microcontroller and integrates multiple input and output modalities, including an OLED display for instruction feedback, NeoPixel LEDs for visual cues, an accelerometer for motion detection, a rotary encoder for control input, and a passive buzzer for audio feedback. Players interact with the device through tilting, shaking, twisting, pressing, and light-based challenges, receiving immediate feedback for every action.

Beyond gameplay, LightGrid represents a complete embedded systems workflow, encompassing hardware integration, CircuitPython firmware development, real-time interaction design, and non-volatile data storage through an onboard high score system. The project emphasizes physical computing, responsive control design, and the translation of simple electronic inputs into an engaging digital play experience.

---

## Overview

LightGrid is a handheld reaction game built with a XIAO ESP32-C3, a 9-LED NeoPixel light frame, an ADXL345 accelerometer, a 128×64 OLED display, a rotary encoder, and a passive buzzer.

The game challenges players to react quickly to changing instructions such as tilting, shaking, twisting, pressing, and interacting with LED-based tasks. Each correct action advances the player to the next level, while the reaction time becomes progressively shorter as difficulty increases. A failure—either through an incorrect action or a timeout—ends the run and displays the final score.

LightGrid combines physical motion, visual prompts, and sound feedback to create a tightly coupled interaction loop between the player and the device. The design focuses on real-time responsiveness, intuitive physical control, and clear multimodal feedback using motion, light, sound, and on-screen prompts.

---

## How the Game Works

LightGrid operates as a level-based reaction game with an increasing difficulty curve. The game flow consists of four main stages: startup, difficulty selection, core gameplay loop, and end-of-game feedback.

### 1. Startup & Title Screen

When the device is powered on:

- The NeoPixel LEDs perform a smooth green startup animation.
- The OLED displays the game title:

  BOP-IT  
  DELUXE  

- The buzzer plays a short confirmation beep to indicate that the system is ready.

This startup sequence establishes visual, auditory, and system readiness feedback for the player.

---

### 2. Difficulty Selection

The player selects the game difficulty using the rotary encoder:

- Rotate the knob to switch between:
  - EASY – Longer reaction time and fewer levels  
  - MEDIUM – Moderate reaction time and level count  
  - HARD – Short reaction time and the highest number of levels  

- Press the encoder button (D0) to confirm the selected difficulty.

The chosen difficulty directly affects:
- The base reaction time for each level  
- The rate at which the time limit shrinks  
- The total number of levels required to complete the game  

This selection stage allows players to choose an appropriate challenge level before entering gameplay.

---

### 3. Core Gameplay Loop

After difficulty selection, the game enters the main gameplay loop. Each level follows the same structured sequence:

1. The NeoPixel LEDs change color based on the current level.
2. The OLED displays the current game state:

   LEVEL X  
   MOVE: <ACTION>  
   TIME: <seconds>  

3. One random action is selected from the action set.
4. The player must perform the correct physical interaction before the timer expires.
5. If the player succeeds:
   - The buzzer plays a short success tone  
   - The score increases based on the current level  
   - The game advances to the next level with a shorter reaction window  
6. If the player fails:
   - A failure tone plays  
   - The OLED displays the final score  
   - The game checks and updates the high score table  
   - The player is returned to the difficulty selection screen after confirmation  

This loop forms the core real-time interaction pipeline of LightGrid, tightly coupling sensing, timing, feedback, and player response.

---

### 4. End-of-Game Outcomes

LightGrid supports two end states:

- **Game Over:** Triggered when the player fails an action or runs out of time. The final score is displayed and evaluated for high score entry.
- **Victory (You Win):** Triggered when the player successfully completes all levels for the selected difficulty. A win sound sequence plays, followed by score display and high score evaluation.

In both cases, the game transitions to the high score system before allowing the player to restart.


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
