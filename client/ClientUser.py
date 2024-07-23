import socket

PORT = 3300

class ClientUser:

    # Isso aqui seria interessante pra encapsular melhor

    def __init__(self, _name, _email, _passw, _cep, _login, _sock = None):

        self.name, self.email, self.passw, self.cep, self.sockUser = _name, _email, _passw, _cep, _sock

        # definitions of the client socket

        if(not _login):

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

         # A gente tem q fazer close aqui né?

        self.sockUser.close()

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
    
    def sendMsgUser(self, dest, msg):

        # Here the user sends a msg to another user

        self.sockUser.connect((socket.gethostbyname(), PORT))

        mensagem = "2|1@" + self.getName() + "@" + dest + '@' + msg + '@'

        self.sockUser.send(mensagem)

        self.sockUser.close()
    
    def sendMsgGroup(self, dest, msg):

        self.sockUser.connect((socket.gethostbyname(), PORT))

        mensagem = "2|2@" + self.getName() + "@" + dest + '@' + msg + '@'

        self.sockUser.send(mensagem)

        self.sockUser.close()
    
    def sendInviteGroup(self, who, nomeGrupo): # Who its an email

        self.sockUser.connect((socket.gethostbyname(), PORT))

        mensagem = "5|" + nomeGrupo + '|' + who + '|'

        self.sockUser.send(mensagem)

        self.sockUser.close()
    
    def acceptInGroup(self, nomeGrupo, whoIn):

        self.sockUser.connect((socket.gethostbyname(), PORT))

        mensagem = "7|" + nomeGrupo + '|' + whoIn + '|'

        self.sockUser.send(mensagem)

        self.sockUser.close()
    
    def askInGroup(self, nomeGrupo):

        self.sockUser.connect((socket.gethostbyname(), PORT))

        mensagem = "6|" + nomeGrupo + '|' + self.getEmail() + '|'

        self.sockUser.send(mensagem)

        self.sockUser.close()
    