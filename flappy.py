from machine import Pin, I2C, PWM
import time
import ssd1306
import random

def run():
    i2c = I2C(1, sda=Pin(26), scl=Pin(27), freq=400000)
    display = ssd1306.SSD1306_I2C(128, 64, i2c)
    select_btn = Pin(4, Pin.IN, Pin.PULL_UP)
    back_btn = Pin(8, Pin.IN, Pin.PULL_UP) # Middle button (EXIT)
    scroll_btn = Pin(13, Pin.IN, Pin.PULL_UP)
    buzzer = PWM(Pin(15))
    buzzer.duty_u16(0)

    def beep(freq, dur):
        buzzer.freq(freq)
        buzzer.duty_u16(32768)
        time.sleep_ms(dur)
        buzzer.duty_u16(0)

    bird_y = 32
    vel_y = 0
    pipe_x = 128
    gap_y = random.randint(10, 35)
    
    # EASIER: Increased gap size from 22 to 32 pixels
    gap_size = 32 
    
    score = 0
    game_over = False
    last_flap = False

    while True:
        if not back_btn.value():
            while not back_btn.value(): time.sleep_ms(10)
            return

        if game_over:
            display.fill(0)
            display.text("GAME OVER", 28, 15, 1)
            display.text(f"Score: {score}", 35, 30, 1)
            display.text("Middle btn: EXIT", 0, 50, 1)
            display.show()
            time.sleep(0.5)
            while True:
                if not back_btn.value(): return
                if not select_btn.value() or not scroll_btn.value():
                    bird_y, vel_y, pipe_x, score = 32, 0, 128, 0
                    gap_y = random.randint(10, 35)
                    game_over = False
                    break
                time.sleep_ms(50)
            continue

        flap_pressed = not select_btn.value() or not scroll_btn.value()
        if flap_pressed and not last_flap:
            # EASIER: Slightly gentler flap
            vel_y = -3.8 
            beep(1000, 20)
        last_flap = flap_pressed

        # EASIER: Lowered gravity so the bird falls a bit slower
        vel_y += 0.45 
        bird_y += vel_y

        # EASIER: Slowed down the pipe movement from 4 to 3
        pipe_x -= 3 
        if pipe_x < -10:
            pipe_x = 128
            gap_y = random.randint(10, 35)
            score += 1
            beep(1500, 20)

        # Collision mechanics
        if bird_y < 0 or bird_y > 60:
            beep(200, 300)
            game_over = True
        
        if (pipe_x < 26 and pipe_x > 10):
            if bird_y < gap_y or bird_y + 6 > gap_y + gap_size:
                beep(200, 300)
                game_over = True

        # Draw frame
        display.fill(0)
        display.text(f"{score}", 60, 0, 1)
        display.fill_rect(20, int(bird_y), 6, 6, 1) # Draw Bird
        display.fill_rect(int(pipe_x), 0, 10, gap_y, 1) # Draw Top Pipe
        display.fill_rect(int(pipe_x), gap_y + gap_size, 10, 64 - (gap_y + gap_size), 1) # Draw Bottom Pipe
        display.show()
        time.sleep_ms(30)