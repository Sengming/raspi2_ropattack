ifneq ($V,1)
Q ?= @
endif

DEBUG	= -g -O0 -fno-stack-protector
#DEBUG	= -O3
CC	= gcc
INCLUDE	= -I/usr/local/include
CFLAGS	= $(DEBUG) -Wall $(INCLUDE) -Winline -pipe

LDFLAGS	= -L/usr/local/lib
LDLIBS    = 

SRC	=	uart_sender.c

OBJ	=	$(SRC:.c=.o)

BINS	=	$(SRC:.c=)


all: sender
	$Q echo "    $(BINS)" | fmt
	$Q echo ""

sender:	uart_sender.o
	$Q echo [link]
	$Q $(CC) -o $@ $< $(LDFLAGS) $(LDLIBS)

.c.o:
	$Q echo [CC] $<
	$Q $(CC) -c $(CFLAGS) $< -o $@


