import socket
import sys
import os.path



tPort = 65534

read = sys.argv
read = read[1:] # donot need client.py
serverAddr = read[0] # get serverAddr 
uPort  = int(read[1]) # get udp port number
read = read[2:] # get res



def udpconnect():
	#create a udp connection with server
	clientudp = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

	# get the message from client
	message = ' '.join(read) 

	if not message:
		print "error: client does not type in request "
		# the client want to get the list of file in the server.
	alllist = "list"

	#print "send to client message is ",message
	clientudp.sendto(alllist,(serverAddr,uPort)) #send message to server
	# get recieve from server
	while 1:
		data,addr = clientudp.recvfrom(1024)

		global tPort 
		whole = data.split("\n")
		tPort = int(whole[0])
		print "The random tcp port number get from server: ", tPort
		dataprint = ' '.join(whole[len(str(tPort)):])
		
		print "Server has the list of file: " + dataprint
		break
	# split the string of message into a request list
	request = message.split()
	if request[0] == 'put':
		
		if(len(request) != 3):
			sendmsg = "error not enough parameters or too much"
			clientudp.sendto(sendmsg,(serverAddr,uPort))
			sys.exit(sendmsg)
		print "send to server request:", message
		#check the local file is in the folder
		if(os.path.isfile(request[1]) == 1):
			sendmsg = request[0] + " " + request[2]
		else:
			sendmsg = "error no such file"
			clientudp.sendto(sendmsg,(serverAddr,uPort))
			sys.exit(sendmsg)
		# use the UDP to send the put request to server

		print "waiting TCP connection to send file"
		clientudp.sendto(sendmsg,(serverAddr,uPort))
		# call putclient function by using TCP to transfer file
		putclient(request[1],request[2])
	if request[0] == 'get':
		if(len(request) != 3):
			sendmsg = "error not enough parameters"
			clientudp.sendto(sendmsg,(serverAddr,uPort))
			sys.exit(sendmsg)
		print "send to server request:", message
		#send the message to server get remote_filename
		sendmsg = request[0] + " " + request[1] 
		# use the UDP to send the get request to server
		clientudp.sendto(sendmsg,(serverAddr,uPort))
		#global tPort,udpadd = clientudp.recvfrom(1024)
		getclient(request[1],request[2])
	##closeserver = ""
	#clientudp.sendto(closeserver,(serverAddr,uPort)) 


def putclient(local_filename,remote_filename):
	#create a TCP socket
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	try:
		#Connect the socket to the server
		s.connect((serverAddr,tPort))
		tcpaddress = (serverAddr,tPort)
		print "get connection with server address %s port %s" %tcpaddress 
		#send the request message
		msg = "put" + " "  + remote_filename
		s.send(msg)
		print "send a put request to the server by TCP "
		#get a repley from server
		repley = s.recv(1024)
		if(repley == "error cannot create a local file."):
			print "error cannot create a local file."
			sys.exit()
		print "get a repley from server: ", repley # get ok or server open file failed

		# open the file, tell server ok or not
		try:
			fr = open(local_filename, 'r')
		except:
			s.send("error cannot create a local file.")
			sys.exit("error cannot create a local file.")
		else:
			print"file is open"
			s.send("file is open")

		#send file name and 
		file = fr.read(1024)
		while file:
			s.send(file)
			file = fr.read(1024)
		fr.close()
		s.close()
	except Exception, e:
		print "error %s " %str(e)
		sys.exit()
	else:
		print "finish sending file to server"

def getclient(remote_filename,local_filename):
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	#Connect the socket to the server
	s.connect((serverAddr,tPort))
	tcpaddress = (serverAddr,tPort)
	print "get connection with server address %s port %s" % tcpaddress
	try:
		
		#send the request message
		msg = "get" + " "  + remote_filename
		s.send(msg)
		print "Get a connection with server by TCP "
		# get repley from server open file good or not
		repley = s.recv(1024)
		R = repley.split()
		if R[0] == "error":
			print(repley)
			sys.exit()
		print "get a repley from server: ", repley

		# open the file
		try:
			fr = open(local_filename, 'w')
		except:
			s.send("error cannot create a local file.")
			sys.exit("error cannot create a local file.")
		else:
			print"file is open"
			s.send("file is open")
		#send file name and 
		file = s.recv(1024)
		while file:
			# write the date into the local file
			fr.write(file)
			# get data from server
			file = s.recv(1024)
		fr.close()
		s.close()
	except Exception, e:
		print "error %s " %str(e)
		sys.exit()
	else:
		print "get file from server successfu!!"


udpconnect()

