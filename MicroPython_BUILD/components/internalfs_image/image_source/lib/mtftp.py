from utils import *
from micropython import const
from m5stack import lcd, node_id
import uos as os
import utime as time
import ustruct, ujson
import machine
import network
import gc

# lcd.image(0, 0, file="dog.jpg", scale=0, type=lcd.JPG)
# print('\nID:' + node_id)

_prev_val = 0
def progress(pgs, x=20, y=180, w=270, h=30):
    global _prev_val
    if _prev_val == pgs:
        return
    _prev_val = pgs
    if pgs < 0:
        pgs = 0
    elif pgs > 100:
        pgs = 100
    pt = pgs * w // 100 + 1
    lcd.rect(x + 1, y + 1, pt - 2, h - 2, 0x666666, 0x666666)
    lcd.rect(x + 1 + pt, y + 1, w - pt - 2, h - 2, 0, 0)
    lcd.rect(x, y, w, h, 0xffffff)
    # if pgs < 55:
    #     lcd.setColor(0xffffff, 0)
    # else:
    #     lcd.setColor(0xffffff, 0x666666)
    # lcd.font(lcd.FONT_Default, fixedwidth=False)
    # lcd.print(('%2d%%' % pgs), lcd.CENTER, y + 10)

_prev_fname = ''
def download_progress(pgs, filename):
    global _prev_fname, _prev_val
    if not filename == _prev_fname:
        lcd.font(lcd.FONT_Default)
        # lcd.print('M5Cloud', lcd.CENTER, 80)
        lcd.setColor(0xffffff, 0)
        lcd.print("Downlonad:" + filename, 20, 160)
        _prev_fname = filename
        _prev_val = 0
    progress(pgs)


_CMD_RRQ   = const(1)
_CMD_WRQ   = const(2)
_CMD_DATA  = const(3)
_CMD_ACK   = const(4)
_CMD_ERROR = const(5)
_CMD_LIST  = const(6)
_CMD_RESET = const(9)

_STA_IDLE  = const(0)
_STA_RRQ   = const(1)
_STA_WRQ   = const(2)
_STA_LIST  = const(3)
_BLOCK_SIZE = const(1024)


