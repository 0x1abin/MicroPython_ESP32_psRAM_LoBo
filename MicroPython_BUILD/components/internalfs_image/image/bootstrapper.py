import gc
import uos as os
import ubinascii
from m5stack import lcd, buttonC
from utils import *
from config import config


# Reset apikey
if buttonC.isPressed():
    os.remove('apikey.pem')


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

# M5Cloud
from m5cloud import M5Cloud
from config import config
m5cloud = M5Cloud(token=apikey, server=config['mqtt']['server'], port=config['mqtt']['port'])
m5cloud.run(thread=False)


gc.collect()
