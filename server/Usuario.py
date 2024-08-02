from socket import *
import os 
from Grupo import Grupo
import threading
mensagemNotFoundUser = "canal com o usuario nao encontrado"
mensagemNotFoundGrupo = "voce nao esta no grupo"
mensagemUnauthorized = "Você não está autorizado a fazer isso"
mensagemGroupNameUsed = "Nome de Grupo já existe"
mensagemOutGrupo = "5@"

CONNECTION_TYPE = {
    "GROUP": "GROUP",
    "CHANNEL": "CHANNEL",
    "NONE": None,
}


class Usuario:

    users = list()
    groupsAsked = set()
    groups = list()
    usersChannel = dict() # dict<name, msgs>
    notifs = list() # isso aqui vai funcionar como uma pilha de notificacoes
    #  toda vez q entrar a gente manda essas notificacoes
    # tem q marcar tbm os grupos q ja pediu pra entrar

    def __init__(self, name, email, passw, cep, ipv4, sockUser, server) -> None:

        self.name, self.email, self.passw, self.cep, self.ipv4 = name, email, passw, cep, ipv4
        self.serv = server

        self.conected = None
        self.tipoConec = CONNECTION_TYPE["NONE"]
        self.sockUser = sockUser 
    
    def receiveMsgUser(self, message, whoSent):

        self.usersChannel[whoSent].append(message)

        if (self.tipoConec == CONNECTION_TYPE["CHANNEL"] and self.conected == whoSent):
            self.sockUser.send(message.encode("utf-32"))
    
    def receiveMsgGrupo(self, message, whoSent, toPropImage = True):

        if (self.tipoConec == CONNECTION_TYPE["GROUP"] and self.conected == whoSent):
            self.sockUser.send(message.encode("utf-32"))
            if message[0] == "*" and toPropImage: #if is a upload 
                print("É O CODAS")
                filename = "./rec/"+ message.split(":")[1]
                file_size = os.path.getsize(filename)

                with open(filename, "rb") as file:
                    c = 0 
                    while c <= file_size:
                        data = file.read(1024)
                        if not (data):
                            break
                        self.sockUser.sendall(data)
                        c += len(data)

                
    def start(self):
       prev_message= ""
       while True:
            try:
                mensagem = self.sockUser.recv(1024).decode("utf-32")
            except:
                pass
            
            if (mensagem == "" or (mensagem == prev_message and mensagem.startswith("2U"))) :
                continue

            prev_message = mensagem
           
            """
                0 -> open connection
                1 -> close
                2 -> message for group/channel
                2U -> message as file/video/audio for group/channel
                3 -> logout
                4 -> quer adicionar um novo usuario
                5 -> manda convite
                6 -> pede pra entrar
                7 -> entra
                8 -> cria grupo
                9 -> sai Grupo
                11 -> pede Users
                10 -> pede Groups
                12 -> Quero infos desse usuario
                13 -> take notifications
                0|tipo|email ou nome
                1|
                2|groupName|userName|message
                2U|tipo|destUser|userName|filename|file_size
                4|nome
                5|grupo|email
                6|grupo|email
                7|grupo|email
                8|grupo|email
                9|NomeGrupo|email
                12|userName
           """

            message = mensagem.split("|")

            match message[0]:
                case ('0'):
                    try:
                        self.tipoConec = message[1]
                        self.conected = message[2]

                        past_messages = ""
                        if(message[1] == CONNECTION_TYPE["GROUP"]):
                            group = self.findGroup(message[2])
                            group.propagateMessage(f"{self.getName()} joined this chat\n", False)
                            for message in group.messages:
                                past_messages += f"{message}|"
                        else:
                            self.receiveMsgUser(f"você e {message[2]} estao conectados\n", message[2])
                            # self.serv.users[message[2]].receiveMsgUser(f"você e {message[2]} estao conectados", self.getName())
                            for mensagem in self.usersChannel[message[2]]:
                                past_messages += f"{mensagem}|"

                        if(past_messages == ""):
                            past_messages = " " 
                        self.sockUser.send(past_messages.encode("utf-32"))
                    except: 
                        print("CONNECTION ERROR")
                case ('1'):
                    self.conected = None
                    self.tipoConec = None
                case ('2'):
                    try: 
                        if(message[1] == CONNECTION_TYPE["GROUP"]):
                            group = self.serv.groups[message[2]]
                            userMessage = f"{message[3]}: {message[4]}"
                            group.messages.append(userMessage)
                            group.propagateMessage(userMessage)
                        elif(message[1] == CONNECTION_TYPE["CHANNEL"]):
                            userMessage = f"{message[3]}: {message[4]}"
                            self.receiveMsgUser(userMessage, message[2])
                            self.serv.users[message[2]].receiveMsgUser(userMessage, self.getName())
                    except:
                        print("Sending message error")
                case ('2U'):
                    try: 
                        if(message[1] == CONNECTION_TYPE["GROUP"]):
                            filename= "./rec/" + message[4].split("/")[-1]
                            filesize = int(message[5])
                            # print(message)
                            group = self.serv.groups[message[2]]
                            userMessage = f"*{message[3]}:{filename.split("/")[-1]}:{filesize}" #if starts with "*", its a file message
                            # print(filename, filesize, userMessage)
                            with open(filename, "wb") as file:
                                c = 0
                                while c < filesize:
                                    try:
                                        data = self.sockUser.recv(1024)
                                        if (not data) :
                                            break
                                        file.write(data)
                                        c +=  len(data)
                                    except:
                                        print("Download error")
                            group.messages.append(userMessage)
                            group.propagateMessage(userMessage)
                        elif(message[1] == CONNECTION_TYPE["CHANNEL"]):
                            pass # TODO: file messages to users channel
                    except:
                        print("Sending file message error")
                case ('2S'):
                    filename = "./rec/"+ message[1]
                    file_size = int(message[2])

                    with open(filename, "rb") as file:
                        c = 0 
                        while c <= file_size:
                            data = file.read(1024)
                            if not (data):
                                break
                            self.sockUser.sendall(data)
                            c += len(data)
                case ('3'):
                    self.conected = None
                    self.tipoConec = None
                    break
                case ('4'):

                    if (message[1] in self.usersChannel.keys()):
                        continue
                    self.addUser(self.serv.users[message[1]])
                    self.serv.users[message[1]].addUser(self.serv.users[self.name])

                case('5'):
                    if (self.name != self.serv.groups[message[1]].getAdmin()):
                        self.sockUser.send(mensagemUnauthorized.encode("utf-32"))
                        continue

                    # O usuario devera receber o grupo que foi convidado
                    t = threading.Thread(target= self.serv.users[message[2]].rcvInvite, args=(message[1]))
                    t.start()
                    
                case('6'):

                    self.groupsAsked.add(message[1])
                    t = threading.Thread(target= (self.serv.groups[message[1]].getAdmin()).pedidoParaEntrar, args=(message[2]))
                    t.start()

                case('7'):
                    self.tipoConec = CONNECTION_TYPE["GROUP"]
                    self.conected = message[1]
                    # self.serv.users[message[2]].groupsAsked.remove(message[1])
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
                    user = self.serv.users[message[1]]
                    mensagem = f"{user.getName()}|{user.getEmail()}|{user.getCep()}"
                    self.sockUser.send(mensagem.encode("utf-32"))
                case('13'):
                    
                    notif = "|"

                    for noti in self.notifs:
                        notif += f"{noti}|"
                    
                    self.sockUser.send(notif.encode("utf-32"))
                case('14'):
                    group = self.serv.groups[message[1]]
                    self.sockUser.send(f"{group.getName()}|".encode("utf-32"))

    def addUser(self, userStuff):   # esse userStuff é um objeto Usuario

        self.users.append(userStuff)
        self.usersChannel[userStuff.getName()] = list()
        return
    
    def rcvInvite(self, group):

        # 3 implica um convite

        mensagem = "3@"
        mensagem += group + '@'

        self.notifs.append(mensagem)
    
    def pedidoParaEntrar(self, whoWantsIn): # A gente passa ao admin quem pediu pra entrar
        
        message = "4@"

        message += whoWantsIn + '@'

        self.notifs.append(message)
    
    def sairDeUmGrupo(self, grupo):

        self.grupos.remove(grupo)

        # se a gente tivesse mais grupos usar um dict seria melhor
        # para a complexidade

        grupo.propagateMessage(f"{self.name} saiu.")

    
    def addGroup(self, groupStuff): # esse groupStuff é um objeto Grupo

        self.groups.append(groupStuff)
        return

    def findGroup(self, groupName):
        for group in self.serv.groups.values():
            if group.name == groupName:
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