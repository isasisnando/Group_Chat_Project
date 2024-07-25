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

        self.users = dict()  #dict<email, User>
        self.activeUser = dict()   #dict<ip, User>
        self.groups = dict() # dict<name, Group>

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((HOST, PORT))
        self.socket.listen()

    def login(self, message, client, address):

        if message[1] in self.users:
            if (message[2] == self.users[message[1]].getPassw()):

                user = self.users[message[1]]
                user.ipv4 = address
                user.sockUser = client
                self.activeUser[str(address)] = user

                mensagem = "login Done : " + user.getName() + " : " + user.getCep() + " : "

                client.send(mensagem.encode("utf-32"))
                return
        
        mensagem = "login Not Done : "
        client.send(mensagem.encode("utf-32"))

    def sign_up(self, message, client, address):

        user = Usuario(message[2], message[1], message[3], message[4], address, client)
        self.users.append(user)
        self.activeUser[str(address)] = user
    
    def logout(self, address):
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

                        client.send(mensagemExistsUserEmail)
                        continue

                    t = threading.Thread(target= self.sign_up, args=(message))
                    t.start()
                case ('2'):

                    ip = str(address) 
                    user = None
                    if (ip in self.activeUser.keys()):

                        user =  self.activeUser[ip]
                        t = threading.Thread(target= user.serverRcv, args=(message[1]))
                        t.start()
                case ('3'):
                    t = threading.Thread(target= self.logout, args=(address))
                    t.start()
                case ('4'):
                    if (message[1] not in self.users.keys()):
                        client.send(mensagemNaoEncontrouUser.encode("utf-32"))
                        continue
                    # Adiciona um novo usuario para o usuario atual
                    t = threading.Thread(target= self.activeUser[str(address)].addUser, args=(self.users[message[1]]))
                    t1 = threading.Thread(target= self.users[message[1]].addUser, args=(self.activeUser[str(address)]))
                    t1.start()
                    t.start()
                case('5'):
                    if (self.activeUser[str(address)].getName() != self.groups[message[1]].getAdmin()):
                        client.send(mensagemUnauthorized.encode("utf-32"))
                        continue

                    # O usuario devera receber o grupo que foi convidado
                    t = threading.Thread(target= self.user[message[2]].rcvInvite, args=(message[1]))
                    t.start()
                    
                case('6'):

                    t = threading.Thread(target= (self.groups[message[1]].getAdmin()).pedidoParaEntrar, args=(message[2]))
                    t.start()

                case('7'):

                    t = threading.Thread(target= self.groups[message[1]].addUser, args=(self.users[message[2]]))
                    t1 = threading.Thread(target= self.users[message[2]].addGroup, args=(self.groups[message[1]]))
                    t1.start()
                    t.start()
                
                case('8'):

                    if (message[1] in self.groups.keys()):
                        client.send(mensagemGroupNameUsed.encode("utf-32"))
                        continue

                    newGrupo = Grupo(message[1], self.users[message[2]])

                    self.groups[message[1]] = newGrupo

                    t = threading.Thread(target= self.users[message[2]].addGroup, args=(newGrupo))
                    t.start()
                
                case('9'):

                    t = threading.Thread(target= self.groups[message[1]].eraseUser, args=(self.users[message[2]]))
                    t1 = threading.Thread(target= self.users[message[2]].sairDeUmGrupo, args=(self.groups[message[1]]))
                    t1.start()
                    t.start()

    def start(self):
        self.receive()

Server().start()