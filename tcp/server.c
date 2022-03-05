#include <stdio.h>
#include <stdlib.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <netinet/in.h>
#include <string.h>

void sendfile(int connectfd);

int main(int argc, char const *argv[])
{
	int listenfd;
	socklen_t addrlen;
	int connectfd;

	if ((listenfd = socket(AF_INET, SOCK_STREAM, 0)) == -1) // create server socket
	{
		printf("create socket error\n");
		exit(0);
	}

	// set socket option
	int option = SO_REUSEADDR;
	setsockopt(listenfd, SOL_SOCKET, SO_REUSEADDR, &option, sizeof(option));

	struct sockaddr_in server, client;

	// set server option
	memset(&server, 0, sizeof(server));
	server.sin_family = AF_INET;
	server.sin_port = htons(11235);
	server.sin_addr.s_addr = htonl(INADDR_ANY);

	if (bind(listenfd, (struct sockaddr *)&server, sizeof(server)) == -1)
	{
		printf("bind error\n");
		exit(0);
	}

	if (listen(listenfd, 1) == -1) //listen, just accept 1 connection
	{
		printf("listen error\n");
		exit(0);
	}

	if ((connectfd = accept(listenfd, (struct sockaddr *)&client, &addrlen)) == -1) // waiting for connection
	{
		printf("accept error\n");
		exit(0);
	}

	sendfile(connectfd);

	printf("\nsend over\n");

	shutdown(connectfd, SHUT_WR);
	shutdown(listenfd, SHUT_RDWR);
	return 0;
}

void sendfile(int connectfd)
{

	char buf;
	int num = 0;
	FILE *f = fopen("./send", "r");
	buf = fgetc(f);
	do
	{
		send(connectfd, &buf, 1, 0);
		num ++;
		printf("Have sent: %d bytes\r", num); //show progress
		buf = fgetc(f);
	} while (buf != EOF);
	fclose(f);
}
