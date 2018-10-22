import ssd1306
from machine import I2C, Pin


class Display(object):
    SET_HWSCROLL_OFF = const(0x2e)
    SET_HWSCROLL_ON = const(0x2f)
    SET_HWSCROLL_RIGHT = const(0x26)
    SET_HWSCROLL_LEFT = const(0x27)

    def __init__(self, i2c, resolution=(128, 64)):
        self.display = ssd1306.SSD1306_I2C(resolution[0], resolution[1], i2c)
        self.display.fill(0)

    def hardware_scroll(self, side, speed=9):
        """
        Enables hardware supported scroll
        :param side: In which side to scroll, can be 'left' or 'right'
        :param speed: integer from 1 to 12 (it works in a strange way, i recommend using default value ;) )
        :return:
        """
        directions = {
            'left': self.SET_HWSCROLL_LEFT,
            'right': self.SET_HWSCROLL_RIGHT,
        }

        self.display.write_cmd(self.SET_HWSCROLL_OFF)
        self.display.write_cmd(directions[side])
        self.display.write_cmd(0x00)  # dummy byte
        self.display.write_cmd(0x07)  # start page = page 7
        self.display.write_cmd(speed)  # frequency
        self.display.write_cmd(0x00)  # end page = page 0

        self.display.write_cmd(0x00)
        self.display.write_cmd(0xff)
        self.display.write_cmd(self.SET_HWSCROLL_ON)  # activate scroll

    def hardware_scroll_stop(self, refresh=True):
        self.display.write_cmd(self.SET_HWSCROLL_OFF)
        if refresh:
            self.display.show()

    def clear(self):
        self.display.fill(0)
        self.display.show()

    def draw_from_file(self, path, by_line=False):
        self.clear()

        with open(path, 'rb') as f:
            for y in range(self.display.height):
                row = f.read(self.display.width)
                for x, val in enumerate(iter(row)):
                    self.display.pixel(x, y, val)

                if by_line:
                    self.display.show()

        self.display.show()

    def draw_text(self, text):
        pass

