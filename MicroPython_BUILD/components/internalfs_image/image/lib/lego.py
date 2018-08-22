from micropython import const
import uos as os
import utime as time
import machine
import ustruct
import i2c_bus


M5GO_WHEEL_ADDR = const(0x56)
MOTOR_CTRL_ADDR = const(0x00)
ENCODER_ADDR = const(0x04)

motor1_pwm = 0
motor2_pwm = 0


def constrain(amt, low, high):
    if amt < low:
        return low
    if amt > high:
        return high
    return amt


class NXT_Motor:
    def __init__(self, port):
        self.i2c = i2c_bus.get(i2c_bus.M_BUS)
        self.port = port

    def stop(self):
        self.set_pwm(0)

    def set_pwm(self, pwm):
        global motor1_pwm, motor2_pwm
        if self.port == 1:
            motor1_pwm = pwm
        else:
            motor2_pwm = pwm
        buf = ustruct.pack('<hh', int(motor1_pwm), int(motor2_pwm))
        self.i2c.writeto_mem(M5GO_WHEEL_ADDR, MOTOR_CTRL_ADDR, buf)

    def read_encoder(self):
        buf = bytearray(4)
        self.i2c.readfrom_mem_into(M5GO_WHEEL_ADDR, ENCODER_ADDR, buf)
        encoder_buf = tuple(ustruct.unpack('<hh', buf))
        if self.port == 1:
            return encoder_buf[0]
        else:
            return encoder_buf[1]

