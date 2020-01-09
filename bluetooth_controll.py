import serial
from bluedot import BlueDot

# Serial networking
ser = serial.Serial('/dev/ttyUSB0',9600)
if ser is None:
    ser = serial.Serial('/dev/ttyUSB1',9600)

# Load BlueDot
bd = BlueDot();

# Follow the direction of circle
def dpad(pos):
    if pos.top:
        ser.write(("F\n").encode("ascii"))
    elif pos.bottom:
        ser.write(("B\n").encode("ascii"))
    elif pos.left:
        ser.write(("L\n").encode("ascii"))
    elif pos.right:
        ser.write(("R\n").encode("ascii"))

# Stop RC car
def released():
    ser.write(("H\n").encode("ascii"))

# Run dpad function
bd.when_pressed = dpad
bd.when_moved = dpad
bd.when_released = released

# Activate while connected to application
while True:
    read_serial = ser.readline()
    print(read_serial)
