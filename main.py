import time
from machine import Pin
from ir_rx.nec import NEC_8  # Import NEC decoder
from ir_tx.nec import NEC  # Import NEC transmitter

#Light commands!
LIGHTS_OnOffToggle = 64
LIGHTS_dim = 93
LIGHTS_brighten = 92

#PRESET RGB stuff
LIGHTS_initPreset = 13
#Red
LIGHTS_increaseRed = 20
LIGHTS_decreaseRed = 16
#Green
LIGHTS_increaseGreen = 21
LIGHTS_decreaseGreen = 17
#Blue
LIGHTS_increaseBlue = 22
LIGHTS_decreaseBlue = 18

#Stored light values
LIGHTS_R = 27
LIGHTS_G = 27
LIGHTS_B = 27
#RGB range = range(0, 26)
#Dim range = range(0, 7)


ir_transmitter_pin = Pin(2, Pin.OUT, value = 0)
nec = NEC(ir_transmitter_pin)

# Callback function to handle decoded IR messages
def ir_callback(data, addr, ctrl):
    if data < 0:  # No valid data received
        print("Invalid data received")
    else:
        print(f"RECEVED: Address: {addr}, Command: {data}, Control: {ctrl}")
        print(f"LIGHTS_ = {data}")

ir_recever_pin = Pin(3, Pin.IN)
# decoder = NEC_8(ir_recever_pin, ir_callback) #UNCOMMENT TO SEE CODES

def send_nec_message(command, log = False):
    address = 0 # For this remote it is zero. This can be changed into a funciton param though.
    nec.transmit(address, command)
    time.sleep(1/8) # Any faster than this exceeds the receve rate
    if log is True:
        print(f"SENT: NEC message with Address: {address}, Command: {command}")


#Custom functions!

def interpolate_colors(color1, color2, length):
    # Split the input colors into their RGB components
    r1, g1, b1 = color1
    r2, g2, b2 = color2

    # Function to interpolate between two values
    def interpolate(start, end, factor):
        return int(start + (end - start) * factor)

    # Generate the interpolated colors
    interpolated_colors = [
        (
            interpolate(r1, r2, i / (length - 1)),
            interpolate(g1, g2, i / (length - 1)),
            interpolate(b1, b2, i / (length - 1))
        )
        for i in range(length)
    ]

    return interpolated_colors

def resetLights():
    global LIGHTS_R, LIGHTS_G, LIGHTS_B
    send_nec_message(LIGHTS_initPreset)
    for num in range(0, 25 + 1):
        send_nec_message(LIGHTS_increaseRed)
        send_nec_message(LIGHTS_increaseBlue)
        send_nec_message(LIGHTS_increaseGreen)
        print(f"Getting lighter! ({num}/26)")

    for num in range(0, 6 + 1):
        send_nec_message(LIGHTS_brighten)
        print(f"Getting brighter! ({num}/7)")
    LIGHTS_R = 27
    LIGHTS_G = 27
    LIGHTS_B = 27

def setRGB(color):
    red, green, blue = color
    global LIGHTS_R, LIGHTS_G, LIGHTS_B

    while LIGHTS_R != red or LIGHTS_G != green or LIGHTS_B != blue:
        # Adjust Red
        if LIGHTS_R < red:
            send_nec_message(LIGHTS_increaseRed)
            LIGHTS_R += 1
        elif LIGHTS_R > red:
            send_nec_message(LIGHTS_decreaseRed)
            LIGHTS_R -= 1

        # Adjust Green
        if LIGHTS_G < green:
            send_nec_message(LIGHTS_increaseGreen)
            LIGHTS_G += 1
        elif LIGHTS_G > green:
            send_nec_message(LIGHTS_decreaseGreen)
            LIGHTS_G -= 1

        # Adjust Blue
        if LIGHTS_B < blue:
            send_nec_message(LIGHTS_increaseBlue)
            LIGHTS_B += 1
        elif LIGHTS_B > blue:
            send_nec_message(LIGHTS_decreaseBlue)
            LIGHTS_B -= 1


resetLights()

# Example usage
color_start = (27, 0, 0)  # Red
setRGB(color_start)
color_end = (0, 0, 27)    # Blue
length = 10

colors = interpolate_colors(color_start, color_end, length)
for i, color in enumerate(colors):
    setRGB(color)
    print(f"Completed interpolation step {i+1}/{len(colors)}")

# Main loop
while True:
    # send_nec_message(LIGHTS_OnOffToggle) # Epilepsy warning

    time.sleep(1/8)  # Keep the program running
