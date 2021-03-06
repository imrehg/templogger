#!/usr/bin/env python2
"""
Temperature logger and plotter

Using an Arduino and a BMP085 temperature/atmospheric pressure module
log the temperature and display results.

The Arduino is already flashed with program to return reading every 1 second,
in the form of `temperature,pressure\n`, example `29.2,100650`.

For help, can run the program with the `-h` command line parameter.
"""
import datetime
import serial
import logging
import sys
import os
import argparse

from time import time, strftime

## Handling command line arguments
parser = argparse.ArgumentParser(description='Temperature logger.')
parser.add_argument('--noplot', action='store_true', help='Do not generate plot in the end.')
parser.add_argument('--noplotshow', action='store_true', help='Do not show plot in the end but still save.')
parser.add_argument('--logfile', help='Filename to log to')
parser.add_argument('--onlyplot', metavar='FILENAME', help="Do not start to log, only plot from FILENAME")
args = parser.parse_args()

## Conditional import, as not needed if nothing to plot
if not args.noplot:
    ## For plotting
    import numpy as np
    import matplotlib
    # Prevent conflict with Qt5 and above.
    from matplotlib import use as mpl_use
    mpl_use("Qt4Agg")
    ## if not showing then put plotting engine in the background
    if args.noplotshow:
        matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import matplotlib.dates as mdates

print("Temperature Logger v0.1 - MoonPunch.org")

if not args.onlyplot:
    ## Set up logging
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

    ## Find the right serial port, default settings for Linux
    serialbase = "/dev/ttyUSB"
    countbase = 0
    if (os.name) == "nt":   # modify default settings for Windows
        serialbase = "COM"
        countbase = 1

    ## Probe serial connections until one can connect
    foundserial = False
    serialport = ''
    for i in range(countbase, 20):
        try :
            serialport = "%s%i" %(serialbase, i)
            dev = serial.Serial(serialport, 115200, timeout=2)
            if len(dev.readline()) > 0:
                foundserial = True
                break
        except(OSError, serial.SerialException):
            continue

    if not foundserial:
        print("Could not find attached logger on serial/USB port.")
        sys.exit(1)
    else:
        print "Found good serial port at %s" %serialport

    print("Now logging to %s" %(logfilename))
    print("Press Ctrl-C to stop!")

    ## Setting up output file
    logger.info("#Time(Localtime),Temperature(degC),Pressure(Pa)")

    while True:
        try:
            input = dev.readline()
            if input[0] == "#" :
                continue
            now = datetime.datetime.now()
            vals = input.strip().split(',')
            temperature, pressure = float(vals[0]), int(vals[1])
            logger.info("%s,%s,%s" % (now.strftime("%Y-%m-%d %H:%M:%S.%f"),temperature,pressure))
            sys.stdout.write("Temperature: %.1f C; Pressure: %.1fhPa   \r" % (temperature,pressure/1000.0) )
            sys.stdout.flush()
        except (KeyboardInterrupt):
            break
        except (ValueError, IndexError):  # if conversion does not succeed in try section
            continue

#### Logging finished
#### Plotting section

## Might not want to plot
if args.noplot:
    sys.exit(0)

print("\n\nPlease wait, generating image from log...")

## Where does the data file come from - command line or previous logging
if args.onlyplot:
    datafile = args.onlyplot
else:
    datafile = logfilename

## Do the plotting
timestamp, temperature = np.loadtxt(datafile,
                                    unpack=True,
                                    delimiter=",",
                                    converters={ 0: mdates.strpdate2num("%Y-%m-%d %H:%M:%S.%f")},
                                    usecols=[0, 1],
                                    )

fig = plt.figure(figsize=(8, 6), dpi=80, facecolor='w', edgecolor='k')
ax = fig.add_subplot(111)

ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))

plt.plot_date(x=timestamp, y=temperature, fmt="k-")
plt.title("Temperature record from %s" %(datafile))
plt.ylabel("Temperature")
plt.xlabel("Time")
plt.ylim([min(temperature)-0.2, max(temperature)+0.2])
fig.autofmt_xdate(rotation=45)
plt.grid(True)

if not args.onlyplot:
    imagefilename = "%s.png" %(datafile)
    plt.savefig(imagefilename)
    print("=> Image saved to %s" %(imagefilename))

if not args.noplotshow:
    plt.show()
