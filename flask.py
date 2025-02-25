from machine import Pin, ADC
import ujson
import json
import network
import dht
import time
import urequests as requests

DEVICE_ID = "esp32"
WIFI_SSID = "bukan gp"
WIFI_PASS = "tebakajapasswordnya"
TOKEN = "BBUS-fgIorFaOy7n5MXOaI70LrWcO6lLPAZ"
DHT_PIN = Pin(15, Pin.IN)  # Fix deklarasi pin
LDR_PIN = Pin(34)
dht_sensor = dht.DHT11(DHT_PIN)
# WIFI Connection
def connect_to_wifi():
    print("Connecting to WiFi", end="")
    wifi_client = network.WLAN(network.STA_IF)
    wifi_client.active(True)
    wifi_client.connect(WIFI_SSID, WIFI_PASS)
    while not wifi_client.isconnected():
        print(".", end="")
        time.sleep(0.1)
    print(" Connected!")

def send_data_ubidots(temperature, humidity, light):
    url = "http://industrial.api.ubidots.com/api/v1.6/devices/" + DEVICE_ID
    headers = {"Content-Type": "application/json", "X-Auth-Token": TOKEN}
    data = {
        "temp": temperature,
        "humidity": humidity,
        "light": light
    }
    response = requests.post(url, json=data, headers=headers)
    print("Done Sending Data!")
    print("Response:", response.text)
    response.close()
    
def send_data_flask(temperature, humidity, light):
    API_URL = "http://192.168.0.100:7000/api/sensor"  # IP DISESUAIKAN DENGAN SERVER FLASK/DEVICE LAPTOP DALAM JARINGAN
    data = {
        "temp": temperature,
        "humidity": humidity,
        "light": light,
    }
    response = requests.post(API_URL, json=data)
    response.close()

connect_to_wifi()

ldr = ADC(LDR_PIN)
ldr.atten(ADC.ATTN_11DB)

while True:
    try:
        dht_sensor.measure()  # Membaca data sensor
        temperature = dht_sensor.temperature()  # Suhu dalam °C
        humidity = dht_sensor.humidity()  # Kelembaban dalam %
        ldr_value = ldr.read()
        send_data_ubidots(temperature, humidity, ldr_value)
        send_data_flask(temperature, humidity, ldr_value)
        print(f"Suhu: {temperature}°C  |  Kelembaban: {humidity}%  | Cahaya: {ldr_value}")
    except OSError as e:
        print("Error membaca sensor DHT11:", e)

    time.sleep(1)  # Tunggu minimal 2 detik sebelum membaca ulang