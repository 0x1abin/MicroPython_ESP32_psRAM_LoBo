#!/usr/bin/env python3
import uos as os
import machine
import gc
import utime as time
import ujson as json
import ubinascii
from micropython import const
from umqtt.simple import MQTTClient
from m5stack import *
import network

wlan_sta = network.WLAN(network.STA_IF)

__VERSION__ = 0.01

# State machine const
STA_IDLE = const(0)
STA_BUSY = const(1)
STA_UPLOAD = const(2)
STA_DOWNLOAD = const(3)

# ============ M5Cloud Client ============
class M5Cloud:
    def __init__(self, token, server="mqtt.m5stack.com", port=1883):
        self.token = token
        self.state = STA_IDLE
        self._task_period = 0
        self._task_millis = 0
        self._user_task = None
        self._exec_out = self.token + "-O/EXEC"
        self._data_out = self.token + "-O/DATA"
        self._context = {}
        self._server_ctx = {"_ctx": self._context,
                            "_set_user_task": self.set_user_task,
                            "_respond": self.exec_respond,
                            "_send_data": self.send_data}

        self.chipid = ubinascii.hexlify(machine.unique_id()).decode("utf-8")
        self.mqtt = MQTTClient('M5-'+self.chipid, server, port)

    # def on_connect(self, param):
    def on_connect(self):
        # print("[{}] M5Cloud connected.".format(param))
        self.mqtt.subscribe(self.token + "-I/EXEC")
        self.mqtt.subscribe(self.token + "-I/DATA")

    # def on_data(self, msg):
    def on_data(self, topic, data):
        self.state = STA_BUSY
        topic = topic if type(topic) == str else topic.decode('utf-8')
        event = topic.split('/')[-1]
        if event == "EXEC":
            data = data if type(data) == str else data.decode('utf-8')
            # print("================ EXEC Handle ==================")
            # print(data)
            try:
                exec(data, globals(), self._server_ctx)
            except Exception as e:
                print('Exception:\n' + repr(e))
                self.exec_respond('Exception')
                self.exec_respond(repr(e))
        elif event == "DATA":
            try:
                self._context["io"].write(data)
            except:
                self.exec_respond("ERROR")
            else:
                self.exec_respond("OK")
        self.state = STA_IDLE

    def exec_respond(self, data):
        self.mqtt.publish(self._exec_out, data)

    def send_data(self, data):
        self.mqtt.publish(self._data_out, data)

    def set_user_task(self, task, ms_period=None):
        self._user_task = task
        self._task_period = ms_period
        self._task_millis = time.ticks_ms() + ms_period

    def _run_task(self):
        if self._user_task:
            if self._task_period:
                if time.ticks_ms() > self._task_millis:
                    self._task_millis = time.ticks_ms() + self._task_period
                    self._user_task(self._context)
            else:
                self._user_task(self._context)
        else:
            time.sleep(1)

    def _pind(self, param):
        self.mqtt.ping()

    def _backend(self):
        self.timeshot = time.ticks_ms() + 1000*60
        t1 = machine.Timer(2)
        t1.init(period=30000, mode=t1.PERIODIC, callback=self._pind)
        while True:
            if not wlan_sta.isconnected():
                print("M5Cloud disconnected.")
                while not wlan_sta.isconnected():
                    time.sleep(1)
                self.mqtt.connect()
                print("M5Cloud connected.")

            self.mqtt.wait_msg()
            time.sleep(0.1)
            # self.mqtt.check_msg()
            # time.sleep(0.1)
            # if time.ticks_ms() > self.timeshot:
            #     self.mqtt.ping()
            #     self.timeshot = time.ticks_ms() + 30000
                # print("ping")

    def run(self, thread=True):
        self.mqtt.DEBUG = True
        self.mqtt.set_callback(self.on_data)
        self.mqtt.connect()
        self.on_connect()
        print("M5Cloud connected.")
        if thread:
            import _thread
            _thread.start_new_thread('M5Cloud_backend', self._backend, ())
        else:
            self._backend()

        # while False:
        #     # User loop task
        #     if self.state == STA_IDLE:
        #         try:
        #             self._run_task()
        #         except:
        #             self._user_task = None
        #     else:
        #         time.sleep(1)


# ============ Extern startup ==============
# def create(apikey="dc890c453c28e72b5a9f959673bac151", server="mqtt.m5stack.com", port=1883):
#     return M5Cloud(apikey, server, port)
