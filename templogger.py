"""
Temperature logger and plotter
"""
import datetime
import serial
import logging
import sys
import pylab
import os

# For plotting
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


from time import time, strftime

# Set up logging
logger = logging.getLogger('serialmulti')
logdate = strftime("%Y%m%d_%H%M%S")
logfilename = "templog_%s.csv" %(logdate)
hdlr = logging.FileHandler(logfilename)
formatter = logging.Formatter('%(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.INFO)

# Find the right serial port
serialbase = "/dev/ttyUSB"
countbase = 0
if (os.name) == "nt":
    serialbase = "COM"
    countbase = 1

foundserial = False
serialport = ''
for i in range(countbase, 20):
    try :
        serialport = "%s%i" %(serialbase, i)
        dev = serial.Serial(serialport, 115200, timeout=2)
        foundserial = True
        break
    except(OSError):
        continue

if not foundserial:
    print("Could not find attached logger on serial/USB port.")
    sys.exit(1)
else:
    print "Found good serial port at %s" %serialport

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
        temperature, pressure = float(vals[0]), int(vals[1])
        logger.info("%s,%s,%s" % (now,temperature,pressure))
        sys.stdout.write("Temperature: %.1f C; Pressure: %.1fhPa   \r" % (temperature,pressure/1000.0) )
        sys.stdout.flush()
    except (KeyboardInterrupt):
        break
    except (ValueError):
        continue


## Do the plotting

timestamp, temperature, pressure = np.loadtxt(logfilename,
                                              unpack=True,
                                              delimiter=",",
                                              converters={ 0: mdates.strpdate2num("%Y-%m-%d %H:%M:%S.%f")})

fig = plt.figure(figsize=(8, 6), dpi=80, facecolor='w', edgecolor='k')
ax = fig.add_subplot(111)

# ax.set_xticks(timestamp) # Tickmark + label at every plotted point
ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))

plt.plot_date(x=timestamp, y=temperature, fmt="k-")
plt.title("Temperature record from %s" %(logfilename))
plt.ylabel("Temperature")
plt.xlabel("Time")
plt.ylim([min(temperature)-0.2, max(temperature)+0.2])
fig.autofmt_xdate(rotation=45)
plt.grid(True)
imagefilename = "plot_%s.png" %(logdate)
plt.savefig(imagefilename)
print("\n\n...Image saved to %s" %(imagefilename))
plt.show()
