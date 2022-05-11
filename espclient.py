# ECE 568 - Lab Assignment - 2
import machine
from machine import Pin, Timer
import network
import esp32
import ussl as ssl
import urequests
import time
import gc
try:
    import usocket as socket
except:
    import socket

# Thingspeak Credentials
thingspeakWriteKey = "LWT45ZFCXEASC72P"
thingspeakApiHost = "api.thingspeak.com"
thingspeakApiPort = 80

# Wifi Credentials
wifi_ssid = "NETGEAR73"   
wifi_password = "roundlake377"

# Function reads Esp32 onboard sensor values.
def MeasureOnboardSensorValues():
    temp = GetTemperatureSensorValue()
    hall = GetHallSensorValue()
    sensorValues = (temp, hall)
    return sensorValues

# Function uploads the input sensor values to Thingspeak cloud platform.
def UploadSensorValuesToCloud(sensorValues):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    addressInfo = socket.getaddrinfo(thingspeakApiHost, thingspeakApiPort)
    address = addressInfo[0][-1]
    s.connect(address)
    s.send('GET https://api.thingspeak.com/update?api_key='+thingspeakWriteKey+'&field1='+str(sensorValues[0])+'&field2='+str(sensorValues[1])+'\r\n\r\n')
    print(s.recv(1024))
    s.close()

# Function reads and prints onboard Temperature sensor value.
def GetTemperatureSensorValue():
    temp = esp32.raw_temperature()
    print("Onboard Temperature sensor value: " + str(temp) + "F")
    return temp

# Function reads and prints onboard Hall sensor value.
def GetHallSensorValue():
    hall = esp32.hall_sensor()
    print("Onboard Hall sensor value: " + str(hall) + "V")
    return hall

# Function connects ESP32 board to Wireless Network.
def ConnectToWifi(ssid, password):
    # Create a station object to store our connection
    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)
    if sta_if.isconnected():
        PrintWirelessNetworkDetails(sta_if)
        return None
    print('Trying to connect to %s...' % ssid)
    sta_if.connect(ssid, password)
    for retry in range(100):
        connected = sta_if.isconnected()
        if connected:
            break
        time.sleep(0.1)
        print('.', end='')
    if connected:
        PrintWirelessNetworkDetails(sta_if)
    else:
        print("Error connecting...Check credentials and reboot the system")

# Function displays Wireless network connection details.
def PrintWirelessNetworkDetails(sta_if):
    print("\n")
    print("Connected to " + sta_if.config('essid'))
    print("IP Address:", sta_if.ifconfig()[0])
    
# Connect to Wireless Network
ConnectToWifi(wifi_ssid, wifi_password)

# Enable Automatic Garbage Collection
gc.enable()
# Define Timer of period 30 seconds
timer1 = Timer(0)
timer1.init(period = 30000, mode = Timer.PERIODIC, callback= lambda t: UploadSensorValuesToCloud(MeasureOnboardSensorValues()))
