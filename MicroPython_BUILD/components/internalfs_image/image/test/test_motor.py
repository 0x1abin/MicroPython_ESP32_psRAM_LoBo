import machine
import ustruct

i2c = machine.I2C(sda=21, scl=22)

def set_motor(m0_pwm):
    buf = ustruct.pack('<hh', int(m0_pwm), int(55))
    i2c.writeto_mem(0x56, 0, buf)


import i2c_bus, ustruct
i2c = i2c_bus.get(i2c_bus.M_BUS)

i2c.writeto_mem(0x56, 0x00, ustruct.pack('<h', 200))
buf = bytearray(4)
i2c.readfrom_mem_into(0x56, 0x00, 4)
