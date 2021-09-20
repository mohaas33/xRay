// Client side implementation of UDP client-server model
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <netinet/in.h>

#include <iostream>
#include <iomanip>

#define PORT  50001
#define MAXLINE 1024

using namespace std;

int main( int argc, char *argv[])
{
  int sockfd;
  int i;
  char buffer[MAXLINE] = {0};
  struct sockaddr_in  servaddr;
  
  if ( argc < 3)
    {
      cerr << " usage: " << argv[0] << " address  message" << endl;
      return 1;
    }
  
  // Creating socket file descriptor
  if ( (sockfd = socket(AF_INET, SOCK_STREAM, 0)) < 0 )
    {
      perror("socket creation failed");
      exit(EXIT_FAILURE);
    }

  memset(&servaddr, 0, sizeof(servaddr));
  // argv[1] is the server address. We make no attempt to DNS-resolve it.
  servaddr.sin_addr.s_addr = inet_addr( argv[1]);
  servaddr.sin_port = htons(PORT);
  servaddr.sin_family = AF_INET;

  if ( connect(sockfd, (struct sockaddr*) &servaddr
               , sizeof(servaddr)) < 0 )
    {
      std::cout << "error in connect" << std::endl;
      exit(1);
    }

  
  int n = strlen(argv[2]);

  if ( n >= MAXLINE-2)
    {
      cerr << "string is too long " << endl;
      return 1;
    }
  
  buffer[0] = 2;
  memcpy ( &buffer[1], argv[2], n);
  buffer[n+1] = 3;

  // we calculate the checksum for other application although we don't need it here
  int cs = 0;
  for ( int i = 0; i < n+2; i++)
    {
      cs += buffer[i];
      cout << i << " " << hex << setw(3) << int(buffer[i]) << dec;
      if ( buffer[i] >= 32 ) cout << "  " << buffer[i]; //printable char
      cout << endl;
    }
  cs = ( (0x100 -cs) & 0x7f) | 0x40;

  write (sockfd, buffer, n+2);

  cout << "message sent." << endl;

  // we need to make a 2s timeout in case we never get a reply
  fd_set read_flag;
  FD_ZERO(&read_flag);
  FD_SET(sockfd, &read_flag);

  struct timeval tv;
  tv.tv_sec = 8;
  tv.tv_usec = 0;
  int retval = select(sockfd+1, &read_flag, 0, 0, &tv);
  if ( !retval)
    {
      cerr << "timeout waiting for response " << endl;
      return 1;
    }      

  n = read ( sockfd, buffer, MAXLINE);

  for ( int i = 0; i < n; i++)
    {
      cout << i << " " << hex << setw(3) << int(buffer[i]) << dec;
      if ( buffer[i] >= 32 ) cout << "  " << buffer[i];  // printable char
      cout << endl;
    }
  cout << endl;

  // now show us only the printable part
  for ( int i = 0; i < n; i++)
    {
      if ( buffer[i] >= 32 ) cout << buffer[i];  // printable char
    }
  cout << endl;
      

  close(sockfd);
  return 0;
}
