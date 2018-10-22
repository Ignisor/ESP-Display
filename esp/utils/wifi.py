import time
import network
import machine

from data import conf
from utils.pins import LED

ap_if = network.WLAN(network.AP_IF)
sta_if = network.WLAN(network.STA_IF)


def toggle_wifi(status=True):
    """Enables or disables wi-fi for connection"""
    sta_if.active(status)


def toggle_hotspot(status=True):
    """Enables or disables hotspot (ap_if)"""
    ap_if.active(status)


def connect(ssid=None, password=None):
    """Tries to connect to the wi-fi network"""
    ssid = ssid or conf.SSID
    password = password or conf.PASSWORD

    for i in range(conf.CONNECT_RETRIES):
        t_start = time.time()
        sta_if.connect(ssid, password)

        while not sta_if.isconnected():
            LED.value(0)  # 0 - is enable for LED
            time.sleep(0.1)
            LED.value(1)
            time.sleep(0.1)

            t = time.time() - t_start
            if t >= conf.CONNECTION_TIME:
                break

        if sta_if.isconnected():
            return sta_if.isconnected()


def reset_if_not_connected():
    if sta_if.isconnected():
        return True
    else:
        machine.reset()
        return False
