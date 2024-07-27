import socket 
from Usuario import Usuario
from Grupo import Grupo
import threading


HOST = "127.0.0.1"
PORT = 3300
mensagemNaoEncontrouUser = "Usuario nao esta no servidor"
mensagemUnauthorized = "Você não está autorizado a fazer isso"
mensagemGroupNameUsed = "Nome de Grupo já existe"
mensagemExistsUserEmail = "Já existe usuario com esse email"

class Server: 
    def __init__(self):

        self.users = dict() # dict<email, user>
        self.groups = list()

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((HOST, PORT))
        self.socket.listen()

    def login(self, message, client, address):

        if message[1] in self.users.keys():
            if (message[2] == self.users[message[1]].getPassw()):

                user = self.users[message[1]]
                user.ipv4 = address
                user.sockUser = client
                

                mensagem = "login Done : " + user.getName() + " : " + user.getCep() + " : "

                client.send(mensagem.encode("utf-32"))

                t = threading.Thread(target= self.user.start(), args=())
                t.start()
                return
        
        mensagem = "login Not Done : "
        client.send(mensagem.encode("utf-32"))

    def sign_up(self, message, client, address):

        user = Usuario(message[2], message[1], message[3], message[4], address, client)
        t = threading.Thread(target= self.user.start(), args=())
        t.start()
        self.users[user.getEmail()] = user

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
                6 -> pede pra entrar
                7 -> entra
                8 -> cria grupo
                9 -> sai Grupo
                0|email|name|password|cep
                1|email|password
                4!emailDoNewUser
                5|grupo|email
                6|grupo|email
                7|grupo|email
                8|grupo|email
                9|NomeGrupo|email
                
                Acredito q seria interessante deixar a resposta de um convite ou pedido
                privadas

                Futuramente com o lado do cliente implementado e quando formos olhar as coisas
                da transmissão de audio e video mais coisas devem ser adicionadas, mas
                o corpo acho q é isso

            """
            message = client.recv(1024).decode("utf-32")

            message = message.split("|")

            match message[0]:
            
                case ('1'):

                    t = threading.Thread(target= self.login, args=(message, client, address))
                    t.start()
                case ('0'):

                    if (message[1] in self.users.keys()):

                        client.send(mensagemExistsUserEmail.encode("utf-32"))
                        continue

                    t = threading.Thread(target= self.sign_up, args=(message, client, address))
                    t.start()

    def start(self):
        self.receive()

Server().start()