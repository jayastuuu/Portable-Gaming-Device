# Portable Gaming Device

[![Console Demo](https://img.youtube.com/vi/LIlF-m11eEY/maxresdefault.jpg)](https://youtu.be/LIlF-m11eEY)
*(Click the image above to watch the unlisted video demonstration)*


The system utilizes a unified `main.py` launcher that dynamically imports individual game modules into the Pico's memory only when selected, preventing memory overflow. 

*   **Dino Runner (`dino.py`)**: A clone of the classic browser game featuring progressive difficulty, gravity physics, and dynamically scaling obstacle speed.
*   **Flappy Bird (`flappy.py`)**: A physics-based scroller with custom flap mechanics, gap generation, and collision detection.
*   **Pancake Catch (`pancake.py`)**: A cutesy, high-speed reaction game featuring custom pixel art, dynamic chiptune pitch-scaling, and stacked scoring. 

##  Hardware Architecture

The circuit was specifically soldered to eliminate overlapping wires and keep the physical layout clean. 

**Components Used:**
*   Raspberry Pi Pico (RP2040)
*   SSD1306 OLED Display (128x64)
*   3x Tactile Push Buttons
*   1x Passive Buzzer

**Custom Pin Mapping:**
| Component | Pico Pin | Physical Pin | Function |
| :--- | :--- | :--- | :--- |
| **OLED (I2C1)** | GP26 / GP27 | 31 / 32 | SDA / SCK |
| **Left Button** | GP4 | 6 | Select / Action |
| **Middle Button** | GP8 | 11 | Back / Hard Exit |
| **Right Button** | GP13 | 17 | Scroll / Action |
| **Buzzer (PWM)**| GP15 | 20 | Audio Out |

##  Tech Stack & Tools
*   **Language:** MicroPython
*   **Libraries:** `machine` (Pin, I2C, PWM), `ssd1306`, `time`, `random`
*   **Environment:** VS Code with MicroPico extension

##  How to Run
1. Flash the Raspberry Pi Pico with the latest MicroPython `.uf2` firmware.
2. Wire the components according to the pin mapping table above.
3. Upload `ssd1306.py`, `main.py`, `dino.py`, `flappy.py`, and `pancake.py` to the Pico's root directory.
4. Reboot the Pico to automatically launch the main menu.
