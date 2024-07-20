from socket import *

class Grupo:

    users = list()
    messages = list()

    # pessoal, acho q aqui a gente poderia ter um set com o momento que ela entrou
    # pra definir quem seria o novo admin?

    def __init__(self, name, admin):

        self.name, self.admin = name, admin  
        self.users.append(admin)
    
    def getName(self):
        return self.name
    
    def getAdmin(self):
        return self.admin
    
    
