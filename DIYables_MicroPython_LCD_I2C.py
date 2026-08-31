import time

class LCD_I2C:
    def __init__(self, i2c, addr, rows, cols):
        self.i2c = i2c
        self.addr = addr
        self.rows = rows
        self.cols = cols
        self.backlight_val = 0x08
        time.sleep_ms(50)
        self._write_command(0x03)
        time.sleep_ms(5)
        self._write_command(0x03)
        time.sleep_ms(1)
        self._write_command(0x03)
        self._write_command(0x02)
        self._write_command(0x28)
        self._write_command(0x0C)
        self._write_command(0x06)
        self.clear()

    def _write_byte(self, data):
        self.i2c.writeto(self.addr, bytes([data | self.backlight_val]))

    def _toggle_enable(self, data):
        time.sleep_us(1)
        self._write_byte(data | 0x04)
        time.sleep_us(1)
        self._write_byte(data & ~0x04)
        time.sleep_us(50)

    def _write_command(self, cmd):
        high = cmd & 0xF0
        low = (cmd << 4) & 0xF0
        self._write_byte(high)
        self._toggle_enable(high)
        self._write_byte(low)
        self._toggle_enable(low)

    def _write_data(self, data):
        high = (data & 0xF0) | 0x01
        low = ((data << 4) & 0xF0) | 0x01
        self._write_byte(high)
        self._toggle_enable(high)
        self._write_byte(low)
        self._toggle_enable(low)

    def clear(self):
        self._write_command(0x01)
        time.sleep_ms(2)

    def backlight(self):
        self.backlight_val = 0x08
        self._write_byte(0x00)

    def putstr(self, string):
        for char in string:
            self._write_data(ord(char))

    def move_to(self, col, row):
        
        row_offsets = [0x00, 0x40, 0x14, 0x54]
        self._write_command(0x80 | (col + row_offsets[row]))
