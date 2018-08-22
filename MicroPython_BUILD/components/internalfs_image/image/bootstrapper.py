import gc
import uos as os
import ubinascii
from m5stack import lcd, buttonC, speaker
from utils import *
from config import config

# Beep
speaker.tone(500)

# Reset apikey
if buttonC.isPressed():
    uos.remove('apikey.pem')


# Connect network
import wifisetup
wifisetup.auto_connect()


# Read apikey
try:
    f = open('apikey.pem', 'r')
except:
    apikey = ubinascii.hexlify(os.urandom(3)).decode('utf8') #Random APIKEY
    apikey = apikey.upper()
    f = open('apikey.pem', 'w')
    f.write(apikey)
else:
    apikey = f.read()
finally:
    f.close()


# Display 
lcd.clear(lcd.BLACK)
lcd.font(lcd.FONT_DejaVu24)
lcd.fillRect(0, 0, 320, 30, lcd.BLUE)
lcd.setTextColor(lcd.WHITE, lcd.BLUE)
lcd.print(" Flow.m5stack.com", 0, 5, lcd.WHITE)

# apikey qrcode
lcd.font(lcd.FONT_DejaVu18)
lcd.setTextColor(0xaaaaaa, lcd.BLACK)
lcd.println("APIKEY", 25, 120)
lcd.font(lcd.FONT_DejaVu24)
lcd.print(apikey, 12, 138, color=lcd.ORANGE)
lcd.qrcode(config['qrcode_url'] + apikey, 126, 46, 175)


# ingre main
if exists('main.py'):
    if exists('_main.py'):
        os.remove('_main.py')
    os.rename('main.py', '_main.py')

gc.collect()
