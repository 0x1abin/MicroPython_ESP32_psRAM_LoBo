from machine import Pin
from machine import Timer
from time import ticks_ms

class M5Button:
    def __init__(self, pin, invert=True, dbTime=10):
        self._invert =invert
        self._dbTime = dbTime
        self._pin = Pin(pin, mode=Pin.IN)
        self._state = 1
        self._laststate = 1
        self._change = False
        self._press = False
        self._reless = False
        self._press_clear = 0
        self._reless_clear = 0
        self._callback_pr = None
        self._callback_re = None
        self._time_press = 0
        self._time = 0
        self._longrelese = False

    def read(self):
        self._laststate = self._state
        self._state = self._pin.value()
        
        if self._change == True:
            self._change = False
            if self._state == self._laststate:
                if self._state:
                    if self._time and (ticks_ms() - self._time_press) > self._time:
                        self._longrelese = True
                    else: 
                        if self._callback_re:
                            self._callback_re()
                        self._reless = True
                        self._reless_clear = 50
                else:
                    if self._callback_pr:
                        self._callback_pr()
                    self._time_press = ticks_ms()
                    self._press = True
                    self._press_clear = 50
        
        if self._state != self._laststate:
            self._change = True

        if self._press_clear:
            self._press_clear -= 1
        else:
            self._press = False
        
        if self._reless_clear:
            self._reless_clear -= 1
        else:
            self._reless = False

    def wasPressed(self, callback=None):
        if callback:
            self._callback_pr = callback
        else:
            data = self._press
            self._press = False
            return data
    
    def wasReleased(self, callback=None):
        if callback:
            self._callback_re = callback
        else:
            data = self._reless
            self._reless = False
            return data

    def releasedFor(self, time=500, callback=None):
        self._time = time
        data = self._longrelese
        self._longrelese = False
        return data

    def isPressed(self):
        return not self._pin.value()

    def isReleased(self):
        return self._pin.value()

        


