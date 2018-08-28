from m5stack import lcd, buttonA, buttonB, buttonC, speaker
import uos as os
import utime as time
from utils import filecp

triangle_last = [5, 19]
def draw_triangle(x, y):
  global triangle_last
  lcd.triangle(triangle_last[0], triangle_last[1], triangle_last[0], triangle_last[1]+7, triangle_last[0]+8, triangle_last[1]+3, lcd.BLACK, lcd.BLACK)
  lcd.triangle(x, y, x, y+7, x+8, y+3, lcd.RED, lcd.RED)
  triangle_last = [x, y]

def file_start():
    global files, files_len, draw_number
    lcd.clear()
    lcd.triangle(59, 228, 67, 215, 75, 228, lcd.WHITE, lcd.WHITE)
    lcd.triangle(233, 215, 241, 228, 249, 215, lcd.WHITE, lcd.WHITE)
    lcd.text(249, 216, '/DEL', lcd.RED)
    # lcd.triangle(247, 215, 255, 228, 263, 215, lcd.GREEN, lcd.GREEN)
    lcd.text(0, 0, 'Select program to run:', lcd.WHITE)
    lcd.text(142, 215, 'RUN', lcd.WHITE)
    files = os.listdir('/flash/apps')
    files_len = len(files)
    for i in range(files_len):
        lcd.text(20, 18 + i*15, files[i], lcd.YELLOW)
    draw_number = 0
    draw_triangle(6, 19)

def file_choose():
    global files, files_len, draw_number
    file_start()
    while True:
        if buttonA.wasReleased():
            draw_number = draw_number - 1 if draw_number > 1 else 0
            draw_triangle(6, 19+draw_number*15)
        elif buttonB.wasReleased():
            filecp('apps/{}'.format(files[draw_number]), 'main.py')
            break
        elif buttonC.wasReleased():
            draw_number = draw_number + 1 if draw_number < (files_len-1) else (files_len - 1)
            draw_triangle(6, 19+draw_number*15)
        elif buttonC.releasedFor(400):
            lcd.clear()
            lcd.text(130, 110, 'delete ?', lcd.RED)
            lcd.text(54, 215, 'YES', lcd.RED)
            lcd.text(246, 215, 'NO', lcd.RED)
            while True:
                if buttonA.wasReleased():
                    os.remove('apps/{}'.format(files[draw_number]))
                    file_start()
                    break
                elif buttonC.wasReleased():
                    file_start()
                    break
                time.sleep_ms(50)               
        time.sleep_ms(50)