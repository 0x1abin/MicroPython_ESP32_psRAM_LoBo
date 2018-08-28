import machine
import ustruct

# i2c = machine.I2C(sda=21, scl=22)


import i2c_bus, ustruct
i2c = i2c_bus.get(i2c_bus.M_BUS)


def set_motor(n, pwm):
    i2c.writeto_mem(0x56, 0x00 + n*2, ustruct.pack('<h', pwm))

def read_encoder(n):
    buf = bytearray(4)
    i2c.readfrom_mem_into(0x56, 0x08 + n*4, buf)
    return tuple(ustruct.unpack('<i', buf))[0]



# i2c.writeto_mem(0x56, 0x00, ustruct.pack('<h', 200))
# buf = bytearray(4)
# i2c.readfrom_mem_into(0x56, 0x08, buf)
# tuple(ustruct.unpack('<i', buf))[0]
