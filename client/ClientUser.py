import socket

PORT = 3300

mensagemNaoEncontrouUser = "Usuario nao esta no servidor"
mensagemUnauthorized = "Você não está autorizado a fazer isso"
mensagemGroupNameUsed = "Nome de Grupo já existe"
mensagemExistsUserEmail = "Já existe usuario com esse email"

class ClientUser:
    # Isso aqui seria interessante pra encapsular melhor

    def __init__(self, _name, _email, _passw, _cep):

        self.name, self.email, self.passw, self.cep = _name, _email, _passw, _cep

        # definitions of the client socket

        self.sockUser = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # socket definitions done
        # this is the first connection so we need to
        # sign up this big person

        self.sockUser.connect(socket.gethostbyname(), PORT)

        mensagem = "0|" + _email + "|" + _name + "|" + _passw + "|" + _cep + "|"

        self.sockUser.send(mensagem)

        # A gente tem q fazer close aqui né?

        self.sockUser.close()
    
    def getName(self):
        return self.name
    
    def getEmail(self):
        return self.email
    
    def addFriend(self, who):

        # who é um email

        self.sockUser.connect(socket.gethostbyname(), PORT)

        mensagem = "4|" + who + '|'

        self.sockUser.send(mensagem.encode("utf-32"))

        self.sockUser.close()

    def rcvServer(self):

        mensagemSrvr = self.sockUser.rcv(1024).decode("utf-32")

        # Tratar as mensagens de acordo com o estabelecido pelo servidor
        




