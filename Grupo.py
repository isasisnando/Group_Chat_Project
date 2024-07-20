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

        # Aqui a mensagem será recebida e enviada para todos
        # usuarios com exceçao do q enviou

        mensagemSplitada = mensagem.split('@')

        # propaga a mensagem para todos os usuarios presentes no grupo
        for user in self.users.keys():

            if(user != mensagemSplitada[1]):

                self.users[user].receiveMsgGrupo(mensagem, self.name)
    
    def addUser(self, user):
        self.users[user.getName()] = user
    
    def convite(self):
        pass

    def pedidoParaEntrar(self):
        pass

    def getName(self):
        return self.name
    
    def getAdmin(self):
        return self.admin
    
    
