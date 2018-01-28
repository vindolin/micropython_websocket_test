import machine as m
from neopixel import NeoPixel
from time import sleep
import math
from color import hsl2rgb
from microWebSrv import MicroWebSrv  # download at https://github.com/jczic/MicroWebSrv
import gc
import _thread

# edit the networks.py file or use your own code here to connect to your wifi
from networks import networks
from wifi import connect
wifi = connect(networks)

r = m.reset  # shortcut

NEOPIXEL_PIN = 12
PIXELCOUNT = 16

SPEED = 0.02
SCALER = 40

np = NeoPixel(m.Pin(NEOPIXEL_PIN), PIXELCOUNT, timing=True)

max_lum = 20
hue = 50


def clear():
    """ clear all pixels to black """
    for i in range(PIXELCOUNT):
        np[i] = (0, 0, 0)
        np.write()


clear()


def set_luminosity(luminosity):
    """ set the luminosity and precompute the gradient array """
    global lum_gradient, max_lum
    max_lum = luminosity
    step = max_lum / PIXELCOUNT
    lum_gradient = [int(step * i) for i in range(PIXELCOUNT + 1)]
    gc.collect()


set_luminosity(max_lum)  # set initial luminosity


def run_main_loop():
    i = 0

    while True:
        for pixi in range(PIXELCOUNT):
            rgb = hsl2rgb((
                hue,
                255,
                lum_gradient[pixi]
            ))
            np[(i + pixi) % PIXELCOUNT] = [int(c) for c in rgb]
        np.write()

        # speed the animation up and down with a sine wave
        st = math.sin(i / SCALER) + 1
        sleep(SPEED * st)
        i += 1
        gc.collect()


websockets = []  # keeps track of all connections


def _recvTextCallback(webSocket, msg):
    globals()['hue'] = int(msg)
    # synchronize the other clients
    for ws in websockets:
        if ws != webSocket:
            ws.SendText(msg)
    gc.collect()


def _closedCallback(webSocket):
    with _thread.allocate_lock():
        websockets.remove(webSocket)
    gc.collect()
    print('closing stale websocket')
    print('number of connections: {}'.format(len(websockets)))
    print('free mem: {}'.format(gc.mem_free()))


def _acceptWebSocketCallback(webSocket, httpClient):
    with _thread.allocate_lock():
        websockets.append(webSocket)
    gc.collect()

    print('new connection from {}'.format(httpClient.GetIPAddr()))
    print('number of connections: {}'.format(len(websockets)))
    webSocket.RecvTextCallback = _recvTextCallback
    webSocket.ClosedCallback = _closedCallback
    webSocket.SendText(str(hue))
    print('free mem: {}'.format(gc.mem_free()))


mws = MicroWebSrv(webPath='/www')
mws.MaxWebSocketRecvLen = 256
mws.AcceptWebSocketCallback = _acceptWebSocketCallback
mws.Start()

_thread.start_new_thread(run_main_loop, ())
