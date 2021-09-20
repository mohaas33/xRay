// Server side implementation of UDP client-server model
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <netinet/in.h>

#define PORT  50001
#define MAXLINE (1024*2)

#include <iostream>
#include <iomanip>

using namespace std;

int main( int argc, char *argv[])
{
  int sockfd;
  int in_fd;
  int i;
  char buffer[MAXLINE];
  struct sockaddr_in servaddr, cliaddr;

  const char *reply = "Thank you";
  
  // Creating socket file descriptor
  if ( (sockfd = socket(AF_INET, SOCK_STREAM, 0)) < 0 )
    {
      perror("socket creation failed");
      exit(EXIT_FAILURE);
    }
  
  memset(&servaddr, 0, sizeof(servaddr));
  
  // Filling server information
  servaddr.sin_family = AF_INET; // IPv4
  servaddr.sin_addr.s_addr = INADDR_ANY;
  servaddr.sin_port = htons(PORT);

  // Bind the socket with the server address
  if ( bind(sockfd, (const struct sockaddr *)&servaddr,
	    sizeof(servaddr)) < 0 )
    {
      perror("bind failed");
      exit(EXIT_FAILURE);
    }
  
  listen(sockfd, 1);
  
  unsigned int len, n;

  while (sockfd > 0)
    {
      len = sizeof(cliaddr); 
      memset(&cliaddr, 0, sizeof(cliaddr));

      in_fd = accept(sockfd,  (struct sockaddr *) &cliaddr, &len);

      if ( in_fd < 0)
	{
	  continue;
	}
	
      n = read ( in_fd, buffer, MAXLINE);
      for ( int i = 0; i < n; i++)
	  {
	    cout << i << " " << hex << setw(3) << int(buffer[i]) << dec;
	    if ( buffer[i] >= 32 ) cout << "  " << buffer[i];  // printable char
	    cout << endl;
	  }

      write (in_fd, reply, strlen(reply) +1);
      close (in_fd);
      in_fd = 0;
    }
      

  return 0;
}
