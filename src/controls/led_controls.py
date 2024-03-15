import os
from fcntl import ioctl

WR_RED_LEDS   = 24933
WR_GREEN_LEDS = 24934

def set_green_leds(leds):
    if(len(leds) > 9): return
    led = leds[0]
    for i in range(1,len(leds)):
        led = (led << 1) | leds[i]
    fd = os.open("/dev/mydev", os.O_RDWR)
    ioctl(fd, WR_GREEN_LEDS)
    retval = os.write(fd, led.to_bytes(4, 'little'))
    os.close(fd)

def set_red_leds(leds):
    if(len(leds) > 18): return
    led = leds[0]
    for i in range(1,len(leds)):
        led = (led << 1) | leds[i]
    fd = os.open("/dev/mydev", os.O_RDWR)
    ioctl(fd, WR_RED_LEDS)
    retval = os.write(fd, led.to_bytes(4, 'little'))
    os.close(fd)

