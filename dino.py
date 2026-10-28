from machine import Pin, I2C, PWM
import time
import ssd1306

def run():
    i2c = I2C(1, sda=Pin(26), scl=Pin(27), freq=400000)
    display = ssd1306.SSD1306_I2C(128, 64, i2c)
    select_btn = Pin(4, Pin.IN, Pin.PULL_UP)
    back_btn = Pin(8, Pin.IN, Pin.PULL_UP)
    scroll_btn = Pin(13, Pin.IN, Pin.PULL_UP)
    buzzer = PWM(Pin(15))
    buzzer.duty_u16(0)

    def beep(freq, dur):
        buzzer.freq(freq)
        buzzer.duty_u16(32768)
        time.sleep_ms(dur)
        buzzer.duty_u16(0)

    dino_y = 40
    vel_y = 0
    is_jumping = False
    cactus_x = 128
    score = 0
    speed = 4.0
    game_over = False

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
                    dino_y, vel_y, cactus_x, score, speed = 40, 0, 128, 0, 4.0
                    game_over, is_jumping = False, False
                    break
                time.sleep_ms(50)
            continue

        if (not select_btn.value() or not scroll_btn.value()) and not is_jumping:
            vel_y = -8  # Stronger initial jump
            is_jumping = True
            beep(800, 30)

        vel_y += 1.2 # Stronger gravity for faster fall
        dino_y += vel_y
        if dino_y >= 40:
            dino_y = 40
            is_jumping = False

        cactus_x -= int(speed)
        if cactus_x < -10:
            cactus_x = 128
            score += 1
            # Speed ramps up significantly faster as score increases
            speed += 0.5 if speed < 12 else 0 
            beep(1200, 20)

        if (cactus_x < 20 and cactus_x > 2) and dino_y > 30:
            beep(200, 300)
            game_over = True

        display.fill(0)
        display.hline(0, 50, 128, 1)
        display.text(f"{score}", 110, 0, 1)
        display.fill_rect(10, int(dino_y), 10, 10, 1)
        display.fill_rect(int(cactus_x), 40, 8, 10, 1)
        display.show()
        time.sleep_ms(30)