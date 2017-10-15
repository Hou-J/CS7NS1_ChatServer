import sys, socket

if (len(sys.argv) < 3):
    print("Server usage: python Server.py [IP] [PORT]")
    sys.exit(0)

host, port, student_id = sys.argv[1], int(sys.argv[2]), 17304249

class Server:
    def __init__(self, host, port, student_id, ):
        self.host = host
        self.port = port
        self.studend_id = student_id
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.host, self.port))

    def run(self):
        self.socket.listen(5)
        self.socket.setblocking(1)
        print("Server is listening to :", host)
        print(self.socket.recv(1024).decode())

    def heloServer(self):
        pass

    def killServer(self):
        pass

class Chatroom:
    pass

class Client:
    pass