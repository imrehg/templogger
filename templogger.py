"""
Temperature logger and plotter
"""
import datetime
import serial
import logging
import sys
import os
import argparse

from time import time, strftime

# Command line arguments
parser = argparse.ArgumentParser(description='Temperature logger.')
parser.add_argument('--noplot', action='store_true', help='Do not generate plot in the end.')
parser.add_argument('--noplotshow', action='store_true', help='Do not show plot in the end but still save.')
parser.add_argument('--logfile', help='Filename to log to')
args = parser.parse_args()
#print(args)
#print(args.logfile)
#sys.exit(0)

if not args.noplot:
    # For plotting
    import numpy as np
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import matplotlib.dates as mdates

# Set up logging
if args.logfile:
    logfilename = args.logfile
else:
    logdate = strftime("%Y%m%d_%H%M%S")
    logfilename = "templog_%s.csv" %(logdate)

logger = logging.getLogger('serialmulti')
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

## Might not want to plot
if args.noplot:
    sys.exit(0)

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
imagefilename = "%s.png" %(logfilename)
plt.savefig(imagefilename)
print("\n\n...Image saved to %s" %(imagefilename))
if not args.noplotshow:
    plt.show()
