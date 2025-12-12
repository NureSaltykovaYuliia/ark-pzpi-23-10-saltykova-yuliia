# adapters/network.py
import network
import time
import urequests
import json

class NetworkAdapter:
    def __init__(self, ssid, password, url):
        self.ssid = ssid
        self.password = password
        self.url = url
        self.wlan = network.WLAN(network.STA_IF)

    def connect(self):
        self.wlan.active(True)
        if not self.wlan.isconnected():
            print('Connecting to WiFi...')
            self.wlan.connect(self.ssid, self.password)
            while not self.wlan.isconnected():
                time.sleep(1)
        print('WiFi Connected:', self.wlan.ifconfig()[0])

    def send_telemetry(self, data):
        try:
            headers = {'Content-Type': 'application/json'}
            # У реальному проекті тут треба додати Authorization токен
            res = urequests.post(self.url, data=json.dumps(data), headers=headers)
            print(f"[POST] Status: {res.status_code}")
            res.close()
        except Exception as e:
            print(f"[ERROR] Send failed: {e}")