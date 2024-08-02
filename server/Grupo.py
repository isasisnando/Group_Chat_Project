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


    def propagateMessage(self, mensagem, toPropImage = True):
        for user in self.users.keys():  
            self.users[user].receiveMsgGrupo(mensagem, self.name, toPropImage)

    
    def User(self, user):
        self.users[user.getName()] = user
    
    def eraseUser(self, user):
        del self.users[user.getName()]
    
    def addUser(self, user):
        self.users[user.getEmail()] = user
    
    def getName(self):
        return self.name
    
    def getAdmin(self):
        return self.admin
