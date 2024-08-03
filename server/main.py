import socket 
from Usuario import Usuario
from Grupo import Grupo
import threading


HOST = "127.0.0.1"
PORT = 3300

mensagemExistsUserEmail = "Já existe usuario com esse email"
okMessage = "OK"

class Server: 
    def __init__(self):
        
        self.usersLogin = dict() # dict<email, senha>
        self.users = dict() # dict<name, user>
        self.groups = dict() # dict<nome, group>

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((HOST, PORT))
        self.socket.listen()

    def login(self, message, client, address):

        if message[1] in self.usersLogin.keys():
            if (message[2] == self.usersLogin[message[1]]):

                user = self.users[message[1]]
                user.ipv4 = address
                user.sockUser = client
                
                mensagem = "login Done : " + user.getName() + " : " + user.getCep() + " : "

                client.send(mensagem.encode("utf-32"))

                t = threading.Thread(target= user.start, args=())
                t.start()
                return
        
        mensagem = "login Not Done : "
        client.send(mensagem.encode("utf-32"))

    def sign_up(self, message, client, address):
        user = Usuario(message[2], message[1], message[3], message[4], address, client, self)
        self.users[user.getName()] = user
        self.usersLogin[user.getEmail()] = user.getPassw()
        t = threading.Thread(target= user.start, args=())
        t.start()

    def receive(self):

        while True:

            client, address = self.socket.accept()
            """
                0 -> signup
                1 -> login
    
                0|email|name|password|cep
                1|email|password

            """
            message = client.recv(1024).decode("utf-32")

            message = message.split("|")

            match message[0]:
            
                case ('1'):

                    self.login(message, client, address)
                case ('0'):

                    if (message[1] in self.users.keys()):

                        client.send(mensagemExistsUserEmail.encode("utf-32"))
                        continue
                    client.send(okMessage.encode("utf-32"))
                    self.sign_up(message, client, address)


    def start(self):
        self.receive()

Server().start()