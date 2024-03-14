#!/usr/bin/python3

import os, sys
from fcntl import ioctl

# ioctl commands defined at the pci driver
RD_SWITCHES   = 24929
RD_PBUTTONS   = 24930
WR_L_DISPLAY  = 24931
WR_R_DISPLAY  = 24932
WR_RED_LEDS   = 24933
WR_GREEN_LEDS = 24934

def main():
    if len(sys.argv) < 2:
        print("Error: expected more command line arguments")
        print("Syntax: %s </dev/device_file>"%sys.argv[0])
        exit(1)

    fd = os.open("/dev/mydev", os.O_RDWR)
    #data = 0b0
    data1 = 0b010000000
    ioctl(fd, WR_GREEN_LEDS)
    retval = os.write(fd, data1.to_bytes(4, 'little'))
    
    #data2 = 0b111000111000111000  
    #ioctl(fd, WR_RED_LEDS)
    #retval = os.write(fd, data2.to_bytes(4, 'little'))
    
    
    #data = 0x40404040;
    #data1 = 0x79243019;
    #ioctl(fd, WR_L_DISPLAY)
    #retval = os.write(fd, data1.to_bytes(4, 'little'))
    #print("wrote %d bytes"%retval)
    #data2 = 0x12027800;
    #ioctl(fd, WR_R_DISPLAY)
    #retval = os.write(fd, data2.to_bytes(4, 'little'))
    #print("wrote %d bytes"%retval)

	
    ioctl(fd, RD_PBUTTONS)
    red = os.read(fd, 4); # read 4 bytes and store in red var
    #print("button 0x%X"%int.from_bytes(red, 'little'))

    ioctl(fd, RD_SWITCHES)
    rad = os.read(fd, 4); # read 4 bytes and store in rad var
    #print("switch 0x%X"%int.from_bytes(rad, 'little'))
    
    print(f"button: {int(bin(int.from_bytes(red, 'little')), 2)} | switches: {bin(int.from_bytes(rad, 'little'))}")

    os.close(fd)

if __name__ == '__main__':
    while True:
        main()

