# Makefile by Matheus Souza (github.com/mfbsouza)
# O jogo em si e Python. O alvo padrao confere a sintaxe e compila os exemplos em C.
# make run abre o jogo. Sem a placa DE2i-150 ele usa o teclado.

.DEFAULT_GOAL := check

PYTHON := python3
APPDIR := src/app

.PHONY: check run examples driver

check:
	$(PYTHON) -m py_compile \
		$(APPDIR)/car_game.py \
		$(APPDIR)/assets.py \
		$(APPDIR)/controls/board.py \
		$(APPDIR)/controls/button_controls.py \
		$(APPDIR)/controls/display_controls.py \
		$(APPDIR)/controls/led_controls.py
	@echo "python ok. para jogar: make run"

run:
	@$(PYTHON) -c "import pygame" || { echo "falta o pygame. no Debian/Ubuntu: sudo apt install python3-pygame"; exit 1; }
	cd $(APPDIR) && $(PYTHON) -u car_game.py

examples:
	@mkdir -p target
	gcc -Wall -I include -o target/app-pci exemples/c/app-pci.c
	gcc -Wall -I include -o target/app-char exemples/c/app-char.c
	@echo "binarios em target/. eles abrem /dev/mydev e precisam da placa."

driver:
	@if [ ! -d "/lib/modules/$$(uname -r)/build" ]; then \
		echo "sem headers do kernel $$(uname -r). o modulo PCI nao compila nesta maquina."; \
		exit 1; \
	fi
	$(MAKE) -C driver/pci
	$(MAKE) -C driver/char

# project name
PROJECT  := app

# paths
BUILDDIR := ./target
DBGDIR   := $(BUILDDIR)/debug
RELDIR   := $(BUILDDIR)/release
INCDIR   := ./include

# compiler and binutils
PREFIX :=
CC     := $(PREFIX)gcc
AS     := $(PREFIX)nasm
CXX    := $(PREFIX)g++
OD     := $(PREFIX)objdump

# flags
CFLAGS   := -Wall -I $(INCDIR) -MMD -MP
CXXFLAGS := -Wall -I $(INCDIR) -MMD -MP
ASMFLAGS := -f elf
LDFLAGS  :=

ifeq ($(DEBUG),1)
	BINDIR    := $(DBGDIR)
	OBJDIR    := $(DBGDIR)/obj
	CFLAGS    += -g -O0 -DDEBUG
	CXXFLAGS  += -g -O0 -DDEBUG
else
	BINDIR    := $(RELDIR)
	OBJDIR    := $(RELDIR)/obj
	CFLAGS    += -g -O3 -DNDEBUG
	CXXFLAGS  += -g -O3 -DNDEBUG
endif

# sources to compile
ALLCSRCS   += $(shell find ./src -type f -name *.c)
ALLCXXSRCS += $(shell find ./src -type f -name *.cpp)
ALLASMSRCS += $(shell find ./src -type f -name *.asm)

# set the linker to g++ if there is any c++ source code
ifeq ($(ALLCXXSRCS),)
        LD := $(PREFIX)gcc
else
        LD := $(PREFIX)g++
endif

# objects settings
COBJS   := $(addprefix $(OBJDIR)/, $(notdir $(ALLCSRCS:.c=.o)))
CXXOBJS := $(addprefix $(OBJDIR)/, $(notdir $(ALLCXXSRCS:.cpp=.o)))
ASMOBJS := $(addprefix $(OBJDIR)/, $(notdir $(ALLASMSRCS:.asm=.o)))
OBJS    := $(COBJS) $(CXXOBJS) $(ASMOBJS)
DEPS    := $(OBJS:.o=.d)

# paths where to search for sources
SRCPATHS := $(sort $(dir $(ALLCSRCS)) $(dir $(ALLCXXSRCS)) $(dir $(ALLASMSRCS)))
VPATH     = $(SRCPATHS)

# output
OUTFILES := $(BINDIR)/$(PROJECT) $(BUILDDIR)/$(PROJECT).lst

# targets
.PHONY: all clean

all: $(OBJDIR) $(BINDIR) $(OBJS) $(OUTFILES)

# targets for the dirs
$(OBJDIR):
	@mkdir -p $(OBJDIR)

$(BINDIR):
	@mkdir -p $(BINDIR)

# target for c objects
$(COBJS) : $(OBJDIR)/%.o : %.c
ifeq ($(VERBOSE),1)
	$(CC) -c $(CFLAGS) $< -o $@
else
	@echo -n "[CC] \t$<\n"
	@$(CC) -c $(CFLAGS) $< -o $@
endif

# target for cpp objects
$(CXXOBJS) : $(OBJDIR)/%.o : %.cpp
ifeq ($(VERBOSE),1)
	$(CXX) -c $(CXXFLAGS) $< -o $@
else
	@echo -n "[CXX]\t$<\n"
	@$(CXX) -c $(CXXFLAGS) $< -o $@
endif

# target for asm objects
$(ASMOBJS) : $(OBJDIR)/%.o : %.asm
ifeq ($(VERBOSE),1)
	$(AS) $(ASMFLAGS) $< -o $@
else
	@echo -n "[AS] \t$<\n"
	@$(AS) $(ASMFLAGS) $< -o $@
endif

# target for ELF file
$(BINDIR)/$(PROJECT): $(OBJS)
ifeq ($(strip $(OBJS)),)
	@echo "sem fontes C/C++/ASM em src/. o jogo e o alvo 'make run'."
else ifeq ($(VERBOSE),1)
	$(LD) $(LDFLAGS) $(OBJS) -o $@
else
	@echo -n "[LD] \t./$@\n"
	@$(LD) $(LDFLAGS) $(OBJS) -o $@
endif

# target for disassembly and sections header info
$(BUILDDIR)/$(PROJECT).lst: $(BINDIR)/$(PROJECT)
ifeq ($(strip $(OBJS)),)
	@true
else ifeq ($(VERBOSE),1)
	$(OD) -h -S $< > $@
else
	@echo -n "[OD] \t./$@\n"
	@$(OD) -h -S $< > $@
endif

# target for cleaning files
clean:
	rm -rf $(BUILDDIR)

# include the dependency files, should be the last of the makefile
-include $(DEPS)
