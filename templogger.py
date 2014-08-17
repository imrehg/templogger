import datetime
import serial

dev = serial.Serial('/dev/ttyUSB0', 115200, timeout=2)

while True:
    try:
        input = dev.readline().strip()
        vals = input.split(',')
        now = datetime.datetime.now()
        print("%s,%s,%s" % (now,vals[0],vals[1]))
    except KeyboardInterrupt:
        break
