from machine import Pin, I2C, PWM
import time
import ssd1306
import random

def run():
    i2c = I2C(1, sda=Pin(26), scl=Pin(27), freq=400000)
    display = ssd1306.SSD1306_I2C(128, 64, i2c)
    left_btn = Pin(4, Pin.IN, Pin.PULL_UP)
    back_btn = Pin(8, Pin.IN, Pin.PULL_UP) # Middle button (EXIT)
    right_btn = Pin(13, Pin.IN, Pin.PULL_UP)
    buzzer = PWM(Pin(15))
    buzzer.duty_u16(0)

    def play_tone(freq, dur):
        buzzer.freq(freq)
        buzzer.duty_u16(20000)
        time.sleep_ms(dur)
        buzzer.duty_u16(0)

    def draw_heart(x, y):
        display.pixel(x+1, y, 1)
        display.pixel(x+3, y, 1)
        display.hline(x, y+1, 5, 1)
        display.hline(x+1, y+2, 3, 1)
        display.pixel(x+2, y+3, 1)

    plate_x = 50
    plate_w = 28
    pan_x = random.randint(0, 110)
    pan_y = 0
    score = 0
    game_over = False
    heart_timer = 0
    heart_x = 0

    # Startup Cute Melody
    play_tone(1047, 100)
    play_tone(1319, 150)

    while True:
        if not back_btn.value(): 
            while not back_btn.value(): time.sleep_ms(10)
            return

        if game_over:
            display.fill(0)
            display.text("Oh no! Dropped!", 10, 15, 1)
            display.text(f"Pancakes: {score}", 25, 30, 1)
            display.show()
            time.sleep(0.5)
            while True:
                if not back_btn.value(): return
                if not left_btn.value() or not right_btn.value():
                    plate_x, pan_y, score = 50, 0, 0
                    pan_x = random.randint(0, 110)
                    game_over = False
                    break
                time.sleep_ms(50)
            continue

        # Plate movement
        if not left_btn.value() and plate_x > 0:
            plate_x -= 8
        if not right_btn.value() and plate_x < (128 - plate_w):
            plate_x += 8

        # Pancake falling
        pan_y += 2
        
        # Catch logic
        if pan_y >= 52:
            if plate_x - 5 <= pan_x <= plate_x + plate_w:
                score += 1
                pan_y = 0
                pan_x = random.randint(0, 110)
                heart_timer = 10 # Show heart for 10 frames
                heart_x = plate_x + 10
                play_tone(1200 + (score * 20), 50) # Pitch goes up with score
            elif pan_y > 64:
                play_tone(300, 300)
                game_over = True

        # Draw Frame
        display.fill(0)
        display.text(f"Gorima's Pancakes: {score}", 0, 0, 1)
        
        # Draw Plate
        display.hline(plate_x, 58, plate_w, 1)
        display.hline(plate_x+4, 59, plate_w-8, 1)
        
        # Draw Falling Pancake (Rounded rect with syrup line)
        display.fill_rect(pan_x, pan_y, 16, 5, 1)
        display.hline(pan_x+2, pan_y+2, 12, 0) # Syrup line
        
        # Draw Heart if caught recently
        if heart_timer > 0:
            draw_heart(heart_x, 45)
            heart_timer -= 1

        display.show()
        time.sleep_ms(30)