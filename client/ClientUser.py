import socket

PORT = 3300
CONNECTION_TYPE = {
    "GROUP": "GROUP",
    "CHANNEL": "CHANNEL",
    "NONE": None,
}

class ClientUser:

    # Isso aqui seria interessante pra encapsular melhor
    groups = dict()

    def __init__(self, _name, _email, _passw, _cep, _sock = None):
        self.name, self.email, self.passw, self.cep, self.sockUser = _name, _email, _passw, _cep, _sock
    
    def getName(self):
        return self.name
    
    def getEmail(self):
        return self.email
    
    def getCep(self):
        return self.cep

    
    def addFriend(self, who):
        # who é um email
        mensagem = "4|" + who + '|'
        self.sockUser.send(mensagem.encode("utf-32"))
         # A gente tem q fazer close aqui né?

    def rcvServer(self):

        mensagemSrvr = self.sockUser.rcv(1024).decode("utf-32")

        match str(mensagemSrvr):
            case ("Já existe usuario com esse email"):
                
                return("Já existe usuario com esse email")
                # tentou criar uma conta com o email q ja usou

            case ("Nome de Grupo já existe"):
                return("Nome de Grupo já existe")
                # tentou criar nome de grupo q ja existe
            case ("canal com o usuario nao encontrado"):

                # tenta se comunicar com alguem q vc n add
                return("canal com o usuario nao encontrado")
            case ("Você não está autorizado a fazer isso"):

                # tentou convidar alguem
                return("Você não está autorizado a fazer isso")
            case ("Usuario nao encontrado"):

                # tentou adicionar alguem q n existe
                return("Usuario nao encontrado")
            case ("voce nao esta no grupo"):

                # tentou mandar algo para um grupo q ele n ta
                return ("voce nao esta no grupo")

        mensagemSplitada = mensagemSrvr.split('@')

        match mensagemSplitada[0]:
            case ('1'):
                # Passa pro front como a mensagem chegou e se é de usuario

                realMsg = mensagemSplitada[3]

                for i in range(4, len(mensagemSplitada)):

                    realMsg += '@' + mensagemSplitada[i]

                return("usuario", mensagemSplitada[1], realMsg)
            case ('2'):

                realMsg = mensagemSplitada[3]

                for i in range(4, len(mensagemSplitada)):

                    realMsg += '@' + mensagemSplitada[i]

                # Grupo, quem enviou, de qual grupo, msg

                return("grupo", mensagemSplitada[1], mensagemSplitada[2], realMsg)
            case ('3'):
                return("Aceita grupo?", mensagemSplitada[1])
            case ('4'):
                return("Pode entrar?", mensagemSplitada[1])
            case ('5'):
                return("Perdeu Acesso a esse grupo", mensagemSplitada[1])
            case ('6'):
                return("Adicionou esse usuario", mensagemSplitada[1])
            case ('7'):
                return("Voce entrou no grupo", mensagemSplitada[1])
        # Tratar as mensagens de acordo com o estabelecido pelo servidor
    
    def sendMsgUser(self, dest, user, msg):
        mensagem = f"2|CHANNEL|{dest}|{user}|{msg}"
        self.sockUser.send(mensagem.encode("utf-32"))
    
    def sendMsgGroup(self, dest, user,msg):
        mensagem = f"2|GROUP|{dest}|{user}|{msg}"
        self.sockUser.send(mensagem.encode("utf-32"))
    
    def sendInviteGroup(self, who, nomeGrupo): # Who its an email
        mensagem = "5|" + nomeGrupo + '|' + who + '|'
        self.sockUser.send(mensagem.encode("utf-32"))
    
    def acceptInGroup(self, nomeGrupo):
        mensagem = "7|" + nomeGrupo + '|' + self.getEmail() + '|'
        self.sockUser.send(mensagem.encode("utf-32"))
    
    def askInGroup(self, nomeGrupo):
        mensagem = "6|" + nomeGrupo + '|' + self.getEmail() + '|'
        self.sockUser.send(mensagem)

    def openConection(self, type, channel_or_group_name):
        mensagem = f"0|{type}|{channel_or_group_name}"
        self.sockUser.send(mensagem.encode("utf-32"))
        return (list(self.sockUser.recv(1024).decode("utf-32").split('|')))   
    
    def closeConection(self):
        self.sockUser.send(("1|".encode("utf-32")))
    
    def takeGroups(self):
        self.sockUser.send(f"10|".encode("utf-32"))
        return (list(self.sockUser.recv(1024).decode("utf-32").split('|')))
    
    def takeUsers(self):
        self.sockUser.send(f"11|".encode("utf-32"))
        return (list(self.sockUser.recv(1024).decode("utf-32").split('|')))   
    