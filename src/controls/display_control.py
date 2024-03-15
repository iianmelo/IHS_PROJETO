import os
from fcntl import ioctl

WR_L_DISPLAY = 24931
WR_R_DISPLAY = 24932
hex0 = 0b1111110
hex1 = 0b0110000
hex2 = 0b1101101
hex3 = 0b1111001
hex4 = 0b0110011
hex5 = 0b1011011
hex6 = 0b1011111
hex7 = 0b1110000
hex8 = 0b1111111
hex9 = 0b1111011
numbers = [hex0, hex1, hex2, hex3, hex4, hex5, hex6, hex7, hex8, hex9]

#display direito vai ser usado para um numero de 4 digitos

def right_display_write(number):
    fd = os.open("/dev/mydev", os.O_RDWR)
    ioctl(fd, WR_R_DISPLAY)
    #primeiro digito
    result = numbers[(number % 10)] << 7
    #segundo digito
    result = (result << 7) | numbers[int((number % 100) / 10)]
    #terceiro digito
    result = (result << 7) | numbers[int((number % 1000) / 100)]
    #quarto digito
    result = (result << 7) | numbers[int(number/ 1000)]
    retval = os.write(fd, result.to_bytes(4, 'little'))
    os.close(fd)

#display esquerdo vai ser usado para dois numeros de 2 digitos

def left_display_write(num1, num2):
    fd = os.open("/dev/mydev", os.O_RDWR)
    ioctl(fd, WR_L_DISPLAY)
    #primeiro digito do num1
    result = numbers[(num2 % 10)] << 8
    #segundo digito do num1
    result = (result << 7) | numbers[int((num2 % 100) / 10)]
    #terceiro digito do num2
    result = (result << 7) | numbers[int((num1 % 10))]
    #quarto digito do num2
    result = (result << 7) | numbers[int((num1 % 100) / 10)]
    retval = os.write(fd, result.to_bytes(4, 'little'))
    os.close(fd)
