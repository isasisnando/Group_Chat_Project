from socket import *

class Grupo:

    users = dict() # dict<Nick, Usuario>
    messages = list()

    # pessoal, acho q aqui a gente poderia ter um set com o momento que ela entrou
    # pra definir quem seria o novo admin?

    def __init__(self, name, admin):

        self.name, self.admin = name, admin 
        self.users.append(admin)
    
    def rcvAndPropMsg(self, mensagem):

        # Aqui a mensagem é armazenada para futuras requisições das mensagens

        self.messages.append(mensagem)
    
    def retornaMsg(self):

        return(self.messages)
    
    def addUser(self, user):
        self.users[user.getName()] = user
    
    def eraseUser(self, user):
        del self.users[user.getName()]

        mensagem = "2@" + user.getName() + "@saiu"

        self.rcvAndPropMsg(mensagem)
    
    def getName(self):
        return self.name
    
    def getAdmin(self):
        return self.admin
    
    
