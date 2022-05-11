# ECE 568 - Lab Assignment - 2
import network
import esp32
import machine
from machine import Pin
import time
try:
    import usocket as socket
except:
    import socket
        
# Define socket host and port
serverHost = '0.0.0.0'
serverPort = 8000

# Wifi Credentials
wifi_ssid = "NETGEAR73"   
wifi_password = "roundlake377"

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

# Function reads and prints onboard Temperature sensor value.
def GetTemperatureSensorValue():
    temp = esp32.raw_temperature()
    return temp

# Function reads and prints onboard Hall sensor value.
def GetHallSensorValue():
    hall = esp32.hall_sensor()
    return hall

# Function creates a Socket Server
def CreateSocketServer():
    addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
    s = socket.socket()
    s.bind(addr)
    s.listen(1)
    print('listening on', addr)
    return s
    
def web_page():
    """Function to build the HTML webpage which should be displayed
    in client (web browser on PC or phone) when the client sends a request
    the ESP32 server.
    
    The server should send necessary header information to the client
    (YOU HAVE TO FIND OUT WHAT HEADER YOUR SERVER NEEDS TO SEND)
    and then only send the HTML webpage to the client.
    
    Global variables:
    temp, hall, red_led_state
    """
    
    html_webpage = """<!DOCTYPE HTML><html>
    <head>
    <title>ESP32 Web Server</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.7.2/css/all.css" integrity="sha384-fnmOCqbTlWIlj8LyTjo7mOUStjsKC4pOpQbqyi7RrhN7udi9RwhKkMHpvLbHG9Sr" crossorigin="anonymous">
    <style>
    html {
     font-family: Arial;
     display: inline-block;
     margin: 0px auto;
     text-align: center;
    }
    h1 { font-size: 3.0rem; }
    p { font-size: 3.0rem; }
    .units { font-size: 1.5rem; }
    .sensor-labels{
      font-size: 1.5rem;
      vertical-align:middle;
      padding-bottom: 15px;
    }
    .button {
        display: inline-block; background-color: #e7bd3b; border: none; 
        border-radius: 4px; color: white; padding: 16px 40px; text-decoration: none;
        font-size: 30px; margin: 2px; cursor: pointer;
    }
    .button2 {
        background-color: #4286f4;
    }
    </style>
    </head>
    <body>
    <h1>ESP32 WEB Server</h1>
    <p>
    <i class="fas fa-thermometer-half" style="color:#059e8a;"></i> 
    <span class="sensor-labels">Temperature</span> 
    <span>"""+str(temp)+"""</span>
    <sup class="units">&deg;F</sup>
    </p>
    <p>
    <i class="fas fa-bolt" style="color:#00add6;"></i>
    <span class="sensor-labels">Hall</span>
    <span>"""+str(hall)+"""</span>
    <sup class="units">V</sup>
    </p>
    <p>
    RED LED Current State: <strong>""" + red_led_state + """</strong>
    </p>
    <p>
    <a href="/?red_led=on"><button class="button">RED ON</button></a>
    </p>
    <p>
    <a href="/?red_led=off"><button class="button button2">RED OFF</button></a>
    </p>
    </body>
    </html>"""
    return html_webpage

# Connect to wireless network
ConnectToWifi(wifi_ssid, wifi_password)

# Initialize Pin 12 as OUT for the external LED
led = machine.Pin(12, Pin.OUT)

# Update the values of the global variables
red_led_state = "ON" if led.value == 1 else "OFF" # string, check state of red led, ON or OFF
temp = GetTemperatureSensorValue()
hall = GetHallSensorValue()

# Main Server Routine
socketServer = CreateSocketServer()
while True:
    # Update Sensor values and LED State
    temp = GetTemperatureSensorValue()
    hall = GetHallSensorValue()
    red_led_state = "ON" if led.value() == 1 else "OFF"
    
    # Wait for client connections
    clientConnection, clientAddress = socketServer.accept()
    print('Got a connection from %s' % str(clientAddress))
    request = clientConnection.recv(1024)
    request = str(request)
    
    led_on = request.find('/?red_led=on')
    led_off = request.find('/?red_led=off')
    if led_on == 6:
        print('LED ON')
        red_led_state = "ON"
        led.value(1)
    if led_off == 6:
        print('LED OFF')
        red_led_state = "OFF"
        led.value(0)
    
    # Create the HTTP response
    response = web_page()    
    clientConnection.send('HTTP/1.1 200 OK\n')
    clientConnection.send('Content-Type: text/html\n')
    clientConnection.send('Connection: close\n\n')
    clientConnection.sendall(response.encode())
    clientConnection.close()
    
# Close Socket
socketServer.close()