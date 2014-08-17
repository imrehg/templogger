import datetime
import serial
import logging

from time import time, strftime

# Set up logging
logger = logging.getLogger('serialmulti')
logfilename = "templog_%s.csv" %(strftime("%Y%m%d_%H%M%S"))
hdlr = logging.FileHandler(logfilename)
formatter = logging.Formatter('%(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.INFO)


dev = serial.Serial('/dev/ttyUSB0', 115200, timeout=2)

print("Now logging to %s" %(logfilename))
print("Press Ctrl-C to stop!")

# Setting up output file
logger.info("#Time(Localtime),Temperature(degC),Pressure(Pa)")

while True:
    try:
        input = dev.readline()
        if input[0] == "#" :
            continue
        now = datetime.datetime.now()
        vals = input.strip().split(',')
        logger.info("%s,%s,%s" % (now,vals[0],vals[1]))
    except (KeyboardInterrupt):
        break
