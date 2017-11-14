import socket


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sock.connect(('127.0.0.1',5555))

# sock.send(b'HELO test\n')
# sock.send(b'KILL_SERVICE\n')


# sock.send(b'ssssssss\n')

# sock.send(b'JOIN_CHATROOM: cccccroom 1\n'+
# 		  b'CLIENT_IP: 127.0.0.1\n'+
# 		  b'PORT: 5555\n'+
# 		  b'CLIENT_NAME: Client 1\n')

#
sock.send(b'LEAVE_CHATROOM:: chatroom 1\n'+
		  b'JOIN_ID: \n'+
		  b'CLIENT_NAME: \n')

#
#
# sock.send(b'CHAT: chatroom 1\n'+
# 		  b'JOIN_IDJOIN_ID:\n'+
# 		  b'CLIENT_NAME: \n'+
# 		  b'MESSAGE:\n')
#



print(sock.recv(1024).decode())

