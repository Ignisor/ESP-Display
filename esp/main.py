import time

from utils.pins import DISPLAY


while True:
    DISPLAY.draw_text('GoWombat\nThis is very descriptive and long text with different staff that will not fit and '
                      'also it requires some paging as well and stuff bla bla bla cucumbers',
                      alignment='right')
    time.sleep(3)
