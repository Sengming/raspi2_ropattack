#
# Makefile:
#	wiringPi - A "wiring" library for the Raspberry Pi
#	https://projects.drogon.net/wiring-pi
#
#	Copyright (c) 2012-2015 Gordon Henderson
#################################################################################
# This file is part of wiringPi:
#	Wiring Compatable library for the Raspberry Pi
#
#    wiringPi is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Lesser General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    wiringPi is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Lesser General Public License for more details.
#
#    You should have received a copy of the GNU Lesser General Public License
#    along with wiringPi.  If not, see <http://www.gnu.org/licenses/>.
#################################################################################

ifneq ($V,1)
Q ?= @
endif

DEBUG	= -g -O0 -fno-stack-protector
#DEBUG	= -O3
CC	= gcc
INCLUDE	= -I/usr/local/include
CFLAGS	= $(DEBUG) -Wall $(INCLUDE) -Winline -pipe

LDFLAGS	= -L/usr/local/lib
LDLIBS    = -lwiringPi -lwiringPiDev -lpthread -lm -lcrypt -lrt

# Should not alter anything below this line
###############################################################################

SRC	=	serialRead.c

OBJ	=	$(SRC:.c=.o)

BINS	=	$(SRC:.c=)

all: serialRead	
	$Q echo "    $(BINS)" | fmt
	$Q echo ""

really-all:	$(BINS)

serialRead:	serialRead.o
	$Q echo [link]
	$Q $(CC) -o $@ serialRead.o $(LDFLAGS) $(LDLIBS)

.c.o:
	$Q echo [CC] $<
	$Q $(CC) -c $(CFLAGS) $< -o $@

clean:
	$Q echo "[Clean]"
	$Q rm -f $(OBJ) *~ core tags $(BINS)
	$Q rm -f log.txt temp.txt

fileclean:
	$Q rm -f log.txt temp.txt

tags:	$(SRC)
	$Q echo [ctags]
	$Q ctags $(SRC)

depend:
	makedepend -Y $(SRC)

# DO NOT DELETE
