import threading
import tkinter as tk
import tkinter.scrolledtext
import socket 
from ClientUser import ClientUser


HOST = "127.0.0.1"
PORT = 3300
PRIMARY_COLOR =  "#95ECEC"

CONNECTION_TYPE = {
    "GROUP": "GROUP",
    "CHANNEL": "CHANNEL",
    "NONE": None,
}

class ErrorMsg(tk.Tk):
    
    def __init__(self, message):
        super().__init__()

        self.geometry("200x200")

        self.title("ERROR")

        self.frame = tk.Frame(self, background="red")
        self.frame.pack(fill="both", expand=True)

        tk.Label(self.frame, text="Error: "+message, background="black", foreground="white", width=10, height=10).place(relwidth=1, y=75)

class Notif(tk.Tk):

    def __init__(self, message):
        super().__init__()

        self.geometry("200x200")

        self.title("Notificação")

        self.frame = tk.Frame(self, background="green")
        self.frame.pack(fill="both", expand=True)

        tk.Label(self.frame, text="Notificação: "+message, background="black", foreground="white", width=10, height=10).place(relwidth=1, y=75)

        self.mainloop()

# class NotifWtButton(tk.Tk):

#     def __init__(self, message):
#         super().__init__


class Start(tk.Tk):
    def __init__(self):
        super().__init__()

        self.geometry("400x300")

        self.title("Bem vindo ao Chat Room")

        self.frame = tk.Frame(self, background= "#95ECEC")
        self.frame.pack(fill="both", expand=True)

        tk.Label(self.frame, text="Bem vindo ao Chat Room").place(relwidth=1, y=12)

        self.signUp = tk.Button(self.frame, command=self.open_signup, text="Cadastrar", bg="red", relief="raised", height=3, width=10)
        self.signUp.place(x=155, y=110)

        self.logs = tk.Button(self.frame, command=self.open_login, text="Entrar", bg="red", relief="raised", height=3, width=10)
        self.logs.place(x=155, y=180)
        
        self.mainloop()

    def open_login(self):
        LogIn()
        self.destroy()
    def open_signup(self):
        SignUp()
        self.destroy()


class LogIn(tk.Tk):
    def __init__(self):
        super().__init__()

        self.geometry("400x300")

        self.title("insira seus dados")

        self.frame = tk.Frame(self, background= "#95ECEC")
        self.frame.pack(fill="both", expand=True)

        tk.Label(self.frame, text="Insira seus dados:").place(relwidth=1, y = 20)
        tk.Label(self.frame, text="Email:", bg="white").place(x=50, y=100)
        self.email_input = tk.Entry(self.frame, width=20, bg="#D3D3D3")
        self.email_input.place(x=110, y= 100)
        tk.Label(self.frame, text="Senha:", bg="white").place(x=50, y=140)
        self.passw_input = tk.Entry(self.frame, width=25, bg="#D3D3D3", show="*")
        self.passw_input.place(x=110, y= 140)

        self.submit = tk.Button(self.frame, command=self.login, text="Entrar", bg="red", relief="raised", height=3, width=10)
        self.submit.place(x=155, y=190)

        self.mainloop()
    
    def login(self): 
        # definitions of the client socket
        self.sockUser = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        _email = self.email_input.get()
        _passw = self.passw_input.get()
        # socket definitions done
        # this is the first connection so we need to
        # sign up this big person
        self.sockUser.connect((HOST, PORT))
        mensagem = f"1|{_email}|{_passw}|"
        self.sockUser.send(mensagem.encode("utf-32"))
        resp = self.sockUser.recv(1024).decode("utf-32")
        resp = resp.split(" : ")
        if(resp[0] == "login Done"):
            self.destroy()
            self.user = ClientUser(resp[1], _email, _passw, resp[2], self.sockUser)
            IntialPage(self.user)
            return
        
        self.destroy()
        self.sockUser.close()
        ErrorMsg("EMAIL OU SENHA ERRADO.")
        LogIn()

