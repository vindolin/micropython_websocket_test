import machine as m
from neopixel import NeoPixel
from time import sleep
import math
from color import hsl2rgb
from microWebSrv import MicroWebSrv  # download at https://github.com/jczic/MicroWebSrv

# edit the networks.py file or use your own code here to connect to your wifi
from networks import networks
from wifi import connect
wifi = connect(networks)

NEOPIXEL_PIN = 17
PIXELCOUNT = 12

SPEED = 0.04

r = m.reset  # usefull for debugging r()
np = NeoPixel(m.Pin(NEOPIXEL_PIN), PIXELCOUNT)

max_lum = 20
hue = 50


def clear():
    for i in range(PIXELCOUNT):
        np[i] = (0, 0, 0)
        np.write()


clear()


def set_luminosity(luminosity):
    global lramp, max_lum
    max_lum = luminosity
    step = max_lum / PIXELCOUNT
    lramp = [int(step * i) for i in range(PIXELCOUNT + 1)]


set_luminosity(max_lum)


def go():
    i = 0

    while True:
        for pixi in range(PIXELCOUNT):
            rgb = hsl2rgb((
                hue,
                255,
                lramp[pixi]
            ))
            np[(i + pixi) % PIXELCOUNT] = [int(c) for c in rgb]
        np.write()

        st = (math.sin(i / 40) + 1) / 2
        sleep(SPEED * st)
        i += 1


def ping():
    while True:
        print(lramp)
        sleep(2)


def _recvTextCallback(webSocket, msg):
    global hue
    hue = int(msg)


def _closedCallback(webSocket):
    print('WS CLOSED')


def _acceptWebSocketCallback(webSocket, httpClient):
    print('WS ACCEPT')
    webSocket.RecvTextCallback = _recvTextCallback
    webSocket.ClosedCallback = _closedCallback
    webSocket.SendText(str(hue))


mws = MicroWebSrv(webPath='/www')
mws.MaxWebSocketRecvLen = 256
mws.WebSocketThreaded = True
mws.AcceptWebSocketCallback = _acceptWebSocketCallback
mws.Start(threaded=True)

go()
