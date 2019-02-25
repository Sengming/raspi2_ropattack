/* This program updates a log file via uart after copying saved data from a
 * sensor or another module
 * SengMing Yeoh <sengming@vt.edu>
 */

#include <stdio.h>
#include <string.h>
#include <errno.h>
#include <unistd.h>
#include <wiringSerial.h>
#include <stdint.h>
#include <fcntl.h>
#include <sys/stat.h>
//#define DEBUGFILE
//#define BUFSIZE			(100)
#define BUFSIZE			(10)
#define FIRST_PACKET_SIZE	(4)

union payload_size {
	uint32_t frame_size;
	struct {
		uint8_t byte[FIRST_PACKET_SIZE];
	};
};

void secret()
{
	int fd;
	fd = open("secret_accessed.txt", O_CREAT|O_RDWR);
	close(fd);
}

/* Start receiving log data from sensor's log file*/
void receive_serial(int serial_driver, int local_log)
{
	uint8_t buffer[BUFSIZE];
	union payload_size first_packet = {0};

	/* Read in the first packet message to see how long our log will be */
	read(serial_driver, &first_packet.byte, FIRST_PACKET_SIZE);
	printf("Payload size: %u\n", first_packet.frame_size);
	/* Sleep here for one second to allow all the other bytes to arrive, */
	sleep(1);
	/* Next, read the remaining payload based on size*/
	read(serial_driver, &buffer, first_packet.frame_size);
	write(local_log, &buffer, first_packet.frame_size);
	close(local_log);
}

int main ()
{
	int serial_port, local_log;

#ifdef DEBUGFILE
	if ((serial_port = open("/dev/stdin", O_RDWR)) < 0)
	{
		fprintf (stderr, "Unable to open serial device: %s\n",
			 strerror (errno)) ;
		return 1 ;
	}
#else
	if ((serial_port = serialOpen ("/dev/ttyAMA0", 115200)) < 0)
	{
		fprintf (stderr, "Unable to open serial device: %s\n",
			 strerror (errno)) ;
		return 1 ;
	}
#endif

	if ((local_log = open("log.txt", O_RDWR | O_CREAT)) < 0)
	{
		fprintf (stderr, "Unable to open local log: %s\n",
			 strerror (errno)) ;
		return 1 ;
	}

// Loop, Reading sensor data

	//for (;;)
	//{
		receive_serial(serial_port, local_log);
		//putchar (serialGetchar (serial_port)) ;
	//}
	return 0;
}
