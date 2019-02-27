#include <stdlib.h>
#include <unistd.h>

int main()
{
	char* shellscript = "shellscript";
//	char* test = (char*)malloc(12);
	//chmod("shellscript", 777);
	//syscall(11, "testfile.txt", NULL, NULL);
	system("/home/pi/pirop/malloc_test/shellscript");
	//execve("/bin/sh", &shellscript, NULL);
	return 0;
}
