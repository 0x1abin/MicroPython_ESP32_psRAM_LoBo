from m5stack import *
import machine
import utime as time

tcounter = 0
lcd.clear()

def tcb(timer):
    global tcounter
    tcounter += 1
    print("[tcb] timer: {} counter: {}".format(timer.timernum(), tcounter))
    lcd.print("[tcb] timer: {} counter: {}".format(timer.timernum(), tcounter), lcd.CENTER, lcd.CENTER)

t1 = machine.Timer(0)
t1.init(period=100, mode=t1.PERIODIC, callback=tcb)

