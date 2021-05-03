# pico-weatherstation
A weatherstation with a display implemented with Raspberry Pico and the Pimoroni Pico Explorer Hat.
Files:
<br><b>lib/dht11_jurassic.py</b>
<br>Micropython DHT11 Library (https://github.com/JurassicPork/DHT_PyCom/blob/master/dth.py )
<br><b>lib/explorer_hat.py</b>
<br>A wrapper class for the Pimorony library
<br><b>lib/ring_buffer.py</b>
<br>A ringbuffer class to store the temp and humidity data.
<br><b>weatherstation_threading.py</b><br>
<br>The main script. It controls the pimoroni display, keys and the DHT11 temperature and humidity reading.
It also serves a control LED (Picos internal LED) for debugging purpose.
The scripts uses Micropython and the uasyncio library for async control of the several coroutines (coros).
The DHT11 serial pin is connected to Picos pin 2.
<br>
<br>Key_A: Switch from standard screen to temp graph
<br>Key_B: Switch from standard screen to humidity graph
<br>Key_X/_Y for further need...
<br>
<br>The SW depends on Piromomis Micropython release 0.1.3 (https://github.com/pimoroni/pimoroni-pico/releases)
<br>
<br>Remark:
<br>At least the key_handler coro should be refactored.
