# micropython_websocket_test

## Just a little experiment with MicroPython and websockets on an ESP32.

Control the color of a rotating gradient NeoPixel ring from a webpage using websockets.

Multiple windows to the same module can be open and the widgets are synchronized through the websockets.

The client websocket automatically reconnects after connection loss.

Copy networks.py, wifi.py, color.py and main.py and the subfolder www to your flash filesystem.

Also copy microWebSrv.py and microWebSocket.py from https://github.com/jczic/MicroWebSrv.

*Too bad that I get the error "MicroWebSocket : Out of memory on new WebSocket connection." when trying to connect more than two clients :(*

![Screenshot](https://i.imgur.com/YWZlwQz.jpg)
