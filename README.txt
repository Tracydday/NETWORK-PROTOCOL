Beacuse we use the python, so we donot need write a makefile.
The program runs under linux environment.

You should run server.py at first by running script"./server.sh" Then you can get some information
which are serveraddress, a random udp port number and a random tcp port number
Next run the client.py by typing "./client.sh" add the severAddr and udp port number which are provided by the server and also type the get or put command with the two filename. 
Such as:
	run "./server.sh"
	you can get "
	Server Address: ubuntu1404-008
	Server Udp Portnumber: 45610
	Server Tcp Portnumber: 44971"
	Then the  serverAddr which is ubuntu1404-010 and server udp prot number is 45610
	Next run the client: "./client.sh ubuntu1404-010  45610 get remote_filename local_filename"
	Then we can get the list of the file ows by server by the udp.
	Addition, achieving get and put command by using TCP connection to transfer file.