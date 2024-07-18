class Usuario:

    grupos = list()

    # seria interessante ter outra lista com outros usuarios
    # os quais ele já iniciou uma conversa?
    
    def __init__(self, name, email, passw, cep) -> None:

        self.name, self.email, self.passw, self.cep = name, email, passw, cep

    def getName(self):
        return self.name
    
    def getEmail(self):
        return self.email
    
    def getPassw(self):
        return self.passw
    
    def getCep(self):
        return self.cep