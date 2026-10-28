from machine import Pin, I2C, PWM
import time
import ssd1306

i2c = I2C(1, sda=Pin(26), scl=Pin(27), freq=400000)
display = ssd1306.SSD1306_I2C(128, 64, i2c)
select_btn = Pin(4, Pin.IN, Pin.PULL_UP)
scroll_btn = Pin(13, Pin.IN, Pin.PULL_UP)
buzzer = PWM(Pin(15))
buzzer.duty_u16(0)

def beep():
    buzzer.freq(1000)
    buzzer.duty_u16(32768)
    time.sleep_ms(40)
    buzzer.duty_u16(0)

# Swapped Paddle Catch for Flappy Bird
games = ["Dino Runner", "Flappy Bird", "Pancake Catch"]
selected = 0

while True:
    display.fill(0)
    display.text("MAIN MENU", 28, 0, 1)
    
    for i, game in enumerate(games):
        y = 20 + (i * 15)
        if i == selected:
            display.fill_rect(5, y - 2, 118, 12, 1)
            display.text(game, 10, y, 0)
        else:
            display.text(game, 10, y, 1)
    display.show()

    if not scroll_btn.value():
        beep()
        selected = (selected + 1) % len(games)
        time.sleep_ms(200)

    if not select_btn.value():
        beep()
        display.fill(0)
        display.text("LOADING...", 25, 30, 1)
        display.show()
        
        while not select_btn.value():
            time.sleep_ms(10)
        
        # Load the newly indexed games
        if selected == 0:
            import dino
            dino.run()
        elif selected == 1:
            import flappy
            flappy.run()
        elif selected == 2:
            import pancake
            pancake.run()