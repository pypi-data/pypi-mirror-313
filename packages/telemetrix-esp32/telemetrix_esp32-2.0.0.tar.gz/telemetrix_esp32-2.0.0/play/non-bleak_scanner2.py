from adafruit_ble import BLERadio
import sys

radio = BLERadio()
print("scanning")

for entry in radio.start_scan(timeout=60, minimum_rssi=-80):
    if entry.complete_name == 'Telemetrix4ESP32BLE':
        print(f'Mac: {entry.address}')
        sys.exit(0)

