import socket # import socket 
import sys
import os
import os.path


serverAddr = "ubuntu1404-010"
uPort = 12345
tPort = 65534
tcpsocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)



# udp connection by server
def udp():
	# create a udp scoket
	#print "Waiting for server set udp connection with client....."
	serversocket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
	serversocket.bind(('',0)) #Bind udp socket, to get a random udp port number
	global uPort
	uPort = serversocket.getsockname()[1]
	global tcpsocket
	tcpsocket.bind(('',0)) # bind to get a random tcp port number
	global tPort
	tPort = tcpsocket.getsockname()[1]
	global serverAddr
	serverAddr = socket.gethostname()
	#print server udp connection info
	print "Server Address: %s" %serverAddr
	print "Server Udp Portnumber: %s" %uPort
	print "Server Tcp Portnumber: %s" %tPort
	print 'UDP Socket created by server' 
	
	#create a ramdom tcp port number


	while 1:
		data, addr = serversocket.recvfrom(1024) # buffer size is 1024
		
		request = data.split() # split data to a list 
		if(request[0] == "list"):
			print "received message from client: ", request[0]
			filename = os.listdir("./home_folder") # find the file name in the home directory
			filelist = " ".join(filename) 
			# send the list of file which server owned and also the tcp port number
			serversocket.sendto((str(tPort) + '\n' + filelist),addr) # send the list of file to client.
		if(request[0] == "put"):
			print "received message from client by udp:", data
			#print "Waiting for seting Tcp Connection between server and client ...."
			#serversocket.sendto(tPort,addr) # send random tcp port number
			tcp_put(request[1])
			break
		if(request[0] == "get"):
			print "received message from client by udp:", data
			#print "Waiting for seting Tcp Connection between server and client ...."
			#serversocket.sendto(tPort,addr) # send random tcp port number
			tcp_get(request[1])
			break
		if(request[0] == "error"):
			sys.exit(data)
	
			

def tcp_put(filename):
	global tcpsocket
	print "Finish tcp init, begin to listening"
	tcpsocket.listen(1)
	print "starting listening"
	# tcp socket is redeay to get request from client
	client_soc, client_add = tcpsocket.accept()
	print "Socket has the connection whith client: ", client_add
	try:
		
		request = client_soc.recv(1024)
		data = request.split()
		#reciver a error from client
		if(data[0] == "error"):
			sys.exit(request)
		print "client need to:", request

		try:

			file = open('./home_folder' + filename, 'w')
		except:
			client_soc.send("error cannot create a local file.")
			sys.exit("error cannot create a local file.")
		else:
			print"file is open"
			client_soc.send("OK.")
		# check client open file success or fail
		checkclientfile = client_soc.recv(1024)
		if checkclientfile == "error cannot create a local file.":
			sys.exit("error cannot create a local file.")

		file_data = client_soc.recv(1024)
		while file_data:
			file.write(file_data)
			file_data = client_soc.recv(1024)
		file.close()
		tcpsocket.close()

	except Exception, e:
		print "error %s " %str(e)
		sys.exit()
	else:
		print "Finish getting file from client"

def tcp_get(filename):
	global tcpsocket
	print "Finish tcp init, begin to listening"
	tcpsocket.listen(1)
	print "starting listening"
	# tcp socket is redeay to get request from client
	client_soc, client_add = tcpsocket.accept()
	# create a file in the homefoldr
	print "receive a get reqeust form client, starting to send file to client"
	try:
		request = client_soc.recv(1024)
		data = request.split()
		#reciver a error from client
		if(data[0] == "error"):
			sys.exit(request)
		print "client need to:", request
		#check whether file in the local and open file ok or not
		if(os.path.isfile('./home_folder' +filename) == 1):
			try:
				file = open('./home_folder' +filename, 'r')
			except:
				client_soc.send("error cannot open a local file in server.")
				sys.exit("error cannot open a local file in server.")
			else:
				print "open %s and send it to client" %filename
				client_soc.send("OK.")
			# check client open file success or fail
			checkclientfile = client_soc.recv(1024)
			if checkclientfile == "error cannot create a local file.":
				sys.exit("error cannot create a local file.")

			file_data = file.read(1024)
			while file_data:
				client_soc.send(file_data)
				file_data = file.read(1024)
			file.close()
			tcpsocket.close()
		else:
			errormsg = "error %s does not exist." %filename
			client_soc.send(errormsg)
			sys.exit(errormsg)
	except Exception, e:
		print "error %s " %str(e)
		sys.exit()
	else:
		print "finish sending file from server to client"



print "Waiting for server set udp connection with client....."
udp()


	
	
