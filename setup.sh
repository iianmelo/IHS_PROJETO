#!/bin/bash

GREEN='\033[0;32m'
CLEAR='\033[0m'

echo -e "$GREEN CONFERINDO O JOGO $CLEAR"
make check

echo -e "$GREEN COMPILANDO EXEMPLOS EM C $CLEAR"
make examples

echo -e "$GREEN DRIVER PCI $CLEAR"
if [ -d "/lib/modules/$(uname -r)/build" ]; then
    make -C driver/pci
    make -C driver/char
else
    echo "headers do kernel $(uname -r) ausentes. o .ko nao sai nesta maquina."
fi

if lspci -d 1172:0004 >/dev/null 2>&1; then
    echo -e "$GREEN PLACA DE2i-150 PRESENTE $CLEAR"
    echo "para carregar o modulo: sudo insmod driver/pci/de2i-150.ko && sudo chmod 666 /dev/mydev"
else
    echo -e "$GREEN PLACA DE2i-150 AUSENTE $CLEAR"
    echo "o jogo abre em simulacao, com o teclado no lugar dos botoes."
    echo "comando: make run"
fi
