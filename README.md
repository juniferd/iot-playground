# iot-playground
dumping ground for various iot tinkering

## memento camera

playing around with [adafruit memento camera](https://www.adafruit.com/product/5420) with CircuitPython

### setup

- flash memento with CircuitPython - used the [web installer](https://circuitpython.org/board/adafruit_esp32s3_camera/)
- create virtualenv and install requirements
  ```
  python3 -m venv iotenv
  source ./iotenv/bin/activate
  python3 pip install -r requirements.txt
  ```

### transfer and run code.py

- connect memento run repl in terminal
  ```
  mpremote repl
  ```
- copy over memento/code.py or use the dumb shell script (copies over code.py and anything in lib directory)
  ```
  ./scripts/sync.sh
  ```
- repl should automatically restart

### update settings directly in memento
- add settings in `/Volumes/CIRCUITPY/settings.toml` like `CIRCUITPY_WIFI_SSID` and `CIRCUITPY_WIFI_PASSWORD`

### shut down
- disconnect from repl with ctrl + ] (i think? double check)
- eject CIRCUITPY
- turn off/unplug memento
