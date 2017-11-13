import sys, socket, re

# if (len(sys.argv) < 3):
#     print("Server usage: python Server.py [IP] [PORT]")
#     sys.exit(0)

host, port, student_id = '127.0.0.1', 5555, 17304249  # sys.argv[1], int(sys.argv[2]), int(sys.argv[3])

# host, port = sys.argv[1], int(sys.argv[2])
# student_id = 17304249

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
        for client in self.clients:
            client.stop()
        print("Server is killed")
        exit()


class ChatRoom:
    def __init__(self):
        self.client_names = []
        self.chat_rooms = []
        self.client_sockets = []

    def getClientID(self,client_name):
        # try:
        #     self.client_names.index(client_name)
        # if(self.client_names[self.client_names.index(client_name)]):
        if client_name in self.client_names:
            return self.client_names[self.client_names.index(client_name)]
        else:
            self.client_names.append(client_name)
            client_id = self.client_names.index(client_name) + 1

            return client_id


        # except :
        #     client_id = self.id + 1
        #     self.client_names[self.client_names.index(client_name)] = client_id
        #     return client_id;
        # else:
        #     return self.client_names[self.client_names.index(client_name)]

    def addClientToChatroom(self, chatroom, client_id):
        found = False
        room_ref = None
        for rr,value in self.chat_rooms:
            if value == chatroom:
                found = True
                room_ref = rr
                client_id.append(self.chat_rooms[rr]["values"])
                break
        if(found == False):
            self.chat_rooms.append({"name" : chatroom, "values" : client_id})
            room_ref = self.chat_rooms.index({"name" : chatroom,"values" : client_id}) + 1

        return room_ref


    def removeClientFromChatroom(self, client_id, room_ref):
        pass

    def getClientChatrooms(self, client_id):
        pass

    def sendMessageToChatroom(self, room_ref, client_name, message):

        if client_name in self.client_names:
            client_ids = [self.chat_rooms[room_ref - 1]["values"]]
            message_mar = "CHAT:" + str(room_ref) + "\nCLIENT_NAME:" + client_name + "\nMESSAGE:" + message.strip() + "\n\n"
            for client_id in client_ids:
                self.sendMessageToClient(client_id, message_mar)
        # try:
        #     self.client_names[client_name]
        # except NameError:
        #     return
        # else:
        #     client_ids = self.chat_rooms[room_ref]["values"]
        #     message_mar = "CHAT:" + room_ref + "\nCLIENT_NAME:" + client_name + "\nMESSAGE:" + message.strip() + "\n\n"
        #     for client_id in client_ids:
        #         self.sendMessageToClient(client_id,message_mar)

    def sendMessageToClient(self, client_id, message):
        socket = self.getClientSocket(client_id)
        socket.send(message.encode())

    def storeClientSocket(self, client_id, socket):
        self.client_sockets.append(socket)

    def deleteClientSocket(self, client_id):
        pass

    def getClientSocket(self, client_id):
        try:
            self.client_sockets[client_id - 1]
        except NameError:
            return None
        else:
            return self.client_sockets[client_id - 1]

class Client:
    def __init__(self, socket, host, port, studentid, chat_room, server):
        self.client = socket
        self.host = host
        self.port = port
        self.studentid = studentid
        self.chat_room = chat_room
        self.server = server

    def stop(self):
        self.flag = False

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
                    self.client.send(message.encode())
                    print(message, '\n')
                    return True
                elif result[0:12] == "KILL_SERVICE":
                    self.server.killServer()
                    return False
                else:
                    self.handleClient(result, self.client, self.host, self.port)

    def closeSocket(self):
        self.client.setblocking(self.client)
        self.client.close(self.client)
        self.client = None
        return False

    def handleClient(self, result, socket, hostip, port):
        return self.joinChatroom(result, socket, hostip, port) or \
               self.leaveChatroom(result, socket) or \
               self.disconnect(result, socket) or \
               self.chat(result, socket) or \
               self.noMatch(result, socket)

    def noMatch(self, result, socket):
        print('Unknow message:', result, 'unable to process, so terminating self client')
        return False

    def joinChatroom(self, result, socket, hostip, port):
        if result[0:len("JOIN_CHATROOM")] == "JOIN_CHATROOM":
            print("JOIN_CHATROOM:")
            line = result.split(':')
            chatroom = re.sub('\nCLIENT_IP', ' ', line[1]).strip()
            client_ip = re.sub("\nPORT", "", line[2]).strip()
            ipport = re.sub("\nCLIENT_NAME","",line[3]).strip()
            client_name = line[4].strip()
            # print(chatroom,"@",client_ip,"@",ipport,"@",client_name, "!!!!!!!!!!!!!!!!!!!")

            client_id = self.chat_room.getClientID(client_name)
            room_ref = self.chat_room.addClientToChatroom(chatroom, client_id)
            self.chat_room.storeClientSocket(client_id, socket)
            message = "JOINED_CHATROOM:" + str(chatroom) + "\nSERVER_IP:" + hostip + "\nPORT:" + str(port) + "\nROOM_REF:" + str(room_ref) + "\nJOIN_ID: " + str(client_id) + "\n"
            self.client.send(message.encode())
            print("sent to client:\n",message)
            message = client_name+"has joined this chatroom."
            self.chat_room.sendMessageToChatroom(room_ref, client_name, message)
            return True
        else: return False


    def leaveChatroom(self, result, socket):
        pass

    def disconnect(self, result, socket):
        pass

    def chat(self, result, socket):
        pass


chat_room = ChatRoom()
server = Server(host, port, student_id, chat_room)
server.run()