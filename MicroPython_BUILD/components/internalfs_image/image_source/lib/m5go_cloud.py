from m5stack import lcd, node_id
import network
import gc
import utime as time
import mtftp
import _thread


def m5go_run(buffer):
    exec(buffer, globals())


def conncb(task):
    print("[{}] M5Cloud connected.".format(task))
    mqtt.subscribe('M5-' + node_id + '-I')
    mqtt.subscribe('M5GO-' + node_id + '-run')


def disconncb(task):
    print("[{}] Disconnected".format(task))
    from wifisetup import wlan_sta
    while not wlan_sta.isconnected():
        print('.', end='')
        time.sleep(1)
    mqtt.start()


def datacb(msg):
    # print("[{}] Data arrived from topic: {}, Message:\n".format(msg[0], msg[1]), msg[2])
    topic = msg[1]
    if topic[-3:] == 'run':
        buffer = msg[2].decode('utf-8')
        _thread.start_new_thread('m5go_run', m5go_run, (buffer,))
    else:
        mtftpc.recv_handle(msg[2])


mqtt = network.mqtt(name='M5-'+node_id,
                    server="mqtt.m5stack.com",
                    port=1883,
                    autoreconnect=True,
                    clientid='M5-'+node_id,
                    keepalive=30,
                    connected_cb=conncb,
                    disconnected_cb=disconncb,
                    data_cb=datacb)

# mqtt.start()

mtftpc = mtftp.MTFTP(lambda packet: mqtt.publish('M5-'+node_id+'-O', packet))


def isconnected():
    if mqtt.status()[0] == 1:
        return True
    else:
        return False


def idle():
    return mtftpc.isidle()


gc.collect()