class SignUp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((HOST, PORT))
        
        self.geometry("400x300")

        self.title("Chat room")
        self.user = None
        
        self.frame = tk.Frame(self, background=PRIMARY_COLOR)
        self.frame.pack(fill="both", expand=True)

        tk.Label(self.frame, text="SignUp").place(relwidth=1, y=24)

        self.name = tk.Label(self.frame, text= "Name", bg="white")
        self.name.place(x=80, y=150)
        self.name_input = tk.Entry(self.frame, width=20, bg="#D3D3D3")
        self.name_input.place(x=150, y= 150)
        self.email = tk.Label(self.frame, text= "Email", bg="white")
        self.email.place(x=80, y= 180)
        self.email_input = tk.Entry(self.frame, width=25, bg="#D3D3D3")
        self.email_input.place(x=150, y= 180)
        self.passw = tk.Label(self.frame, text= "Password", bg="white")
        self.passw.place(x=80, y= 210)
        self.passw_input = tk.Entry(self.frame, width=25, bg="#D3D3D3", show="*")
        self.passw_input.place(x=150, y=210)
        self.cep = tk.Label(self.frame, text= "CEP", bg="white")
        self.cep.place(x=80, y= 240)
        self.cep_input = tk.Entry(self.frame, width=20, bg="#D3D3D3")
        self.cep_input.place(x=150, y=240)

        self.submit = tk.Button(self.frame, command=self.signup, text="Connect", bg="red", relief="solid")
        self.submit.place(x=200, y=275)

        self.mainloop()

    
    def signup(self):
        name = self.name_input.get()
        passw = self.passw_input.get()
        email = self.email_input.get()
        cep = self.cep_input.get()

        if(name and passw and email and cep):
            message = f"0|{email}|{name}|{passw}|{cep}"
            self.user = ClientUser(name, email, passw, cep, self.socket)

            self.socket.send(message.encode('utf-32'))

            resp = self.socket.recv(1024).decode("utf-32")

            if (resp == "Já existe usuario com esse email"):

                self.destroy()
                ErrorMsg("Já existe usuario com esse email")
                self.socket.close()
                SignUp()
                return
            
            self.destroy()
            IntialPage(self.user)


class IntialPage(tk.Tk):
    def __init__(self, user: ClientUser):
        super().__init__()

        self.user = user 

        self.geometry("450x450")

        self.title("Tela de Inicial")

        self.frame = tk.Frame(self, background= "#95ECEC")
        self.frame.pack(fill="both", expand=True)

        tk.Label(self.frame, text="Tela inicial").place(relwidth=1, y=24)

        self.create_group_btn = tk.Button(self.frame, command=self.create_group, text="Criar grupo", bg="red", relief="raised", height=1, width=10)
        self.create_group_btn.place(x=0, y=0)

        tk.Label(self.frame, text="Nome:").place(x=50, y= 100)
        tk.Label(self.frame, text=self.user.getName()).place(x= 90, y= 100)
        tk.Label(self.frame, text="Email:").place(x=50, y= 135)
        tk.Label(self.frame, text=self.user.getEmail()).place(x= 90, y= 135)
        tk.Label(self.frame, text="CEP:").place(x= 50, y= 170)
        tk.Label(self.frame, text=self.user.getCep()).place(x= 90, y= 170)

        self.users_dropdown_label = tk.Label(self.frame, text="Usuários:", background="white")
        self.users_dropdown_label.place(x=170, y=90)


        self.users_click = tk.StringVar(self.frame)
        self.users_click.set("Escolher")
        self.users_dropdown = tk.OptionMenu(self.frame, self.users_click, None,*self.user.takeUsers())
        self.users_dropdown.place(x=230, y=90)
       
        self.users_button_dropdown = tk.Button(self.frame, background="#FFFFFF",text="Escolher usuário", command=self.choose_user)
        self.users_button_dropdown.place(x=230, y=125)

        self.groups_dropdown_label = tk.Label(self.frame, text="Grupos:", background="white")
        self.groups_dropdown_label.place(x=170, y=165)

        self.groups_click = tk.StringVar(self.frame)
        self.groups_click.set("Escolher")
        self.groups_dropdown = tk.OptionMenu(self.frame, self.groups_click , None, *self.user.takeGroups())
        self.groups_dropdown.place(x=230, y=165)

        self.groups_button_dropdown = tk.Button(self.frame, background="#FFFFFF",text="Escolher grupo", command=self.choose_group)
        self.groups_button_dropdown.place(x=230, y=200)

        self.frame.mainloop()

    def choose_group(self):
        self.destroy()
        Chat(self.user, self.groups_click.get(), "GROUP")

    def choose_user(self):
        self.destroy()
        PerfilScreen(self.user, self.users_click.get())

    def change_dropdown_label(self):
        self.dropdown_label.config(text = self.clicked.get())

    def create_group(self):
        self.destroy()
        CreateGroup(self.user)

