from socket import *

mensagemNotFoundUser = "Usuario nao encontrado"

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
    
    def receiveMsg(self, message, orig):

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

        self.sock.send(message.encode("utf-8"))
    
    def sendMsgToUser(self, message, dest):

        # procuramos se estamos mandando msg pra algum usuario
        # com algum canal

        for user in self.users:

            if(dest == user.getName()):

                return list(message, user)
        
        return list(mensagemNotFoundUser, "NF")

    def serverRcv(self):

        # acredito q temos problemas nessa parte
        # como fazer pra receber msgs de varios sockets diferentes dos usuarios?

        mensagem = self.sockUser.recv(1024).decode("utf-8")

        # aqui temos q tratar a mensagem

        return(self.sendMsgToUser(mensagemAlterada, dest))

    # The main idea in this two methods is to
    # make the process of creating new chanels more
    # easy

    def addUser(userStuff):   # esse userStuff é um objeto Usuario

    

    def addGroup():
    
    
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