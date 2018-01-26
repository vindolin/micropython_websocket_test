import network
from utime import sleep
WIFI_RETRY_SECONDS = 10


def connect(networks):
    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)

    for ssid, password in networks:
        print('trying {}'.format(ssid))
        for i in range(WIFI_RETRY_SECONDS):
            sta_if.connect(ssid, password)
            print('.', end='')
            sleep(1)
            if sta_if.isconnected():
                print('connected to {} - {}'.format(ssid, sta_if.ifconfig()))
                return sta_if

    print('no luck :(')
    return False
