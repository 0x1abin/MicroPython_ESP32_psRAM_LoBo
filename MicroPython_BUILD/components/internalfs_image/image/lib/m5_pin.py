from machine import ADC
from machine import PWM
from machine import Pin

class M5_Pin:
    def __init__(self):
        self._pin_adc_map = {}
        self._pin_pwm_map = {}
        self._pin_io_map = {}
        self._ATTN = ADC.ATTN_11DB
        self._WIDTH = ADC.WIDTH_12BIT

    def analogRead(self, pin):
        if str(pin) not in self._pin_adc_map.keys():
            try:
                self._pin_adc_map[str(pin)] = ADC(pin)
                self._pin_adc_map[str(pin)].atten(self._ATTN)
                self._pin_adc_map[str(pin)].width(self._WIDTH)
            except:
                return 0

        data = self._pin_adc_map[str(pin)].read()
        ad_data = int(data * 1024 / 3300)
        return ad_data
    
    # pin:21,23,25,27,4,19,22,26
    def analogWrite(self, pin, duty, pwm = 500):
        _width = duty * 100 / 1024
        if str(pin) not in self._pin_pwm_map.keys():
            try:
                self._pin_pwm_map[str(pin)] = PWM(pin, freq=pwm, duty=_width)
                return 1
            except:
                return 0
        else:
            self._pin_pwm_map[str(pin)].duty(_width)
            return 1
    
    def pin_mode(self, pin, mode, pull=Pin.PULL_FLOAT):
        if str(pin) not in self._pin_io_map.keys():
            self._pin_io_map[str(pin)] = Pin(pin, mode=mode, pull=pull)
        else:
            self._pin_io_map[str(pin)].init(mode=mode, pull=pull)
        
    def digitalWrite(self, pin, value):
        if str(pin) not in self._pin_io_map.keys():
            self._pin_io_map[str(pin)] = Pin(pin, mode=Pin.OUT)
        self._pin_io_map[str(pin)].value(value)
        
    def digitalRead(self, pin):
        if str(pin) not in self._pin_io_map.keys():
            self._pin_io_map[str(pin)] = Pin(pin, mode=Pin.IN)
        return self._pin_io_map[str(pin)].value()


