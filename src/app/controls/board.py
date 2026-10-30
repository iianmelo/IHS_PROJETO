"""Acesso aos perifericos da DE2i-150.

Se /dev/mydev existir, as chamadas vao para o driver PCI.
Se a placa nao estiver na maquina, os mesmos registradores ficam na memoria
e os botoes saem do teclado. DE2I_MOCK=1 forca esse caminho.
"""

import os
from fcntl import ioctl

RD_SWITCHES = 24929
RD_PBUTTONS = 24930
WR_L_DISPLAY = 24931
WR_R_DISPLAY = 24932
WR_RED_LEDS = 24933
WR_GREEN_LEDS = 24934

DEV_PATH = "/dev/mydev"

_fd = None
MOCK = os.environ.get("DE2I_MOCK", "") == "1"
if not MOCK:
    try:
        _fd = os.open(DEV_PATH, os.O_RDWR)
    except OSError:
        MOCK = True

red_leds = 0
green_leds = 0
display_l = 0
display_r = 0
_last_log = None

# Padroes do display de 7 segmentos usados em display_controls.py.
_SEG = {
    0b11000000: "0",
    0b11111001: "1",
    0b10100100: "2",
    0b10110000: "3",
    0b10011001: "4",
    0b10010010: "5",
    0b10000010: "6",
    0b11111000: "7",
    0b10000000: "8",
    0b10010000: "9",
}


def _digits(word):
    chars = []
    for shift in (24, 16, 8, 0):
        chars.append(_SEG.get((word >> shift) & 0xFF, "?"))
    return "".join(chars)


def _status_line():
    return (
        "[de2i] LED_R={:018b} LED_G={:09b} 7SEG_L={} 7SEG_R={}".format(
            red_leds & ((1 << 18) - 1),
            green_leds & ((1 << 9) - 1),
            _digits(display_l),
            _digits(display_r),
        )
    )


def _log_status():
    global _last_log
    line = _status_line()
    if line != _last_log:
        print(line, flush=True)
        _last_log = line


def _mock_buttons():
    """Botoes ativos em nivel baixo, mesmo codigo lido da placa.

    7 esquerda, 11 tiro, 13 recarga, 14 direita, 15 nenhum.
    """
    try:
        import pygame
    except ImportError:
        return 0xF
    if not pygame.get_init():
        return 0xF
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        return 7
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        return 14
    if keys[pygame.K_SPACE] or keys[pygame.K_UP] or keys[pygame.K_w]:
        return 11
    if keys[pygame.K_r] or keys[pygame.K_DOWN] or keys[pygame.K_s]:
        return 13
    return 0xF


def read_u32(cmd):
    if MOCK:
        if cmd == RD_PBUTTONS:
            return _mock_buttons()
        if cmd == RD_SWITCHES:
            return 0
        return 0
    ioctl(_fd, cmd)
    data = os.read(_fd, 4)
    return int.from_bytes(data, "little")


def write_u32(cmd, value):
    global red_leds, green_leds, display_l, display_r
    if MOCK:
        if cmd == WR_RED_LEDS:
            red_leds = value
        elif cmd == WR_GREEN_LEDS:
            green_leds = value
        elif cmd == WR_L_DISPLAY:
            display_l = value
        elif cmd == WR_R_DISPLAY:
            display_r = value
        _log_status()
        return 4
    fd = os.open(DEV_PATH, os.O_RDWR)
    try:
        ioctl(fd, cmd)
        return os.write(fd, int(value).to_bytes(4, "little"))
    finally:
        os.close(fd)


def draw_overlay(screen, top):
    """Faixa com o estado que iria para LEDs e displays da placa."""
    import pygame

    width = screen.get_width()
    height = screen.get_height() - top
    panel = pygame.Surface((width, height))
    panel.fill((0, 0, 0))
    screen.blit(panel, (0, top))
    font = pygame.font.SysFont("dejavusansmono", 15)
    lines = [
        "DE2i-150 simulada   /dev/mydev ausente",
        "LED R  " + format(red_leds & ((1 << 18) - 1), "018b"),
        "LED G  " + format(green_leds & ((1 << 9) - 1), "09b"),
        "7SEG L {}    7SEG R {}".format(_digits(display_l), _digits(display_r)),
        "teclas  A/esq  D/dir  espaco tiro  R recarga  ESC sai",
    ]
    y = top + 6
    for line in lines:
        screen.blit(font.render(line, True, (230, 230, 230)), (8, y))
        y += 17
