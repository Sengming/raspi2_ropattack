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
#define BUFSIZE			(100)
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
int receive_serial(int serial_driver, int local_log)
{
	uint8_t buffer[BUFSIZE];
	union payload_size first_packet = {0};

	/* Read in the first packet message to see how long our log will be */
	read(serial_driver, &first_packet.byte, FIRST_PACKET_SIZE);
	printf("Payload size: %u\n", first_packet.frame_size);
	if (first_packet.frame_size > 0)
	{
		/* Sleep here for a few seconds to allow all the other bytes to arrive, */
		sleep(1);

		/* Next, read the remaining payload based on size*/
		read(serial_driver, &buffer, first_packet.frame_size);
		serialFlush(serial_driver);
		/* Write to the log file */
		write(local_log, &buffer, first_packet.frame_size);
		close(local_log);

		/* All good, read data correctly*/
		return 0;
	}
	else {
		close(local_log);
		remove("/home/pi/pirop/temp.txt");
		/* 0 bytes read, we failed, try again! */
		return 1;
	}
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

	for (;;) {
		if (access("/home/pi/pirop/log.txt", F_OK != -1)){
			/* Log already exists , we'll need to create a new temporary one
			 * and swap them out once write is complete
			 */
			if ((local_log = open("/home/pi/pirop/temp.txt", O_RDWR | O_CREAT |
					      O_APPEND)) < 0)
			{
				fprintf (stderr, "Unable to open local temp: %s\n"
					 ,strerror (errno)) ;
				return 1 ;
			}

			/* Actually receive the data from other device */
			if (receive_serial(serial_port, local_log) != 1){
				printf("log.txt exists\n");
				/* When we're done, swap the files around */
				remove("/home/pi/pirop/log.txt");
				rename("/home/pi/pirop/temp.txt",
				       "/home/pi/pirop/log.txt");
			}
		}
		else {
			/* No log exists yet, let's create one */

			if ((local_log = open("/home/pi/pirop/log.txt", O_RDWR | O_CREAT)) < 0)
			{
				fprintf (stderr, "Unable to open local log: %s\n"
					 ,strerror (errno)) ;
				return 1 ;
			}
			printf("log.txt doesn't exist\n");
			/* Actually receive the data from other device */
			receive_serial(serial_port, local_log);
		}

	}
	return 0;
}
