# Python-Thermal-Printer Module

Python3 port of the original Adafruit [Python-Thermal-Printer](https://github.com/adafruit/Python-Thermal-Printer) library.

## Getting Started

Install Raspbian Buster and Wire the printer according to [this](https://learn.adafruit.com/networked-thermal-printer-using-cups-and-raspberry-pi/connect-and-configure-printer). I powered the printer with the GPIO pins as well.

Run a test to see if the printer is working by punching in these commands into the terminal.

``` shell
stty -F /dev/serial0 19200
echo -e "This is a test.\\n\\n\\n" > /dev/serial0
```

### Installing

Update the system and install prerequisites.

``` shell
sudo apt-get update
sudo apt-get install git cups wiringpi build-essential libcups2-dev libcupsimage2-dev python3-serial python-pil python-unidecode
```

Install the printer driver. Don't worry about the warnings that g++ gives.

``` shell
sudo apt-get install libcups2-dev libcupsimage2-dev g++ cups cups-client
git clone https://github.com/adafruit/zj-58
cd zj-58
make
sudo ./install
```

Make the printer the default printer. This is useful if you are going to be doing other things with it.

``` shell
sudo lpadmin -p ZJ-58 -E -v serial:/dev/serial0?baud=19200 -m zjiang/ZJ-58.ppd
sudo lpoptions -d ZJ-58
```

Restart the system. Clone this repository and try to run *printertest.py*.

``` shell
git clone https://github.com/grndnl/rpi-printer/
cd rpi-printer
python printertest.py
```


## Usage

### Email printer
```
nohup python email_printer.py &
```

### Echo printer from ssh
```
python echo_printer.py
```

### Road updates printer

Install:
```
python -m venv venv
source venv/bin/activate
pip install requests beautifulsoup4 pyserial qrcode[pil]
```

Test:
```
python road_updates_printer.py
```

Run in background:
```
nohup /home/admin/rpi-printer/venv/bin/python road_updates_printer.py > log-road.txt 2>&1 &
```

Kill:
```
ps aux | grep road_updates_printer.py
kill <PID>
```