class CreateGroup(tk.Tk):
    def __init__(self, user: ClientUser):
        super().__init__()
        self.geometry("400x300")
        self.title("Create group")
        
        self.user = user 

        self.frame = tk.Frame(self, background= "#95ECEC")
        self.frame.pack(fill="both", expand=True)

        tk.Label(self.frame, text="Criação de grupo").place(relwidth=1, y=24)

        self.group_name = tk.Label(self.frame, text= "Nome do grupo", bg="white")
        self.group_name.place(x=80, y=150)
        self.group_name_input = tk.Entry(self.frame, width=20, bg="#D3D3D3")
        self.group_name_input.place(x=80, y= 180)

        self.submit = tk.Button(self.frame, command=self.create_group, text="Criar Grupo", bg="red", relief="raised", height=1, width=10)
        self.submit.place(x=155, y=210)


    def create_group(self):
        message = f"8|{self.group_name_input.get()}|{self.user.getName()}"
        self.user.sockUser.send(message.encode("utf-32"))
        self.destroy()
        IntialPage(self.user)

class Chat(tk.Tk): 
    def __init__(self, user: ClientUser, chatName, tipoChat):
        super().__init__()
        self.user = user
        self.destName = chatName
        self.tipoChat = tipoChat
        self.running = True 
        self.interface_done = False

        run_thread = threading.Thread(target=self.run_app)
        run_thread.daemon = True
        receive_thread = threading.Thread(target=self.receive)
        receive_thread.daemon = True
        run_thread.start()
        receive_thread.start()
    
    def connectToUser(self):
        messages = self.user.openConection(CONNECTION_TYPE["CHANNEL"], self.destName)
        for message in messages: 
            self.text_area.config(state="normal")
            self.text_area.insert('end', message)
            self.text_area.yview('end')
            self.text_area.config(state= "disabled")

    def connectToGroup(self):
        self.user.acceptInGroup(self.destName)
        messages = self.user.openConection(CONNECTION_TYPE["GROUP"], self.destName)
        for message in messages: 
            self.text_area.config(state="normal")
            self.text_area.insert('end', message)
            self.text_area.yview('end')
            self.text_area.config(state= "disabled")


    def run_app(self):
        self.frame = tk.Tk()
        # self.geometry("400x650")
        self.frame.configure(bg= "cyan")
        # self.title(f"{self.group_name} chat")
        self.chat_label = tk.Label(self.frame, text = f"{self.destName} chat:", bg="lightgray")
        self.chat_label.config(font=("Arial", 12))
        self.chat_label.pack(padx=20, pady=5)
        
        self.text_area = tkinter.scrolledtext.ScrolledText(self.frame)
        self.text_area.pack(padx=20, pady=5)
        self.text_area.config(state='disabled', bg=PRIMARY_COLOR)

        self.msg_label = tk.Label(self.frame, text="Message:", bg="lightgray")
        self.msg_label.config(font=("Arial", 12))
        self.msg_label.pack(padx=20, pady=5)

        self.input_area = tk.Text(self.frame, height=3, bg=PRIMARY_COLOR)
        self.input_area.pack(padx=20, pady=5)

        self.send_button = tk.Button(self.frame, text = "Send", command=self.write)
        self.send_button.config(font=("Arial", 12))
        self.send_button.pack(padx=20, pady=5)

        self.interface_done = True
        self.frame.protocol("WM_DELETE_WINDOW", self.stop)
        
        if(self.tipoChat == CONNECTION_TYPE["GROUP"]):
            self.connectToGroup()
        else:
            self.connectToUser()
        
        self.frame.mainloop()

    def write(self):
        if (self.tipoChat == CONNECTION_TYPE["GROUP"]):
            self.user.sendMsgGroup(self.destName, self.user.getName(), self.input_area.get('1.0', 'end'))
        elif (self.tipoChat == CONNECTION_TYPE["CHANNEL"]): 
            self.user.sendMsgUser(self.destName, self.user.getName(), self.input_area.get('1.0', 'end'))
    
        self.input_area.delete('1.0', 'end')
    
    def stop(self):
        self.running = False
        self.frame.destroy()
        message = f"{self.user.getName()} has left the chat"
        self.user.sockUser.send(message.encode("utf-32"))
        self.input_area.delete('1.0', 'end')
        self.user.closeConection()
        IntialPage(self.user)

    def receive(self):
        while self.running:
            try:
                if self.interface_done:
                    message = self.user.sockUser.recv(1024)
                    self.text_area.config(state="normal")
                    self.text_area.insert('end', message.decode("utf-32"))
                    self.text_area.yview('end')
                    self.text_area.config(state= "disabled")
            except ConnectionAbortedError: 
                break
            except:
                print("Error")
                self.user.sockUser.close()
                break

