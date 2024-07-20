import socket 
import Usuario

PORT = 3300
mensagemNaoEncontrouUser = "Usuario nao esta no servidor"

class Server: 
    def __init__(self):

        self.users = dict()  #dict<email, User>
        self.activeUser = dict()   #dict<ip, User>
        self.groups = list()

        self.socket = socket.socket((socket.AF_INET, socket.SOCK_STREAM))
        self.socket.bind((socket.gethostbyname(), PORT))
        self.socket.listen()

    def login(self, message, client, address):

        if message[1] in self.users:

            if (message[2] == self.users[message[1]].getPassw()):

                user = self.users[message[1]]
                user.ipv4 = address
                user.sockUser = client
                self.activeUser[str(address)] = user

    def sign_up(self, message, client, address):

        user = Usuario(message[2], message[1], message[3], message[4], address, client)
        self.users.append(user)
        self.activeUser[str(address)] = user
    
    def logout(self, client, address):
        del self.activeUser[str(address)]

    def receive(self):

        while True:

            client, address = self.socket.accept()
            """
                0 -> signup
                1 -> login
                2 -> message for group/direct
                3 -> logout
                4 -> quer adicionar um novo usuario
                5 -> manda convite
                6 -> aceita ou nao
                7 -> pede pra entrar
                8 -> aceita pedido ou nao
                0|email|name|password|cep
                1|email|password
                4!emailDoNewUser
                
            """
            message = client.recv(1024).decode("utf-32")

            message = message.split("|")

            if (message[0] == '1'):
                isValid = self.login(message)
            elif (message[0]=='0'):
                self.sign_up(message)
            elif (message[0] == '2'):
                ip = str(address) 
                user = None
                if (ip in self.activeUser.keys()):
                   user =  self.activeUser[ip]
                user.serverRcv(message[1])
            elif (message[0] == '3'):
                self.logout(client, address)
            elif (message[0] == '4'):

                if (message[1] not in self.users.keys()):
                    client.send(mensagemNaoEncontrouUser.encode("utf-32"))
                    continue

                # Adiciona um novo usuario para o usuario atual
                self.activeUser[str(address)].addUser(self.users[message[1]])

    def sendInvite(self):
        pass

    def acceptInvite(self):
        pass

    def askIn(self):
        pass

    def acceptIn(self):
        pass

    def start(self):
        self.receive()


