# ECE 568 - Lab Assignment - 2

espclient.py:
1. Connects ESP32 to Wireless Network
2. Measures onboard Temperature and Hall sensor values
3. Uploads the sensor data to Thingspeak cloud platform over an interval of 30 seconds.

espserver.py:
1. This python script runs a simple HTTP server on ESP32 and accepts requests from external client devices.
2. Html webpage displays the current Temperature, hall sensor value, and the state of the Red LED connected to the ESP32 board.
3. The HTTP webpage has an "ON" and "OFF" buttons that lets the client device users to turn On/Off the LED light.

Hardware Connection details:
One 5mm LED (Color - Red), connected to the GPIO Pin 12 of ESP 32 Feather board device.
The negative terminal of the LED is connected to Ground terminal via a 220Ohm resistor.

Video link:
https://youtu.be/GRGIwNRlbGI