class PerfilScreen(tk.Tk):
    
    def __init__(self, user : ClientUser, personName : str):
        super().__init__()

        self.geometry("360x300")
        self.title("Informações pessoais")

        self.frame = tk.Frame(self, background= "#95ECEC")
        self.frame.pack(fill="both", expand=True)

        tk.Label(self.frame, text="Informações pessoais").place(relwidth=1, y=24)

        self.user = user

        self.user.sockUser.send((f"12|{personName}").encode("utf-32"))

        self.resp = self.user.sockUser.recv(1024).decode("utf-32")

        self.resp = self.resp.split('|')

        tk.Label(self.frame, text="Nome:", background="#4EABB0", foreground="#006666", font=("Arial", 14)).place(y=75, x=24)
        tk.Label(self.frame, text="Email:", background="#4EABB0",foreground="#006666", font=("Arial", 14)).place(y=140, x=24)
        tk.Label(self.frame, text="CEP:", background="#4EABB0",foreground="#006666", font=("Arial", 14)).place(y=205, x=24)
        tk.Label(self.frame, text=self.resp[0], background="#4EABB0", foreground="#006666", font=("Arial", 14)).place(y=75, x=95)
        tk.Label(self.frame, text=self.resp[1], background="#4EABB0",foreground="#006666", font=("Arial", 14)).place(y=140, x=95)
        tk.Label(self.frame, text=self.resp[2], background="#4EABB0",foreground="#006666", font=("Arial", 14)).place(y=205, x=80)
        tk.Button(self.frame, command=self.openChat, text="Abrir o chat", bg="red", relief="raised", height=1, width=10).place(y=250, x=150)
    
    def openChat(self):

        self.user.sockUser.send((f"4|{self.resp[0]}").encode("utf-32"))

        self.destroy()
        Chat(self.user, self.resp[0], "CHANNEL")
        pass
Start()