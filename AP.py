#WARNING: This is still a work in progress and it's mostly proof of concept code

import network
import socket
from machine import Pin

# Initialize the onboard LED
led = Pin("LED", Pin.OUT)

# Configure the access point
ssid = 'Light Server!'
password = '12345678'
ap = network.WLAN(network.AP_IF)
ap.config(essid=ssid, password=password)
ap.active(True)

print('Access point configured:')
print('SSID:', ssid)
print('Password:', password)
print('IP:', ap.ifconfig()[0])

# HTML to serve
html_on = """<!DOCTYPE html>
<html>
   <head>
     <title>Web Server On Pico W </title>
   </head>
  <body>
      <h1>Pico Wireless Web Server</h1>
      <p>LED is ON</p>
      <a href="/light/on">Turn On</a>
      <a href="/light/off">Turn Off</a>
  </body>
</html>
"""

html_off = """<!DOCTYPE html>
<html>
   <head>
     <title>Web Server On Pico W </title>
   </head>
  <body>
      <h1>Pico Wireless Web Server</h1>
      <p>LED is OFF</p>
      <a href="/light/on">Turn On</a>
      <a href="/light/off">Turn Off</a>
  </body>
</html>
"""

# Open socket
addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(addr)
s.listen(1)

print('Listening on', addr)

# Listen for connections
while True:
    try:
        cl, addr = s.accept()
        print('Client connected from', addr)

        while True:
            try:
                cl.settimeout(3.0)
                request = cl.recv(1024)
                if not request:
                    break
                request = str(request)
                # print(request)

                if '/light/on' in request:
                    print("LED on")
                    led.on()
                    response = html_on
                elif '/light/off' in request:
                    print("LED off")
                    led.off()
                    response = html_off
                else:
                    led.off()
                    response = html_off

                # Generate the web page with the stateis as a parameter
                cl.sendall('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n'.encode('utf-8'))
                cl.sendall(response.encode('utf-8'))
            except OSError as e:
                print("Error:", e)
                break

        cl.close()
        print('Connection closed')

    except OSError as e:
        print("Error:", e)
        continue