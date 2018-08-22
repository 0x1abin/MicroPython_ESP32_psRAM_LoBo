# This file is executed on every boot (including wake-boot from deepsleep)
import sys
import gc
import uos as os

# Set default path
# Needed for importing modules and upip
sys.path[1] = '/flash/lib'

# Start
from m5stack import lcd,buttonA
from utils import *
lcd.setBrightness(300)

# Connect M5Cloud
if buttonA.isPressed():
    import bootstrapper
    from m5cloud import M5Cloud
    from config import config
    m5cloud = M5Cloud(token=bootstrapper.apikey, server=config['mqtt']['server'], port=config['mqtt']['port'])
    m5cloud.run(thread=True)
else:
    if exists('_main.py') and not exists('main.py'):
        os.rename('_main.py', 'main.py')

gc.collect()
