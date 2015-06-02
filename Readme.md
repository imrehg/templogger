# Temperature Logger

Temperature logger module working with an Arduino and a BMP085 
temperature/barometric sensor module.

Features:

* Automatic serial port selection (under most circumstances) on Linux and Windows
* Continuous logging and display of current readings in console
* Automatic plotting at the end of the recording
* Adjustable parameters (run with `-h` to check command line arguments)

## Usage

Run directly with `python2 templogger.py`, or generate stand-alone executive
with `genexec.sh` (on Linux) or `genexec.bat` (on Windows) - the resulting
file will be in the `dist` subdirectory.

Get the command line options by running `--help`. Run the program without
any arguments to start logging. Use `--onlyplot FILENAME` to plot results
from an existing log.

## License

The MIT License (MIT)

Copyright (c) 2014 Gergely Imreh <imrehg@gmail.com>

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