class MTFTP():
    def __init__(self, send_pack):
        self.state = _STA_IDLE
        self._send_pack = send_pack
        self._nblock = 0
        self._buffer = 0
        self._filename = ''
        self._fd = 0
        self._shottime = 0
        self._total_block = 0

    def isidle(self):
        return self.state == _STA_IDLE

    def send_packet(self, packet):
        self._send_pack(packet)

    def send_ack(self, block):
        self.send_packet(ustruct.pack('!HH', _CMD_ACK, block))

    def _fileslist(self, path):
        _list = os.listdir(path)
        for i in _list:
            if isfile(path + '/' + i):
                if filesize(path + '/' + i) < 30000:
                    self._buffer.append(path + '/' + i)
            else:
                self._fileslist(path + '/' + i)

    def getfileslist(self, path='/flash'):
        self._buffer = []
        self._fileslist(path)
        ret = self._buffer
        self._buffer = 0
        return ret

    def get_filename(self, packet):
        fidx = 2
        while fidx < 64:
            # if bytes(packet[fidx], 'utf-8') == ustruct.pack('!B', 0):
            if packet[fidx] == 0:
                break
            fidx += 1
        try:
            self._total_block = ustruct.unpack(
                '!H', packet[fidx + 1:fidx + 3])[0]
        except:
            pass
        return packet[2:fidx].decode('utf-8')

    def send_block(self, block, data):
        packet = ustruct.pack('!HH', _CMD_DATA, block)
        packet += data
        self.send_packet(packet)

    def handle_list(self, path):
        flist = self.getfileslist(path)
        # print(flist)
        self.send_block(block=1, data=ujson.dumps(flist))
        self.state = _STA_LIST
        
    def handle_wrq(self, fname):
        gc.collect()
        # print('Start write file:')
        print('[M5Cloud] Downloading:%s  ' % fname, end='')
        self._shottime = time.ticks_ms()
        self._filename = fname
        self._nblock = 1
        self.state = _STA_WRQ
        try:
            self._fd.close()
        except:
            pass
        makedirs(self._filename[:self._filename.rfind('/')])
        self._fd = open(self._filename, 'wb')
        self.send_ack(0)
        lcd.clear()

    def handle_rrq(self, fname):
        gc.collect()
        print('[M5Cloud] Uploading:%s  ' % fname, end='')
        if exists(fname):
            self._total_block = filesize(fname) // _BLOCK_SIZE + 1
            self._shottime = time.ticks_ms()
            self._filename = fname
            self._nblock = 1
            self.state = _STA_RRQ
            try:
                self._fd.close()
            except:
                pass
            self._fd = open(fname, 'rb')
            self.send_block(self._nblock, self._fd.read(_BLOCK_SIZE))
            # self._buffer = self._fd.read(_BLOCK_SIZE)
        else:
            print("rrq file isn't exists")
            pass

    def recv_handle(self, packet):
        # print("-------------- Recv Packet size:%4d free mem:%6d --------------" % (len(packet), gc.mem_free()))
        # print(packet)
        # print("----------------------------- End ----------------------------------")
        cmd = ustruct.unpack('!H', packet[:2])[0]
        # print('CMD:%d' % (cmd))
        if cmd == _CMD_RRQ:
            self.handle_rrq(self.get_filename(packet))
        elif cmd == _CMD_WRQ:
            self.handle_wrq(self.get_filename(packet))
        elif cmd == _CMD_DATA:
            _block = ustruct.unpack('!H', packet[2:4])[0]
            # print('DATA Block:%d' % _block)
            print('.', end='')
            if self._nblock == _block:
                self._nblock += 1
                download_progress(
                    _block * 100 // self._total_block, self._filename)
                # _data = packet[4:]
                self._fd.write(packet[4:])  # write data
                # print('Block size:%d' % len(_data))
                if len(packet[4:]) < _BLOCK_SIZE:
                    self._fd.close()
                    self._fd = 0
                    self.state = _STA_IDLE
                    usedtime = (time.ticks_ms() - self._shottime)
                    print('')
                    # print('\nBlock Total:%d   Time:%dms   Speed: %d byte/s' % (_block, usedtime, (filesize(self._filename)*1000 // usedtime)))
                    # print('Done.\n')
                self.send_ack(_block)

        elif cmd == _CMD_ACK:
            _block = ustruct.unpack('!H', packet[2:4])[0]
            # print('ACK Block:%d' % block)
            if self.state == _STA_RRQ:
                if _block == self._nblock:
                    print('.', end='')
                    self._nblock += 1
                    self._buffer = self._fd.read(_BLOCK_SIZE)
                    if len(self._buffer) == 0:
                        self._fd.close()
                        self._fd = 0
                        self._buffer = 0
                        self.state = _STA_IDLE
                        self.send_block(0xFFFF, bytes(0)) # send the single for pull operate
                        usedtime = (time.ticks_ms() - self._shottime)
                        print('')
                        # print('\nBlock Total:%d   Time:%0dms   Speed: %d byte/s' % (_block, usedtime, (filesize(self._filename)*1000 // usedtime)))
                        # print('Done!\n')
                    else:
                        self.send_block(self._nblock, self._buffer)
            elif self.state == _STA_LIST:
                self.send_block(0xFFFF, bytes(0))
                self.state = _STA_IDLE

        elif cmd == _CMD_LIST:
            self.handle_list(self.get_filename(packet))
        
        elif cmd == _CMD_RESET:
            # lcd.font(lcd.FONT_DejaVu24)
            # lcd.rect(10, 80, 300, 30, 0, 0)
            # lcd.print('RESTART...', lcd.CENTER, 80)
            machine.reset()
        # gc.collect()

# Start
