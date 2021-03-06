#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <stdarg.h>
#include <string.h>
#include <termios.h>
#include <unistd.h>
#include <fcntl.h>
#include <sys/ioctl.h>
#include <sys/types.h>
#include <sys/stat.h>

int main(int argc, char* argv[])
{
	struct termios options;
	speed_t my_baud = B115200;
	int status, fd;
	int loops = 0;
	FILE *fptr1;
	long filelength;
	int i;
	char c;

	if ((fd = open ("/dev/ttyUSB0", O_RDWR | O_NOCTTY | O_NDELAY |
			O_NONBLOCK)) == -1)
		return -1;

	tcgetattr (fd, &options) ;

	cfmakeraw   (&options) ;
	cfsetispeed (&options, my_baud) ;
	cfsetospeed (&options, my_baud) ;

	options.c_cflag |= (CLOCAL | CREAD) ;
	options.c_cflag &= ~PARENB ;
	options.c_cflag &= ~CSTOPB ;
	options.c_cflag &= ~CSIZE ;
	options.c_cflag |= CS8 ;
	options.c_lflag &= ~(ICANON | ECHO | ECHOE | ISIG) ;
	options.c_oflag &= ~OPOST ;

	options.c_cc [VMIN]  =   0 ;
	options.c_cc [VTIME] = 100 ;	// Ten seconds (100 deciseconds)

	tcsetattr (fd, TCSANOW, &options) ;

	ioctl (fd, TIOCMGET, &status);

	status |= TIOCM_DTR ;
	status |= TIOCM_RTS ;

	ioctl (fd, TIOCMSET, &status);

	usleep (10000) ;	// 10mS

	fptr1 = fopen(argv[1], "r");
	if (fptr1 == NULL)
	{
		printf("Cannot open file %s \n", argv[1]);
		exit(0);
	}

	fseek(fptr1, 0, SEEK_END);
	filelength = ftell(fptr1);
	printf("Filelength in bytes: %ld\n", filelength);

	rewind(fptr1);
	// Read contents from file
	c = fgetc(fptr1);
	for (i = 1; i < filelength; ++i)
	{
		++loops;
		printf("Sending Character: %d\n", (uint8_t)c);
		write(fd, &c, 1);
		c = fgetc(fptr1);
	}
	printf("Number of bytes sent: %d\n", loops+ 1);
	return 0;
}
