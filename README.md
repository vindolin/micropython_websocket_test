# micropython_websocket_test

## Just a little experiment with MicroPython and websockets on an ESP32.

Control the color of a rotating gradient NeoPixel ring from a webpage using websockets.

Multiple windows to the same module can be open and the widgets are synchronized through the websockets.

The client websocket reconnects after connection loss.

Copy networks.py, wifi.py, color.py and main.py and the subfolder www to your flash filesystem.

Also copy microWebSrv.py and microWebSocket.py from https://github.com/jczic/MicroWebSrv.

![Screenshot](https://i.imgur.com/YWZlwQz.jpg)
