import tkinter as tk
import tkinter.scrolledtext
import socket 
from ClientUser import ClientUser

HOST = "127.0.0.1"
PORT = 3300

class ErrorMsg(tk.Tk):
    
    def __init__(self, message):
        super().__init__()

        self.geometry("200x200")

        self.title("ERROR")

        self.frame = tk.Frame(self, background="red")
        self.frame.pack(fill="both", expand=True)

        tk.Label(self.frame, text="Error: "+message, background="black", foreground="white", width=10, height=10).place(relwidth=1, y=75)

        LogIn()
        self.mainloop()

class Start(tk.Tk):
    def __init__(self):
        super().__init__()

        self.geometry("400x300")

        self.title("Bem vindo ao Chat Room")

        self.frame = tk.Frame(self, background="#95ECEC")
        self.frame.pack(fill="both", expand=True)

        tk.Label(self.frame, text="Bem vindo ao Chat Room").place(relwidth=1, y=12)

        self.signUp = tk.Button(self.frame, command=SignUp, text="Cadastrar", bg="red", relief="raised", height=3, width=10)
        self.signUp.place(x=155, y=110)

        self.logs = tk.Button(self.frame, command=LogIn, text="Entrar", bg="red", relief="raised", height=3, width=10)
        self.logs.place(x=155, y=180)
        
        self.mainloop()

class LogIn(tk.Tk):
    def __init__(self):
        super().__init__()

        self.geometry("400x300")

        self.title("insira seus dados")

        self.frame = tk.Frame(self, background="#95ECEC")
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

            self.user = ClientUser(resp[1], _email, _passw, resp[2], self.sockUser)
            IntialPage(self.user)
            return
        
        self.destroy()
        ErrorMsg("EMAIL OU SENHA ERRADO.")

class SignUp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((HOST, PORT))
        
        self.geometry("400x300")

        self.title("Chat room")
        self.user = None
        
        self.frame = tk.Frame(self, background="white")
        self.frame.pack(fill="both", expand=True)

        tk.Label(self.frame, text="SignUp").place(relwidth=1, y=24)

        self.name = tk.Label(self.frame, text= "Name", bg="gray")
        self.name.place(x=80, y=150)
        self.name_input = tk.Entry(self.frame, width=20, bg="#D3D3D3")
        self.name_input.place(x=150, y= 150)
        self.email = tk.Label(self.frame, text= "Email", bg="gray")
        self.email.place(x=80, y= 180)
        self.email_input = tk.Entry(self.frame, width=25, bg="#D3D3D3")
        self.email_input.place(x=150, y= 180)
        self.passw = tk.Label(self.frame, text= "Password", bg="gray")
        self.passw.place(x=80, y= 210)
        self.passw_input = tk.Entry(self.frame, width=25, bg="#D3D3D3", show="*")
        self.passw_input.place(x=150, y=210)
        self.cep = tk.Label(self.frame, text= "CEP", bg="gray")
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
            IntialPage(self.user)


class IntialPage(tk.Tk):
    def __init__(self, user: ClientUser):
        super().__init__()

        self.user = user 

        self.geometry("450x450")

        self.title("Tela de Inicial")

        self.frame = tk.Frame(self, background="#95ECEC")
        self.frame.pack(fill="both", expand=True)

        tk.Label(self.frame, text="Tela inicial").place(relwidth=1, y=24)
        
        tk.Label(self.frame, text="Nome:").place(x=50, y= 100)
        tk.Label(self.frame, text=self.user.getName()).place(x= 90, y= 100)
        tk.Label(self.frame, text="Email:").place(x=50, y= 135)
        tk.Label(self.frame, text=self.user.getEmail()).place(x= 90, y= 135)
        tk.Label(self.frame, text="CPF:").place(x= 50, y= 170)
        tk.Label(self.frame, text=self.user.getCep()).place(x= 90, y= 170)

        self.users_dropdown_label = tk.Label(self.frame, text="Grupos:", background="white")
        self.users_dropdown_label.place(x=170, y=90)

        self.users_dropdown = tk.OptionMenu(self.frame, tk.StringVar(self.frame).set("Escolher") , None,*self.user.groups)
        self.users_dropdown.place(x=230, y=90)

        self.users_button_dropdown = tk.Button(self.frame, background="#FFFFFF",text="Escolha um user", command=self.choose_group)
        self.users_button_dropdown.place(x=230, y=125)

        self.groups_dropdown_label = tk.Label(self.frame, text="Usuários:", background="white")
        self.groups_dropdown_label.place(x=170, y=165)

        self.click = tk.StringVar(self.frame)
        self.click.set("Escolher")
        self.groups_dropdown = tk.OptionMenu(self.frame, self.click , None,*self.user.groups)
        self.groups_dropdown.place(x=230, y=165)

        self.groups_button_dropdown = tk.Button(self.frame, background="#FFFFFF",text="Escolha o grupo", command=self.choose_group)
        self.groups_button_dropdown.place(x=230, y=200)

        self.frame.mainloop()

    def choose_group(self):
        Chat(self.user, self.groups_dropdown.get())


    def change_dropdown_label(self):
        self.dropdown_label.config(text = self.clicked.get())



class Chat(tk.Tk): 
    def __init__(self, user: ClientUser, chatName):
        super().__init__()
        self.configure(bg= "lightgray")
        self.geometry("400x650")
        self.user = user

        self.chat_label = tk.Label(self, text = "Chat:", bg="lightgray")
        self.chat_label.config(font=("Arial", 12))
        self.chat_label.pack(padx=20, pady=5)
        
        self.text_area = tkinter.scrolledtext.ScrolledText(self)
        self.text_area.pack(padx=20, pady=5)
        self.text_area.config(state='disabled')

        self.msg_label = tk.Label(self, text="Message:", bg="lightgray")
        self.msg_label.config(font=("Arial", 12))
        self.msg_label.pack(padx=20, pady=5)

        self.input_area = tk.Text(self, height=3)
        self.input_area.pack(padx=20, pady=5)

        self.send_button = tk.Button(self, text = "Send", command=self.write)
        self.send_button.config(font=("Arial", 12))
        self.send_button.pack(padx=20, pady=5)


        self.protocol("WM_DELETE_WINDOW", self.stop)
        self.mainloop()


    def connectToGroup(self, chatName):
        # MAYBE TODO: end this
        self.user.acceptInGroup(chatName)
        res = self.user.sockUser.recv(1024).encode("utf-32")


    def write(self):
        message = f"{self.user.getName()}: {self.input_area.get('1.0', 'end')}"
        self.user.sockUser.send(message.encode("utf-32"))
        self.input_area.delete('1.0', 'end')
    def stop(self):
        self.destroy()

    def receive(self):
        while True:
            try:
                message = self.user.sockUser.recv(1024)
                self.text_area.config(state="normal")
                self.text_area.insert('end', message)
                self.text_area.yview('end')
                self.text_area.config(state= "disabled")
            except ConnectionAbortedError: 
                break
            except:
                print("Error")
                self.user.sockUser.close()
                break

Start()