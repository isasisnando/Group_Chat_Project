from socket import *

porta = 3333

class Usuario:

    grupos = list()
    users = list()

    # seria interessante ter outra lista com outros usuarios
    # os quais ele já iniciou uma conversa? Acho q essa lista é
    # algo já implementado naquele exemplo de IRC, link:
    # https://github.com/Gabrielcarvfer/Redes-de-Computadores-UnB/blob/master/trabalhos/20181/Lab2/ExemploIRC.py

    
    def __init__(self, name, email, passw, cep, ipv4, sockDoUsuario) -> None:

        self.name, self.email, self.passw, self.cep, self.ipv4 = name, email, passw, cep, ipv4

        # Sockets definitions
        self.sockUser = sockDoUsuario
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind(self.sock.gethostname(), porta)
        self.sock.listen(5)

        # We wants to listen to the messages received
        # and to the messages that are going to be sent

        # Runnig the thing
        self.server()
    
    def server(self):

        while(True):

            usuarioSocket, enderecoUsuario = self.sock.accept()

            # Acho q aqui talvez fosse interessante colocar algo
            # pra identificar de onde vem essa msg
            # se é esse usuario mesmo q ta enviando ou  afins

            mensagemRcvd = self.sock.recv(1024).decode("utf-8")

            # Como sabemos se a mensagem enviada foi de um usuario ou de um grupo?
            # acredito q tenhamos q tratar as mensagens de grupos um pouco diferente
            # ao passar para a interface

            # Aqui embaixo vou fazer um esboço da implementação do processamento da
            # mensagem recebida de um usuario para usuario

            aux = list(usuarioSocket, enderecoUsuario)

            if aux not in self.users:

                self.addUser(aux)
            
            self.sockUser.send(mensagemRcvd.encode("utf-8"))



    # The main idea in this two methods is to
    # make the process of adding peoples more
    # easy

    def addUser(sockAndAdress, nick):

    

    def addGroup():
    
    
    def getName(self):
        return self.name
    
    def getEmail(self):
        return self.email
    
    def getPassw(self):
        return self.passw
    
    def getCep(self):
        return self.cep