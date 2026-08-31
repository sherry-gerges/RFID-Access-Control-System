import time
from machine import SPI, Pin


class MFRC522:
    OK = 0
    NOTAGERR = 1
    ERR = 2

    # PCD (Reader) Commands
    PCD_IDLE = 0x00
    PCD_TRANSCEIVE = 0x0C
    PCD_RESETPHASE = 0x0F

    # PICC (Card) Commands
    PICC_REQIDL = 0x26
    PICC_ANTICOLL = 0x93

    def __init__(self, spi, rst_pin, cs_pin, debug=0):
        self.spi = spi
        self.rst = Pin(rst_pin, Pin.OUT)
        self.cs = Pin(cs_pin, Pin.OUT)

        self.cs.value(1)
        self.rst.value(1)
        self.debug = debug
        self.init()

    def _wreg(self, reg, val):
        aByteTxArray = bytearray([(reg << 1) & 0x7E, val])
        self.cs.value(0)
        self.spi.write(aByteTxArray)
        self.cs.value(1)

    def _rreg(self, reg, read_len=1):
        aByteTxArray = bytearray([((reg << 1) & 0x7E) | 0x80])
        self.cs.value(0)
        self.spi.write(aByteTxArray)
        back = self.spi.read(read_len)
        self.cs.value(1)
        return back if read_len > 1 else back[0]

    def _set_bit(self, reg, mask):
        self._wreg(reg, self._rreg(reg) | mask)

    def _clear_bit(self, reg, mask):
        self._wreg(reg, self._rreg(reg) & (~mask))

    def init(self):
        self.rst.value(0)
        time.sleep_ms(50)
        self.rst.value(1)
        time.sleep_ms(50)

        self._wreg(0x01, self.PCD_RESETPHASE)
        time.sleep_ms(50)

        self._wreg(0x2A, 0x8D)
        self._wreg(0x2B, 0x3E)
        self._wreg(0x2D, 30)
        self._wreg(0x2C, 0)
        self._wreg(0x15, 0x40)
        self._wreg(0x11, 0x3D)

        self._set_bit(0x14, 0x03)

    def _tcom(self, cmd, send):
        back = []
        bits = 0
        wait_irq = 0x30 if cmd == self.PCD_TRANSCEIVE else 0x10

        self._wreg(0x02, 0x77 | 0x80)
        self._clear_bit(0x04, 0x80)
        self._set_bit(0x01, 0x80)  # Flush FIFO
        self._wreg(0x02, 0x77)

        for c in send:
            self._wreg(0x09, c)

        self._wreg(0x01, cmd)

        if cmd == self.PCD_TRANSCEIVE:
            self._set_bit(0x0D, 0x80)

        i = 1000
        while i > 0:
            n = self._rreg(0x04)
            i -= 1
            if (n & 0x01) or (n & wait_irq):
                break

        self._clear_bit(0x0D, 0x80)

        if i == 0 or (self._rreg(0x06) & 0x17) != 0x00:
            return self.ERR, back, bits

        if cmd == self.PCD_TRANSCEIVE:
            n = self._rreg(0x0A)
            if n > 0:
                if n > 16:
                    n = 16
                back = self._rreg(0x09, n)

            last_bits = self._rreg(0x0C) & 0x07
            bits = (n - 1) * 8 + last_bits if last_bits else n * 8

        return self.OK, back, bits

    def request(self, mode=PICC_REQIDL):
        self._wreg(0x0D, 0x07)
        stat, recv, bits = self._tcom(self.PCD_TRANSCEIVE, [mode])
        if stat != self.OK or bits != 16:
            return self.ERR, bits
        return self.OK, bits

    def anticoll(self):
        self._wreg(0x01, 0x00)
        self._set_bit(0x01, 0x80)
        self._wreg(0x0D, 0x00)

        stat, recv, bits = self._tcom(
            self.PCD_TRANSCEIVE, [self.PICC_ANTICOLL, 0x20]
        )

        if stat == self.OK and len(recv) >= 4:
            return self.OK, recv[:4]

        return self.ERR, []


