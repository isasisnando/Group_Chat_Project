from socket import *
import threading

class Grupo:

    users = dict() # dict<Nick, Usuario>
    messages = list()

    # pessoal, acho q aqui a gente poderia ter um set com o momento que ela entrou
    # pra definir quem seria o novo admin?

    def __init__(self, name, admin):

        self.name, self.admin = name, admin 
        self.users[admin.getName()] = admin

    def propagateMessage(self, message): 
        self.admin.sockUser.send(message.encode("utf-32"))
        for user in self.users.values():
            if user.getName() != self.admin.getName(): # TODO: dont send 2 messages for admin
                try:
                    user.sockUser.send(message.encode("utf-32"))
                except:
                    print("ERRO")
    def rcvAndPropMsg(self, mensagem):

        # Aqui a mensagem será recebida e enviada para todos
        # usuarios com exceçao do q enviou

        mensagemSplitada = mensagem.split('@')

        # propaga a mensagem para todos os usuarios presentes no grupo
        for user in self.users.keys():

            if(user != mensagemSplitada[1]):

                t = threading.Thread(target= self.users[user].receiveMsgGrupo, args=(mensagem, self.name))
                t.start()
    
    def User(self, user):
        self.users[user.getName()] = user
    
    def eraseUser(self, user):
        del self.users[user.getName()]

        mensagem = "2@" + user.getName() + "@saiu"

        self.rcvAndPropMsg(mensagem)
    
    def addUser(self, user):
        self.users[user.getEmail()] = user
    
    def getName(self):
        return self.name
    
    def getAdmin(self):
        return self.admin
    
    
