import time

import ssd1306
from machine import I2C, Pin


class Display(ssd1306.SSD1306_I2C):
    SYMBOL_SZIE = (8, 8)

    SET_HWSCROLL_OFF = const(0x2e)
    SET_HWSCROLL_ON = const(0x2f)
    SET_HWSCROLL_RIGHT = const(0x26)
    SET_HWSCROLL_LEFT = const(0x27)

    def __init__(self, i2c, resolution=(128, 64), addr=0x3c, external_vcc=False):
        super(Display, self).__init__(resolution[0], resolution[1], i2c, addr, external_vcc)
        self.fill(0)

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

        self.write_cmd(self.SET_HWSCROLL_OFF)
        self.write_cmd(directions[side])
        self.write_cmd(0x00)  # dummy byte
        self.write_cmd(0x07)  # start page = page 7
        self.write_cmd(speed)  # frequency
        self.write_cmd(0x00)  # end page = page 0

        self.write_cmd(0x00)
        self.write_cmd(0xff)
        self.write_cmd(self.SET_HWSCROLL_ON)  # activate scroll

    def hardware_scroll_stop(self, refresh=True):
        self.write_cmd(self.SET_HWSCROLL_OFF)
        if refresh:
            self.show()

    def clear(self):
        self.fill(0)
        self.show()

    def draw_from_file(self, path, offset=(0, 0), size=(None, None), by_line=False, by_half=True):
        """
        Draws binary image from file. Renders lines interlaced
        :param path: path to file
        :param offset: offset for x, y. E.g. if you want to put image in upper-right corner or somewhere
        :param size: image size, corresponds to screen size if not specified
        :param by_half: show halfs of the interlaced image when ready. "Speeds up" rendering
        :param by_line: show each line when ready (slower but can be fancier)
        """
        width, height = size
        if width is None:
            width = self.width
        if height is None:
            height = self.height

        with open(path, 'rb') as f:
            for start_line in range(2):
                for y in range(start_line, height, 2):
                    f.seek(y * width)
                    row = f.read(width)

                    for x, val in enumerate(iter(row)):
                        self.pixel(x + offset[0], y + offset[1], val)

                    if by_line:
                        self.show()

                if by_half:
                    self.show()

        self.show()

    def draw_from_sequence(self, sequence, offset=(0, 0), size=(None, None), by_line=False):
        """
        Draws image from sequence of bytes
        :param sequence: sequence of bytes
        :param offset: offset for x, y. E.g. if you want to put image in upper-right corner or somewhere
        :param size: image size, corresponds to screen size if not specified
        :param by_line: show each line when ready (slower but can be fancier)
        """
        width, height = size
        if width is None:
            width = self.width
        if height is None:
            height = self.height

        iterable = iter(sequence)
        for y in range(height):
            for x, val in enumerate(iterable):
                self.pixel(x + offset[0], y + offset[1], val)

                if x >= width - 1:
                    break

            if by_line:
                self.show()

        self.show()

    def __get_text_size(self, text):
        return len(text) * self.SYMBOL_SZIE[0]

    def __prepare_text(self, text, autowrap=True):
        lines = text.split('\n')
        for line in lines:
            width = self.__get_text_size(line)

            if width > self.width and autowrap:
                words = line.split(' ')
                line = ''

                for word in words:
                    if line != '':
                        word = ' ' + word

                    if self.__get_text_size(line) + self.__get_text_size(word) <= self.width:
                        line += word
                    else:
                        yield line
                        line = word.strip()

            yield line

    def draw_text(self, text, autowrap=True, alignment='center', by_line=True, delay=3):
        """
        Draws text on screen. Supports simple paging if text does not fit
        :param text: text to draw
        :param autowrap: auto wrap text with new lines
        :param alignment: auto wrap text with new lines
        :param by_line: show text line by line
        :param delay: how long to wait before scrolling to next page in seconds
        """
        GET_POS = {
            'left': lambda size: 0,
            'center': lambda size: int((self.width / 2) - (size / 2)),
            'right': lambda size: self.width - size,
        }

        self.fill(0)

        lines = self.__prepare_text(text, autowrap)

        n = 0
        for line in lines:
            x = GET_POS[alignment](self.__get_text_size(line))
            y = n * self.SYMBOL_SZIE[1]

            self.text(line, x, y)

            if by_line:
                self.show()

            n += 1
            if n * self.SYMBOL_SZIE[1] >= self.height:  # paging if lines does not fit
                n = 0
                self.show()
                time.sleep(delay)
                self.fill(0)

        self.show()
