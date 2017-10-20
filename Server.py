import sys, socket, re

# if (len(sys.argv) < 3):
#     print("Server usage: python Server.py [IP] [PORT]")
#     sys.exit(0)

host, port, student_id = '127.0.0.1', 5555, 17304249  # sys.argv[1], int(sys.argv[2]), int(sys.argv[3])

# host, port = sys.argv[1], int(sys.argv[2])
student_id = 17304249

class Server:
    def __init__(self, host, port, student_id, chat_room):
        self.host = host
        self.port = port
        self.studend_id = student_id
        self.chat_room = chat_room
        self.clients = []
        self.flag = True
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.host, self.port))

    def run(self):
        self.socket.listen(5)
        self.socket.setblocking(1)
        print("Server is listening to :", host)
        while self.flag:
            client, p = self.socket.accept()
            self.clients.append(Client(client, self.host, self.port, self.studend_id, self.chat_room, self))
            closed = []
            for c in self.clients:
                if c.processSocket() == False:
                    closed.append(c)

    def killServer(self):
        if (self.flag == False):
            return
        self.flag = False
        print("Server is killed")
        exit()


class Chatroom:
    def __init__(self):
        self.client_names = []
        self.chat_rooms = []
        self.client_sockets = []



class Client:
    def __init__(self, socket, host, port, studentid, chat_room, server):
        self.client = socket
        self.host = host
        self.port = port
        self.studentid = studentid
        self.chat_room = chat_room
        self.server = server

    def processSocket(self):
        if self.client:
            result = self.client.recv(1024).decode()
            if result == False:
                return self.closeSocket()
            else:
                print('Recieved from client:\n', result)
                if result[0:5] == "HELO ":
                    message = result + "IP:" + self.host + "\nPort:" + str(self.port) + "\nStudentID:" + str(
                        self.studentid)
                    # print(message, "!!!!!!!!!!!!!!!!!!!")
                    self.client.send(message.encode())
                    print(message, '\n')
                    return True
                elif result[0:12] == "KILL_SERVICE":
                    self.server.killServer()
                    return False
                else:
                    pass

    def closeSocket(self):
        self.client.setblocking(self.client)
        self.client.close(self.client)
        self.client = None
        return False


chat_room = Chatroom()
server = Server(host, port, student_id, chat_room)
server.run()
