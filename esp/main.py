import ubinascii
import machine
from umqtt.simple import MQTTClient

from data import conf
from utils.display import DataDisplay
from utils.pins import DISPLAY


CLIENT_ID = ubinascii.hexlify(machine.unique_id())
DATA_DISP = DataDisplay(DISPLAY, ('temperature', 'humidity'))
DATA_DISP.refresh()


def update_data(topic, msg):
    topic = topic.decode().split('/')
    device_id = topic.pop(-1)
    name = topic[-1]
    data = msg.decode()

    DATA_DISP.set_data(name, data)
    DATA_DISP.refresh()


mqtt = MQTTClient(CLIENT_ID, conf.MQTT_SERVER)
mqtt.set_callback(update_data)
mqtt.connect()
mqtt.subscribe(b'sensors/+/+')

while True:
    try:
        mqtt.wait_msg()
    except Exception as e:
        with open(conf.ERROR_LOG_FILENAME, 'w') as err_log:
            err_log.write(e)
            err_log.write('\n')

        mqtt.publish('errors/{}'.format(CLIENT_ID).encode(), str(e).encode())
        mqtt.disconnect()
        machine.reset()
