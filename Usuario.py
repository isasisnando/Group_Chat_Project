from socket import *

mensagemNotFoundUser = "Usuario nao encontrado"
mensagemNotFoundGrupo = "Grupo nao encontrado"

class Usuario:

    grupos = list()
    users = list()

    # seria interessante ter outra lista com outros usuarios
    # os quais ele já iniciou uma conversa? Acho q essa lista é
    # algo já implementado naquele exemplo de IRC, link:
    # https://github.com/Gabrielcarvfer/Redes-de-Computadores-UnB/blob/master/trabalhos/20181/Lab2/ExemploIRC.py

    def __init__(self, name, email, passw, cep, ipv4, sockUser) -> None:

        self.name, self.email, self.passw, self.cep, self.ipv4 = name, email, passw, cep, ipv4

        # Sockets definitions are already done in the server

        self.sockUser = sockUser 
    
    def receiveMsgUser(self, message, orig):

        found = False

        # tem de se checar se uma conexao já foi estabelecida
        # entre esses usuarios

        for user in self.users:

            if(user.getName() == orig):
                found = True
                break

        if(not found):
            self.addUser(orig)
        # Devolvemos essa mensagem pro nosso usuario

        self.sockUser.send(message.encode("utf-32"))
    
    def receiveMsgGrupo(self, message, orig):

        found = False

        # tem de se checar se o usuario está no grupo

        for grupo in self.grupos:

            if(grupo.getName() == orig):

                found = True
                break

        if(not found):

            return
        # Devolvemos essa mensagem pro nosso usuario

        self.sockUser.send(message.encode("utf-32"))
    
    def sendMsgToUser(self, message, dest):

        # procuramos se estamos mandando msg pra algum usuario
        # com algum canal

        for user in self.users:

            if(dest == user.getName()):

                return list(message, user)
        
        return list(mensagemNotFoundUser, "NF")
    
    def sendMsgToGroup(self, message, dest):

        # procuramos se estamos mandando mensagem para algum grupo
        # com algum canal já existente

        for grupo in self.grupos:

            if(dest == grupo.getName()):

                return list(message, grupo)
        
        return list(mensagemNotFoundGrupo, "NF")

    def serverRcv(self, mensagem):
        
        # 1@emerson@lucas@...
        # 1, 2, 3 - > identifica se é mensagem para um usuario ou grupo
        # ou um convite para um grupo
        # orig - > quem está mandando
        # dest - > quem tem q receber

        mensagemSplitada = mensagem.split('@')

        if(mensagemSplitada[0] == '2'):
            return(self.sendMsgToGroup(mensagem, mensagemSplitada[2]))

        return(self.sendMsgToUser(mensagem, mensagemSplitada[2]))

    # The main idea in this two methods is to
    # make the process of creating new chanels more
    # easy

    def addUser(self, userStuff):   # esse userStuff é um objeto Usuario

        self.users.append(userStuff)
        
        return
    
    def rcvInvite(self, group):

        # 3 implica um convite

        mensagem = "3@"
        mensagem += group

        self.sockUser.send(mensagem.encode("utf-32"))
    
    def addGroup(self, groupStuff): # esse groupStuff é um objeto Grupo

        self.grupos.append(groupStuff)
        return
    
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