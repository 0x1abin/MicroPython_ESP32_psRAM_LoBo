from m5stack import *
from units import ENV
import utime as time

lcd.clear()

while True:
    lcd.font(lcd.FONT_Default)
    while True:
        try:
            th = ENV()
            break
        except:
            lcd.print('check if the sensor is attached', lcd.CENTER, 110)
            time.sleep(0.5)

    lcd.clear()
    lcd.setBrightness(200)
    lcd.font(lcd.FONT_Tooney)

    tem = th.temperature()
    hum = th.humidity()
    tem_last = tem
    hum_last = hum
    while True:
        time.sleep(1)
        try:
            tem = th.temperature()
            hum = th.humidity()
        except:
            break
        lcd.print('T:{}'.format(tem_last), lcd.CENTER, 60, lcd.BLACK)
        lcd.print('H:{}'.format(hum_last), lcd.CENTER, 120, lcd.BLACK)
        lcd.print('T:{}'.format(tem), lcd.CENTER, 60, lcd.ORANGE)
        lcd.print('H:{}'.format(hum), lcd.CENTER, 120, lcd.ORANGE)
        tem_last = tem
        hum_last = hum