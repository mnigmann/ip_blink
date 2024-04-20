# IP address blinker

This repository contains a Python script that can be installed on a Raspberry Pi.
When executed, the script will query the Pi's IP address and blink the green LED
on the Pi to indicate the IP address.

## LED protocol

To communicate a single digit, the script will light the LED for 1 second, and then
pulse the LED for 0.3 seconds every 0.3 seconds. The number of pulses corresponds
to the value of the digit. To communicate a multi-digit number, the script will
communicate each digit of that number with a 1 second pause between them. To
communicate a whole IP address, the script will communicate each octet with a 2
second pause between them. Finally, the whole transmission is repeated forever
with a 10 second pause between transmissions.

Using this method, a whole IP address could take over a minute to communicate.
However, encoding the IP address in this way allows the IP address to be 
immediately identified without requiring any conversions or code tables.

## Execution
The script must be run as root. You can also add `sudo /path/to/file/ip_blink.py &`
to `/etc/rc.local` to run the script automatically on boot.
