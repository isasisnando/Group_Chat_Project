from PIL import Image
import socket
import os

PORT = 3300
CONNECTION_TYPE = {
    "GROUP": "GROUP",
    "CHANNEL": "CHANNEL",
    "NONE": None,
}

class ClientUser:

    def __init__(self, _name, _email, _passw, _cep, _sock = None):
        self.groups = dict()
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
    
    def sendMsgUser(self, dest, user, msg, prev=False):
        mensagem = f"2|CHANNEL|{dest}|{user}|{msg}{"|" if prev else ""}"
        self.sockUser.send(mensagem.encode("utf-32"))
    
    def sendMsgGroup(self, dest, user,msg, prev= False):
        mensagem = f"2|GROUP|{dest}|{user}|{msg}{"|" if prev else ""}"
        self.sockUser.send(mensagem.encode("utf-32"))

    
    def sendUpload(self, dest, user,filename, type = CONNECTION_TYPE["GROUP"]):
        file_size = os.path.getsize(filename)
        mensagem = f"2U|{type}|{dest}|{user}|{filename}|{file_size}"
        self.sockUser.send(mensagem.encode("utf-32"))
        
        with open(filename, "rb") as file:
            c = 0 
            while c <= file_size:
                data = file.read(1024)
                if not (data):
                    break
                self.sockUser.sendall(data)
                c += len(data)

    
    def sendInviteGroup(self, who, nomeGrupo): # Who its an email
        mensagem = "5|" + nomeGrupo + '|' + who + '|'
        self.sockUser.send(mensagem.encode("utf-32"))
    
    def acceptInGroup(self, nomeGrupo):
        mensagem = "7|" + nomeGrupo + '|' + self.getName() + '|'
        self.sockUser.send(mensagem.encode("utf-32"))
    
    def askInGroup(self, nomeGrupo):
        mensagem = "6|" + nomeGrupo + '|' + self.getName() + '|'
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
    
    def takeMyGroups(self):
        self.sockUser.send(f"10S|".encode("utf-32"))
        return (list(self.sockUser.recv(1024).decode("utf-32").split('|')))
    
    def takeUsers(self):
        self.sockUser.send(f"11|".encode("utf-32"))
        return (list(self.sockUser.recv(1024).decode("utf-32").split('|')))   
    
    def getSingleFile(self, filename, filesize):
        mensagem = f"2S|{filename}|{filesize}"
        self.sockUser.send(mensagem.encode("utf-32"))   
        print(mensagem)     
        filename ="./rec/" +filename
        with open(filename, "wb") as file:
                c = 0
                while c < filesize:
                    data = self.sockUser.recv(1024)
                    if not (data):
                        break
                    file.write(data)
                    c += len(data)
        if (filename.endswith(".mp3")):
            return filename

        image = Image.open(filename)
        image = image.resize((120, 120))
        return image


