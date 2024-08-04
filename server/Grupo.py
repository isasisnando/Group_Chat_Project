from socket import *
import threading
import pprint

class Grupo:

    # pessoal, acho q aqui a gente poderia ter um set com o momento que ela entrou
    # pra definir quem seria o novo admin?

    def __init__(self, name, admin):

        self.users = dict() # dict<Nick, Usuario>
        self.messages = list()
        self.name, self.admin = name, admin 
        self.users[admin.getName()] = admin


    def propagateMessage(self, mensagem, toPropImage = True):
        pprint.pprint(self.users)
        for user in self.users.keys():  
            try:
                self.users[user].receiveMsgGrupo(mensagem, self.name, toPropImage)
            except Exception as e:
                print("Group connection error")
                print(e)

    
    def User(self, user):
        self.users[user.getName()] = user
    
    def eraseUser(self, user):
        del self.users[user.getName()]
        print(self.users.keys())
    
    def addUser(self, user):
        self.users[user.getName()] = user
        print(self.users.keys())
    
    def getName(self):
        return self.name
    
    def getAdmin(self):
        return self.admin