import os
from fcntl import ioctl

WR_L_DISPLAY = 24931
WR_R_DISPLAY = 24932
hex0 = 0b11000000
hex1 = 0b11111001
hex2 = 0b10100100
hex3 = 0b10110000
hex4 = 0b10011001
hex5 = 0b10010010
hex6 = 0b10000010
hex7 = 0b11111000
hex8 = 0b10000000
hex9 = 0b10010000
numbers = [hex0, hex1, hex2, hex3, hex4, hex5, hex6, hex7, hex8, hex9]

#display direito vai ser usado para um numero de 4 digitos

def right_display_write(number):
    fd = os.open("/dev/mydev", os.O_RDWR)
    ioctl(fd, WR_R_DISPLAY)
    #primeiro digito
    result = numbers[int(number/ 1000)]
    #segundo digito
    result = (result << 8) | numbers[int((number % 1000) / 100)]
    #terceiro digito
    result = (result << 8) | numbers[int((number % 100) / 10)]
    #quarto digito
    result = (result << 8) | numbers[(number % 10)]
    retval = os.write(fd, result.to_bytes(4, 'little'))
    os.close(fd)

#display esquerdo vai ser usado para dois numeros de 2 digitos

def left_display_write(num1, num2):
    fd = os.open("/dev/mydev", os.O_RDWR)
    ioctl(fd, WR_L_DISPLAY)
    #primeiro digito do num1
    result = numbers[int(num2 / 10)]
    #segundo digito do num1
    result = (result << 8) | result = numbers[(num2 % 10)]
    #primeiro digito do num2
    result = numbers[int((num1 / 10)]
    #segundo digito do num2
    result = (result << 8) | numbers[int((num1 % 10))]
    retval = os.write(fd, result.to_bytes(4, 'little'))
    os.close(fd)
