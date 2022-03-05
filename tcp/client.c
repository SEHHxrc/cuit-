#include <sys/socket.h>
#include <stdio.h>
#include <stdlib.h>
#include <arpa/inet.h>
#include <netinet/in.h>
#include <netdb.h>

int write(int socketfd);

int main(int argc, char const *argv[])
{
	struct sockaddr_in serveradd;
	int socketfd;
	int num;

	if (argc != 2)
	{
		printf("Usage:%s ipaddress\n", argv[0]);
		exit(0);
	}

	if ((socketfd = socket(AF_INET, SOCK_STREAM, 0)) == -1) // create socket
	{
		printf("create socket error\n");
		exit(0);
	}

	serveradd.sin_family = AF_INET;
	serveradd.sin_port = htons(11235);

	if (gethostbyname(argv[1]) == NULL)
	{
		printf("get host error\n");
		exit(0);
	}

	serveradd.sin_addr = *(struct in_addr *)gethostbyname(argv[1])->h_addr_list[0];

	if (connect(socketfd, (struct sockaddr *)&serveradd, sizeof(serveradd)) == -1) // connect server
	{
		printf("connect error\n");
		exit(0);
	}

	if ((num = write(socketfd)) == 0) // receive details
	{
		printf("receive error\n");
		exit(0);
	}
	else
		printf("Received: %d bytes\n", num);

	shutdown(socketfd, SHUT_RD); // close connect

	return 0;
}

int write(int socketfd)
{
	FILE *f;
	int num = 0, receive = 0;
	char buf;
	f = fopen("./receive", "a");
	while((receive = recv(socketfd, &buf, 1, 0)) > 0)
	{
		fwrite(&buf, sizeof(char), 1, f);
		num += receive;
	}
	fclose(f);
	return num;
}