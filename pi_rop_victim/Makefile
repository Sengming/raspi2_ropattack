ifneq ($V,1)
Q ?= @
endif

DEBUG	= -O0 -fno-stack-protector -g
CC	= gcc
INCLUDE	= -I/usr/local/include
CFLAGS	= $(DEBUG) -Wall $(INCLUDE) -Winline -pipe 

LDFLAGS	= -L/usr/local/lib
LDLIBS    = -lwiringPi -lwiringPiDev -lpthread -lm -lcrypt -lrt

SRC	=	rop_victim.c

OBJ	=	$(SRC:.c=.o)

BINS	=	$(SRC:.c=)


all: rop_victim 
	$Q echo "    $(BINS)" | fmt
	$Q echo ""

rop_victim:	rop_victim.o
	$Q echo [link]
	$Q $(CC) -o $@ rop_victim.o $(LDFLAGS) $(LDLIBS)

.c.o:
	$Q echo [CC] $<
	$Q $(CC) -c $(CFLAGS) $< -o $@

clean:
	$Q echo "[Clean]"
	$Q rm -f $(OBJ) *~ core tags $(BINS)
	$Q rm -f log.txt temp.txt

asm: rop_victim.c
	$Q echo [CC_ASM] $<
	$Q $(CC) -S $(CFLAGS) $<


asm_link:
	$Q echo [link_asm]
	$Q $(CC) rop_victim.s -o rop_victim $(LDFLAGS) $(LDLIBS)

fileclean:
	$Q rm -f log.txt temp.txt


