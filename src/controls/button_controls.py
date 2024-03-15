#!/usr/bin/python3
import os
from fcntl import ioctl

# ioctl commands defined at the pci driver
RD_SWITCHES   = 24929
RD_PBUTTONS   = 24930

fd = os.open("/dev/mydev", os.O_RDWR)

def read_button ():
    ioctl(fd, RD_PBUTTONS)
    button = os.read(fd, 4)
    return {int(bin(int.from_bytes(button, 'little')), 2)} # read 4 bytes and store in red var
    
def read_switchs():
    ioctl(fd, RD_SWITCHES)
    switch = os.read(fd, 4) # read 4 bytes and store in rad var
    return {int(bin(int.from_bytes(switch, 'little')), 2)}