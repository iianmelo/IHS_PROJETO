#!/usr/bin/python3
import controls.board as board


def read_button():
    read = int(bin(board.read_u32(board.RD_PBUTTONS)), 2)
    if read == 7:
        return 1
    elif read == 11:
        return 2
    elif read == 13:
        return 3
    elif read == 14:
        return 4
    else:
        return 0


def read_switchs():
    return int(bin(board.read_u32(board.RD_SWITCHES)), 2)
