from m5stack import *
import machine
import ujson
import utime
import ubinascii
import uhashlib
import urequests
import logging
from config import config as cfg

# Create global logger for debug messages.
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

'''
host：http://10.0.0.184:7788
注册激活码：/m5cloud/device/regcheckcode
查询激活状态：/m5cloud/device/regstate
确定激活状态：/m5cloud/device/confirm
'''
HOST = "http://io2.m5stack.com:16666"


def private_sign(data, m5pkey="08260529"):
    chipid = ubinascii.hexlify(machine.unique_id()).decode('utf-8')
    sign = uhashlib.sha256(m5pkey + chipid + data)
    return ubinascii.hexlify(sign.digest()).decode("utf-8")


def generate_json(signature):
    r_json = {"chipid": ubinascii.hexlify(machine.unique_id()).decode('utf-8')}
    r_json["signature"] = signature
    return r_json


def start_register():
    reg_state = "POST_CODE"
    apikey_idx = None
    apikey = ''
    lcd.setColor(lcd.BLACK, lcd.WHITE)
    while True:
        if reg_state == "POST_CODE":
            logger.debug("POST_CODE")
            checkcode = "%06d" % machine.random(999999)
            timestamp = str(int(utime.time()))
            req_json = generate_json(private_sign(timestamp))
            req_json["timestamp"] = timestamp
            req_json["checkcode"] = checkcode
            req_json["version"] = cfg["version"]
            req_json["type"] = cfg["type"]
            logger.debug(req_json)
            r = urequests.post(HOST + "/m5cloud/device/regcheckcode", json=req_json)
            if r.status_code == 200: # get the APIKEY index id
                resp = r.json()
                apikey_idx = resp["data"]
                reg_state = "WAIT_KEY"
                # LCD display check code
                print('Your Check Code is:' + checkcode +
                        ' (60 second refresh), use it add device at http://io2.m5stack.com')
                lcd.clear(lcd.BLACK)
                lcd.font(lcd.FONT_DejaVu24, transparent=True)
                lcd.println('Check Code:' + checkcode, lcd.CENTER, 100, lcd.ORANGE)
                lcd.font(lcd.FONT_Default)
                lcd.println('add device at http://io2.m5stack.com', lcd.CENTER, 130, 0xCCCCCC)
            elif r.status_code == 204:  # registered
                print("Device is be registered!")
            elif r.status_code == 400:  # signature invalid
                print("signature invalid")
            elif r.status_code == 205:  # check code exist generate
                pass
            r.close()
            utime.sleep(2)

        elif reg_state == "WAIT_KEY":
            logger.debug("WAIT_KEY")
            r = urequests.get(HOST + "/m5cloud/device/regstate?urlcode=" + apikey_idx)
            if r.status_code == 200:  # get APIKEY
                resp = r.json()
                apikey = resp["data"]
                reg_state = "BTN_CONFIRM"
                lcd.font(lcd.FONT_DejaVu18)
                lcd.print('Press button to confirm register', lcd.CENTER, 210, 0xCCCCCC)
            elif r.status_code == 202:  # wait type add device
                pass
            elif r.status_code == 404:  # Invalid or past due
                reg_state = "POST_CODE"
            r.close()
            utime.sleep(2)

        elif reg_state == "BTN_CONFIRM":
            logger.debug("BTN_CONFIRM")
            # Wait pressed button to confirm register
            if buttonA.isPressed() or buttonB.isPressed() or buttonC.isPressed():
                timestamp = str(int(utime.time()))
                req_json = generate_json(private_sign(timestamp+apikey))
                req_json["timestamp"] = timestamp
                req_json["type"] = cfg["type"]
                req_json["version"] = cfg["version"]
                logger.debug(req_json)
                r = urequests.post(HOST + "/m5cloud/device/confirm", json=req_json)
                if r.status_code == 200:  # Confirm!
                    reg_state = "SAVE_APIKEY"
                else:
                    reg_state = "POST_CODE"
                r.close()
            utime.sleep(0.2)

        elif reg_state == "SAVE_APIKEY":
            logger.debug("SAVE_APIKEY")
            return apikey


def except_display(ept):
    lcd.clear(lcd.BLACK)
    lcd.font(lcd.FONT_DejaVu24)
    lcd.println("Except:", 0, 0, lcd.RED)
    lcd.font(lcd.FONT_DejaVu18)
    lcd.print(repr(ept), color=0xDDDDDD)


def random_apikey():
    import uos
    return ubinascii.hexlify(uos.urandom(16)).decode('utf8')