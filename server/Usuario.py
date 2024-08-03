from socket import *
import os 
from Grupo import Grupo
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

    # isso aqui vai funcionar como uma pilha de notificacoes
    #  toda vez q entrar a gente manda essas notificacoes
    # tem q marcar tbm os grupos q ja pediu pra entrar

    def __init__(self, name, email, passw, cep, ipv4, sockUser, server) -> None:

        self.users = list()
        self.groupsAsked = set()
        self.groups = list()
        self.usersChannel = dict() # dict<name, msgs>
        self.notifs = list() 
        self.name= name
        self.email= email
        self.passw= passw
        self.cep= cep
        self.ipv4= ipv4
        self.serv = server

        self.conected = None
        self.tipoConec = CONNECTION_TYPE["NONE"]
        self.sockUser = sockUser 
    
    def receiveMsgUser(self, message, whoSent):

        self.usersChannel[whoSent].append(message)

        if (self.tipoConec == CONNECTION_TYPE["CHANNEL"] and self.conected == whoSent):
            try:
                self.sockUser.send(message.encode("utf-32"))
            except Exception as e:
                print(e)
                self.conected = None
                self.tipoConec = None
    
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
                14 -> take Group Name
                15 -> take if im in this group
                16 -> refuses any request to a group
                0|tipo|email ou nome
                1|
                2|groupName|userName|message
                2U|tipo|destUser|userName|filename|file_size
                4|nome
                5|grupo|nome
                6|grupo|nome
                7|grupo|nome
                8|grupo|nome
                9|NomeGrupo|email
                12|userName
                14|groupName
                15|groupName
                16|groupName|name
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
                    except Exception as e: 
                        print("CONNECTION ERROR")
                        print(e)
                        breakpoint()
                        self.sockUser.close()
                        self.conected = None
                        self.tipoConec = None

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
                        self.sockUser.close()
                        self.conected = None
                        self.tipoConec = None
                        
                case ('2U'):
                    try: 
                        if(message[1] == CONNECTION_TYPE["GROUP"]):
                            filename= "./rec/" + message[4].split("/")[-1]
                            filesize = int(message[5])
                            # print(message)
                            group = self.serv.groups[message[2]]
                            userMessage = f"*{message[3]}:{filename.split('/')[-1]}:{filesize}" #if starts with "*", its a file message
                            # print(filename, filesize, userMessage)
                            try:
                                with open(filename, "wb") as file:
                                    c = 0
                                    while c < filesize:
                                            data = self.sockUser.recv(1024)
                                            if (not data) :
                                                break
                                            file.write(data)
                                            c +=  len(data)
                                group.messages.append(userMessage)
                                group.propagateMessage(userMessage)
                            except:
                                print("Download error")
                                self.sockUser.close()
                                self.conected = None
                                self.tipoConec = None
                        elif(message[1] == CONNECTION_TYPE["CHANNEL"]):
                            pass # TODO: file messages to users channel
                    except:
                        print("Sending file message error")
                        self.sockUser.close()
                        self.conected = None
                        self.tipoConec = None
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
                    # O usuario devera receber o grupo que foi convidado
                    if (message[1] in self.serv.users[message[2]].groupsAsked):
                        continue
                    if (self.serv.users[message[2]].inGrupos(message[1]) == None):
                        self.sockUser.send("ok".encode("utf-32"))
                    else:
                        self.sockUser.send("esse usuario já está no grupo.".encode("utf-32"))
                        continue
                    self.serv.users[message[2]].groupsAsked.add(message[1])
                    self.serv.users[message[2]].rcvInvite(message[1])
                    
                case('6'):

                    print('1')
                    if (message[1] in self.groupsAsked):
                        print('2')
                        self.sockUser.send("ok".encode("utf-32"))
                        continue
                    if (self.inGrupos(message[1]) == None):
                        print('3')
                        self.sockUser.send("ok".encode("utf-32"))
                    else:
                        print('4')
                        self.sockUser.send("você já está no grupo.".encode("utf-32"))
                        continue
                    self.groupsAsked.add(message[1])
                    self.serv.groups[message[1]].getAdmin().pedidoParaEntrar(message[2], message[1])

                case('7'):
                    # self.tipoConec = CONNECTION_TYPE["GROUP"]
                    # self.conected = message[1]
                    print(message)
                    self.serv.users[message[2]].groupsAsked.remove(message[1])
                    self.serv.groups[message[1]].addUser(self.serv.users[message[2]])
                    self.serv.users[message[2]].addGroup(self.findGroup(message[1]))
                
                case('8'):
                    if (message[1] in self.serv.groups.keys()):
                        self.sockUser.send(mensagemGroupNameUsed.encode("utf-32"))
                        continue

                    newGrupo = Grupo(message[1], self.serv.users[message[2]])

                    self.serv.groups[message[1]] = newGrupo
                    self.groups.append(self.serv.groups[message[1]])

                case('9'):

                    if (message[1] not in self.serv.users[message[2]].groups):
                        self.serv.users[message[2]].sockUser.send(f"{message[2]} nao esta no grupo".encode("utf-32"))
                        continue

                    self.serv.groups[message[1]].eraseUser(self.serv.users[message[2]])
                    self.serv.users[message[2]].sairDeUmGrupo(self.serv.groups[message[1]])
                    self.serv.users[message[2]].sockUser.send("ok".encode("utf-32"))
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

                    self.notifs.clear()
                    
                    self.sockUser.send(notif.encode("utf-32"))
                case('14'):
                    group = self.serv.groups[message[1]]
                    self.sockUser.send(f"{group.getName()}|{group.getAdmin().getName()}".encode("utf-32"))
                case('15'):

                    if(self.inGrupos(message[1]) == None):
                        self.sockUser.send("voce nao esta no grupo".encode("utf-32"))
                        continue

                    self.sockUser.send("esta no grupo".encode("utf-32"))
                case('16'):

                    self.serv.users[message[2]].groupsAsked.remove(message[1])

    def addUser(self, userStuff):   # esse userStuff é um objeto Usuario

        self.users.append(userStuff)
        self.usersChannel[userStuff.getName()] = list()
        return
    
    def rcvInvite(self, group):

        # 3 implica um convite
        mensagem = f"3@{group}@"
        print(mensagem)
        self.groupsAsked.add(group)
        self.notifs.append(mensagem)

    def pedidoParaEntrar(self, whoWantsIn, wichGroup): # A gente passa ao admin quem pediu pra entrar
        
        message = f"4@{wichGroup}@{whoWantsIn}"
        print(message)
        self.notifs.append(message)
    
    def sairDeUmGrupo(self, grupo):

        self.groups.remove(grupo)
        print(self.groups)
        # se a gente tivesse mais grupos usar um dict seria melhor
        # para a complexidade

        grupo.propagateMessage(f"{self.name} saiu.")

    def addGroup(self, groupStuff): # esse groupStuff é um objeto Grupo
        self.groups.append(groupStuff)
        print(self.groups)
        return

    def findGroup(self, groupName):
        for group in self.serv.groups.values():
            if group.name == groupName:
                return group
    
    def inGrupos(self, groupName):

        for grupo in self.groups:
            if grupo.name == groupName:
                print(self.groups)
                return grupo
        
        return None
    
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