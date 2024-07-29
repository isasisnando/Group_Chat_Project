from socket import *
from Grupo import Grupo
import threading
mensagemNotFoundUser = "canal com o usuario nao encontrado"
mensagemNotFoundGrupo = "voce nao esta no grupo"
mensagemUnauthorized = "Você não está autorizado a fazer isso"
mensagemGroupNameUsed = "Nome de Grupo já existe"
mensagemOutGrupo = "5@"

class Usuario:

    users = list()
    groups = list()
    usersChannel = dict() # dict<email, msgs>
    groupsChannel = dict() # dict<nome, msgs>

    # seria interessante ter outra lista com outros usuarios
    # os quais ele já iniciou uma conversa? Acho q essa lista é
    # algo já implementado naquele exemplo de IRC, link:
    # https://github.com/Gabrielcarvfer/Redes-de-Computadores-UnB/blob/master/trabalhos/20181/Lab2/ExemploIRC.py

    def __init__(self, name, email, passw, cep, ipv4, sockUser, server) -> None:

        self.name, self.email, self.passw, self.cep, self.ipv4 = name, email, passw, cep, ipv4
        self.serv = server

        # Sockets definitions are already done in the server

        self.conected = ""
        self.tipoConec = -1
        self.sockUser = sockUser 
    
    def receiveMsgUser(self, message, whoSent):

        # Devolvemos essa mensagem pro nosso usuario

        self.usersChannel[whoSent].append(message)
        # tipo conec = 1 - > Usuario
        if (self.tipoConec == 1 and self.conected == whoSent):
            self.sockUser.send(message.encode("utf-32"))
    
    def receiveMsgGrupo(self, message, whoSent):

        # vc está garantidamente no grupo
        # Devolvemos essa mensagem pro nosso usuario
        self.groupsChannel[whoSent].append(message)
        # tipo conec = 2 - > grupo
        if (self.tipoConec == 2 and self.conected == whoSent):
            self.sockUser.send(message.encode("utf-32"))
    
    def sendMsgToUser(self, message, dest):

        # procuramos se estamos mandando msg pra algum usuario
        # com algum canal

        for user in self.users.keys():

            if(dest == user.getName()):
                
                self.usersChannel[user.getEmail()].append(message)
                return list(message, user)
    
    def sendMsgToGroup(self, message, dest):

        # procuramos se estamos mandando mensagem para algum grupo
        # com algum canal já existente
        for grupo in self.grupos.keys():

            if(dest == grupo.getName()):

                self.groupsChannel[grupo.getName()].append(message)
                return list(message, grupo)
    
    def start(self):

       while True:
           
            mensagem = self.sockUser.recv(1024).decode("utf-32")

            if (mensagem == ""):
                continue
           
            """
                0 -> open connection
                1 -> close
                2 -> message for group/direct
                3 -> logout
                4 -> quer adicionar um novo usuario
                5 -> manda convite
                6 -> pede pra entrar
                7 -> entra
                8 -> cria grupo
                9 -> sai Grupo
                11 -> pede Users
                10 -> pede Groups
                12 -> Historico de mensagens do grupo
                0|tipo|email ou nome
                1|
                2|groupName|userName|message
                4|emailDoNewUser
                5|grupo|email
                6|grupo|email
                7|grupo|email
                8|grupo|email
                9|NomeGrupo|email
                12|groupName|userName
           """

            message = mensagem.split("|")

            match message[0]:
            
                case ('1'):
                    self.conected = ""
                    self.tipoConec = -1
                case ('0'):
                    try:

                        mensagemGrl = ""
                        if (int(message[1]) == 1):
                            for msg in self.usersChannel[message[2]]:
                                mensagemGrl += f"{msg}|"
                        else:
                            for msg in self.groupssChannel[message[2]]:
                                mensagemGrl += f"{msg}|"
                        
                        self.sockUser.send(mensagemGrl.encode("utf-32"))
                        
                        self.conected = message[2]
                        self.tipoConec = int(message[1])
                    except: 
                        pass
                case ('2'):
                    print(message)
                    try: 
                        group = self.serv.groups[message[1]]
                        userMessage = f"{message[2]} : {message[3]}"
                        group.messages.append(userMessage)
                        group.propagateMessage(userMessage)
                    except:
                        print("ERRO")
                    
                case ('3'):
                    break
                case ('4'):
    
                    # Adiciona um novo usuario para o usuario atual
                    # precisa de threading aqui? acho q já começa a ficar muito muito
                    t = threading.Thread(target= self.addUser, args=(self.serv.users[message[1]]))
                    t1 = threading.Thread(target= self.serv.users[message[1]].addUser, args=(self))
                    t1.start()
                    t.start()
                case('5'):
                    if (self.name != self.serv.groups[message[1]].getAdmin()):
                        self.sockUser.send(mensagemUnauthorized.encode("utf-32"))
                        continue

                    # O usuario devera receber o grupo que foi convidado
                    t = threading.Thread(target= self.serv.users[message[2]].rcvInvite, args=(message[1]))
                    t.start()
                    
                case('6'):

                    t = threading.Thread(target= (self.serv.groups[message[1]].getAdmin()).pedidoParaEntrar, args=(message[2]))
                    t.start()

                case('7'):

                    self.serv.groups[message[1]].addUser(self)
                    self.serv.users[message[2]].addGroup(self.findGroup(message[1]))
                
                case('8'):

                    if (message[1] in self.serv.groups.keys()):
                        self.sockUser.send(mensagemGroupNameUsed.encode("utf-32"))
                        continue

                    newGrupo = Grupo(message[1], self.serv.users[message[2]])

                    self.serv.groups[message[1]] = newGrupo
                    self.groups.append(self.serv.groups[message[1]])
                    # t = threading.Thread(target= self.serv.users[message[2]].addGroup, args=(newGrupo))
                    # t.start()                
                case('9'):
                    t = threading.Thread(target= self.serv.groups[message[1]].eraseUser, args=(self.serv.users[message[2]]))
                    t1 = threading.Thread(target= self.serv.users[message[2]].sairDeUmGrupo, args=(self.serv.groups[message[1]]))
                    t1.start()
                    t.start()
                case('10'):
                    groupsGrl = ""
                    for grupo in self.serv.groups.keys():
                        groupsGrl += f"{grupo}|"
                    
                    self.sockUser.send(groupsGrl.encode("utf-32"))
                case('11'):
                    usersGrl = ""
                    for user in self.serv.users.keys():
                        usersGrl += f"{user}|"
                    
                    self.sockUser.send(usersGrl.encode("utf-32"))
                case('12'):
                    print(message)
                    group = self.findGroup(message[1])
                    group.propagateMessage(f"{message[2]} joined this chat\n")
                    groupMessages = ""
                    print(group)
                    for message in group.messages:
                        groupMessages += f"{message}|"
                    print(groupMessages)
                    self.sockUser.send(groupMessages.encode("utf-32"))

    def serverRcv(self, mensagem):
        
        # 1@emerson@lucas@...
        # 1, 2, 3, 4, 5, 6, 7- > identifica se é mensagem para um usuario ou grupo
        # ou um convite para um grupo ou pedido para entrar em um grupo ou
        # sair de um grupo ou usuario adicionado
        # orig - > quem está mandando
        # dest - > quem tem q receber
        # 7@grupo

        mensagemSplitada = mensagem.split('@')

        if(mensagemSplitada[0] == '2'):

            content, dest = self.sendMsgToGroup(mensagem, mensagemSplitada[2])

            dest.rcvAndPropMsg(content)
            
            return

        content, dest = self.sendMsgToUser(mensagem, mensagemSplitada[2])
        
        dest.receiveMsgUser(content, self.getEmail())

    # The main idea in this two methods is to
    # make the process of creating new chanels more
    # easy

    def addUser(self, userStuff):   # esse userStuff é um objeto Usuario

        self.users.append(userStuff)

        mensagem = "6@" + userStuff.getName() + "@" + userStuff.getEmail() + '@'

        self.usersChannel[userStuff.getEmail()] = list()
        self.sockUser.send(mensagem.encode("utf-32"))

        return
    
    def rcvInvite(self, group):

        # 3 implica um convite

        mensagem = "3@"
        mensagem += group + '@'

        self.sockUser.send(mensagem.encode("utf-32"))
    
    def pedidoParaEntrar(self, whoWantsIn): # A gente passa ao admin quem pediu pra entrar
        
        message = "4@"

        message += whoWantsIn + '@'

        self.sockUser.send(message.encode("utf-32"))
    
    def sairDeUmGrupo(self, grupo):

        self.grupos.pop(grupo)

        # se a gente tivesse mais grupos usar um dict seria melhor
        # para a complexidade

        mensagem = mensagemOutGrupo + grupo.getName() + '@'

        self.sockUser.send(mensagem.encode("utf-32"))

    
    def addGroup(self, groupStuff): # esse groupStuff é um objeto Grupo

        self.groupsChannel[groupStuff.getName()] = list()
        self.groups.append(groupStuff)
        return

    def findGroup(self, groupName):
        for group in self.serv.groups.values():
            if group.name == groupName:
                print("gn"+ groupName)
                return group
    
    def getName(self):
        return self.name
    
    def getEmail(self):
        return self.email
    
    def getPassw(self):
        return self.passw
    
    def getCep(self):
        return self.cep

# Acho q vamos precisar de uma classe pra gerar os usuarios e os grupos
# no server side