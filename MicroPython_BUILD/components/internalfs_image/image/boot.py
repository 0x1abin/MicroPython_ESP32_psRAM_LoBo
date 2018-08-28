# This file is executed on every boot (including wake-boot from deepsleep)
import sys
import gc
import uos as os
import utime as time

# Set default path
# Needed for importing modules and upip
sys.path[1] = '/flash/lib'


# boot view
from m5stack import *
lcd.setBrightness(300)
lcd.image(lcd.CENTER, lcd.CENTER, 'img/uiflow_logo_80x80.bmp')
lcd.setColor(0xCCCCCC, 0)
lcd.print('UPLOAD', 40, 225)
lcd.print('APP.LIST', 130, 225)
lcd.print('Wi-Fi', 235, 225)
lcd.setCursor(0, 0)

cnt_down = time.ticks_ms() + 2000
while time.ticks_ms() < cnt_down:
    if buttonA.isPressed():   # M5Cloud upload
        speaker.tone(2000, 50, volume=1) # Beep
        import bootstrapper

    elif buttonB.isPressed(): # APP list
        pass

    elif buttonC.isPressed(): # WiFi setting
        import wificonfig
        wificonfig.webserver_start()


gc.collect()
