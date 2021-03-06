import network
from networks import networks
from utime import sleep
WIFI_RETRY_SECONDS = 10

sta_if = network.WLAN(network.STA_IF)


def _connect():
    sta_if.active(True)

    visible_essids = [wifi[0].decode() for wifi in sta_if.scan()]

    for essid, password in networks:
        if essid in visible_essids:
            print('\ntrying {}'.format(essid))
            sta_if.connect(essid, password)
            for i in range(WIFI_RETRY_SECONDS):
                print('.', end='')
                sleep(1)
                if sta_if.isconnected():
                    print('\nconnected to {} - {}'.format(essid, sta_if.ifconfig()))
                    return essid, sta_if


def connect_wifi(sta_callback=None, ap_callback=None, wifi_retry_seconds=WIFI_RETRY_SECONDS):
    result = _connect()

    if result:
        if sta_callback:
            sta_callback(sta_if)
        return result
    else:
        sta_if.active(False)
        print('\ncould not connect, setting up AccessPoint "NeoPixels"')
        ap_if = network.WLAN(network.AP_IF)
        ap_if.active(True)
        ap_if.config(essid='NeoPixels', authmode=network.AUTH_OPEN)
        print('AP active on {}'.format(ap_if.ifconfig()))

        if ap_callback:
            ap_callback(sta_if)

        return ap_if
