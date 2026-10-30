import controls.board as board

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


def right_display_write(number):
    if number > 9999 or number < 0:
        return
    result = numbers[int(number / 1000)]
    result = (result << 8) | numbers[int(number % 1000 / 100)]
    result = (result << 8) | numbers[int(number % 100 / 10)]
    result = (result << 8) | numbers[number % 10]
    board.write_u32(board.WR_R_DISPLAY, result)


def left_display_write(num1, num2):
    if num1 > 99 or num1 < 0 or num2 > 99 or num2 < 0:
        return
    result = numbers[int(num2 / 10)]
    result = (result << 8) | numbers[num2 % 10]
    result = (result << 8) | numbers[int(num1 / 10)]
    result = (result << 8) | numbers[num1 % 10]
    board.write_u32(board.WR_L_DISPLAY, result)
