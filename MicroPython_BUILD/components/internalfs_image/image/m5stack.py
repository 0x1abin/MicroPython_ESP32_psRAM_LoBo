from micropython import const
import machine, ubinascii
import uos as os
import utime as time
import display as lcd
import utils
from m5button import M5Button

VERSION = "v0.4.3"

_BUTTON_A_PIN = const(39)
_BUTTON_B_PIN = const(38)
_BUTTON_C_PIN = const(37)
_SPEAKER_PIN  = const(25)


class Speaker:
  def __init__(self, pin=25, volume=5):
    self.pwm = machine.PWM(machine.Pin(pin), freq = 1, duty = 0, timer = 2)
    self._timer = 0
    self._volume = volume
    self._blocking = True
    self._beat_time = 500

  def _timeout_cb(self, timer):
    self._timer.deinit()
    self.pwm.duty(0)
    time.sleep_ms(1)
    self.pwm.freq(1)

  def tone(self, freq=1800, duration=200, volume=None):
    if volume == None:
      self.pwm.init(freq=freq, duty=self._volume)
    else:
      self.pwm.init(freq=freq, duty=volume)
    if duration > 0:
      if self._blocking:
        time.sleep_ms(duration)
        self.pwm.duty(0)
        time.sleep_ms(1)
        self.pwm.freq(1)
      else:
        self._timer = machine.Timer(8)
        self._timer.init(period=duration, mode=self._timer.ONE_SHOT, callback=self._timeout_cb)   

  def sing(self, freq=1800, beat=1, volume=None):
    self.tone(freq, int(beat*self._beat_time), volume)
  
  def set_beat(self, value=120):
    self._beat_time = int(60000 / value)

  def volume(self, val):
    self._volume = val

  def setblocking(self, val=True):
    self._blocking = val

def fimage(x, y, file, type=1):
  if file[:3] == '/sd':
    utils.filecp(file, '/flash/fcache', blocksize=8192)
    lcd.image(x, y, '/flash/fcache', 0, type)
    os.remove('/flash/fcache')
  else:
    lcd.image(x, y, file, 0, type)

class RGB_Bar:
  def __init__(self):
    self.led_bar = machine.Neopixel(15, 10)
  
  def set_dir(self, dir, color):
    if dir == 'left':
      for i in range(6, 11):
        self.led_bar.set(i, color)
        time.sleep_ms(5)
    else:
      for i in range(1, 6):
        self.led_bar.set(i, color)
        time.sleep_ms(5)
  
  def set(self, number, color):
    self.led_bar.set(number, color)
  
  def set_all(self, color):
    for i in range(1, 11):
      self.led_bar.set(i, color)
      time.sleep_ms(5)

rgb = RGB_Bar()
rgb.set_all(0)

def delay(ms):
  time.sleep_ms(ms)

def map_value(value, input_min, input_max, aims_min, aims_max):
  value_deal = value * (aims_max - aims_min) / (input_max - input_min) + aims_min
  value_deal = value_deal if value_deal < aims_max else aims_max
  value_deal = value_deal if value_deal > aims_min else aims_min
  return value_deal

# ------------------ M5Stack -------------------
# Node ID
node_id = ubinascii.hexlify(machine.unique_id()).decode('utf-8')
print('\nDevice ID:' + node_id)
print('LCD initializing...', end='')

# pin Analog and digital

# LCD
lcd = lcd.TFT()
lcd.init(lcd.M5STACK, width=240, height=320, speed=40000000, rst_pin=33, 
         miso=19, mosi=23, clk=18, cs=14, dc=27, bgr=True,invrot=3, 
         expwm=machine.PWM(32, duty=0, timer=1))
lcd.setBrightness(30)
lcd.clear()
lcd.setColor(0xCCCCCC)
print('Done!')

# lcd.println('M5Stack MicroPython '+VERSION, 0, 0)
# lcd.println('Device ID:'+node_id)
# lcd.println('Boot Mode:')
# lcd.println('Hold button A to boot into SAFE mode.')
# lcd.println('Hold button B to boot into OFFLINE mode.')
# lcd.print('Boot...', 0, 0)
# try:
#   # lcd.image(0, 0, '/flash/img/m5.jpg')
#   lcd.image(0, 0, '/flash/img/1-1.jpg')
#   lcd.rect(0, 190, 320, 50, lcd.WHITE, lcd.WHITE)
#   lcd.setBrightness(500)
# except:
#   pass
# if not utils.exists('/flash/img/1-1.jpg'):
#   lcd.print('M5GO resource file not found!\n', 0, 0, color=lcd.RED)
#   lcd.print('Please upload to the Internal Filesystem.\n', color=lcd.RED)
#   lcd.print('https://github.com/m5stack/M5GO\n', color=lcd.RED)
#   lcd.setBrightness(300)


# BUTTON
buttonA = M5Button(_BUTTON_A_PIN)
buttonB = M5Button(_BUTTON_B_PIN)
buttonC = M5Button(_BUTTON_C_PIN)

def button_timer(timer):
  buttonA.read()
  buttonB.read()
  buttonC.read()

t1 = machine.Timer(7)
t1.init(period=20, callback=button_timer)

# SPEAKER
speaker = Speaker()
