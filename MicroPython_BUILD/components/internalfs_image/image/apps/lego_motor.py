from m5stack import *
import utime as time
from lego_board import Lego_Motor 

motor = Lego_Motor()

lcd.clear()
lcd.setColor(lcd.WHITE)

def lcd_text_button(number, message):
    x_pos = 0
    if number == 'A':
        x_pos = 62
    elif number == 'B':
        x_pos = 159
    elif number == 'C':
        x_pos = 253
    lcd.text(x_pos - int(lcd.textWidth(message) / 2), 235 - lcd.fontSize()[1], message)

lcd.print('lego motor test', lcd.CENTER, 110)
lego = motor.register(1)

def speed_test():
    motor_flag = True
    time_now = time.ticks_ms()
    lego.set_speed(12)
    while True:
        if time.ticks_ms() - time_now > 2000:
            time_now = time.ticks_ms()
            if motor_flag:
                motor_flag = False
                lego.set_speed(-12)
            else:
                motor_flag = True
                lego.set_speed(12)
        if buttonB.wasPressed():
            lego.release()
            break
        time.sleep_ms(100)

def angle_test():
    motor_flag = True
    lego.set_angle_zero()
    time_now = time.ticks_ms()
    lego.set_angle(360)
    while True:
        if time.ticks_ms() - time_now > 2000:
            time_now = time.ticks_ms()
            if motor_flag:
                motor_flag = False
                lego.set_angle(-360)
            else:
                motor_flag = True
                lego.set_angle(360)
        if buttonB.wasPressed():
            lego.release()
            break
        time.sleep_ms(100)        

while True:
    if not lego.scan():
        lcd.print('not found motor', lcd.CENTER, 130)
    else:
        lcd_text_button('A', 'speed test')
        lcd_text_button('B', 'stop')
        lcd_text_button('C', 'angle test')
        while True:
            if buttonA.wasPressed():
                speed_test()
            elif buttonC.wasPressed():
                angle_test()
            time.sleep_ms(10)
    time.sleep(1)


