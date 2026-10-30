import controls.board as board


def set_green_leds(leds):
    if len(leds) > 9:
        return
    led = leds[0]
    for i in range(1, len(leds)):
        led = (led << 1) | leds[i]
    board.write_u32(board.WR_GREEN_LEDS, led)


def set_red_leds(leds):
    if len(leds) > 18:
        return
    led = leds[0]
    for i in range(1, len(leds)):
        led = (led << 1) | leds[i]
    board.write_u32(board.WR_RED_LEDS, led)
