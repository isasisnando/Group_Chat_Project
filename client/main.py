import threading
import tkinter as tk
import tkinter.scrolledtext
import tkinter.filedialog
from tkinter import ttk
from PIL import Image, ImageTk
import socket 
import os
import time
import pygame
from pathlib import Path
from ClientUser import ClientUser


HOST = "127.0.0.1"
PORT = 3300
PRIMARY_COLOR =  "#95ECEC"

CONNECTION_TYPE = {
    "GROUP": "GROUP",
    "CHANNEL": "CHANNEL",
    "NONE": None,
}

DATA_TYPE = {
    "JOIN_NOTIFICATION": "JOIN_NOTIFICATION",
    "LEAVE_NOTIFICATION": "LEAVE_NOTIFICATION",
    "TEXT": "TEXT",
    "IMAGE": "IMAGE",
    "AUDIO": "AUDIO",
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

    def __init__(self, user : ClientUser, mensagem):
        super().__init__()

        self.geometry("450x360")

        self.title("Notificação")
        self.frame = tk.Frame(self, background="green")
        self.frame.pack(fill="both", expand=True)
        self.user = user
        tk.Label(self.frame, text="Notificação: ", background="black", foreground="white").place(relwidth=1, y=75)

        self.aux = self.trataNotif(mensagem)

        if(self.aux[0] == "Convite"):
            
            tk.Label(self.frame, text=f"Você foi convidado para o grupo {self.aux[1]}.", background="black", foreground="white").place(relwidth=1, y=210)
            self.nome = self.user.name
        else:
            tk.Label(self.frame, text=f"{self.aux[2]} pediu para entrar no grupo {self.aux[1]}.", background="black", foreground="white").place(relwidth=1, y=210)
            self.nome = self.aux[2]
        tk.Button(self.frame, text="Aceitar", command=self.posAns, bg="red", relief="raised", height=1, width=10).place(y=320, x=75)
        tk.Button(self.frame,  text="Recusar", bg="red", command=self.negAns, relief="raised", height=1, width=10).place(y=320, x=200)
    
    def posAns(self):
        self.sendAns(True, self.nome, self.aux[1])
        self.destroy()

    def negAns(self):
        self.sendAns(False, self.nome, self.aux[1])
        self.destroy()

    def trataNotif(self, message):

        message = message.split('@')
        print("->"+ message)
        if (message[0] == '3'):

            return("Convite", message[1])
        
        return("InReq", message[1], message[2])
    
    def sendAns(self, acOrNac, who, group):

        if(acOrNac):
            self.user.sockUser.send(f"7|{group}|{who}".encode("utf-32"))
        else:
            self.user.sockUser.send(f"16|{group}|{who}".encode("utf-32"))


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
        self.destroy()
        LogIn()
    def open_signup(self):
        self.destroy()
        SignUp()

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

            self.user.sockUser.send("13|".encode("utf-32"))
            resp = self.user.sockUser.recv(1024).decode("utf-32").split('|')
            IntialPage(self.user, resp)
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
    def __init__(self, user: ClientUser, mensagens = list()):
        super().__init__()

        for notif in mensagens:
            if(notif == ""):
                continue
            Notif(user, notif)
            
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

        self.t_groups_dropdown_label = tk.Label(self.frame, text="Grupos (teste):", background="white")
        self.t_groups_dropdown_label.place(x=170, y=240)

        self.t_groups_click = tk.StringVar(self.frame)
        self.t_groups_click.set("Escolher")
        self.t_groups_dropdown = tk.OptionMenu(self.frame, self.t_groups_click , None, *self.user.takeGroups())
        self.t_groups_dropdown.place(x=230, y=240)

        self.t_groups_button_dropdown = tk.Button(self.frame, background="#FFFFFF",text="Escolher grupo", command=self.choose_t_group)
        self.t_groups_button_dropdown.place(x=230, y=280)

        self.protocol("WM_DELETE_WINDOW", self.stop)

        self.frame.mainloop()

    def choose_group(self):
        # self.destroy()
        # Chat(self.user, self.groups_click.get(), "GROUP")
        NewChat(self, self.frame, self.user, self.groups_click.get(), CONNECTION_TYPE["GROUP"])
    
    def choose_t_group(self):
        self.destroy()
        GroupPerfilScreen(self.user, self.t_groups_click.get())

    def choose_user(self):
        self.destroy()
        PerfilScreen(self.user, self.users_click.get())

    def change_dropdown_label(self):
        self.dropdown_label.config(text = self.clicked.get())

    def create_group(self):
        self.destroy()
        CreateGroup(self.user)

    def stop(self):
        try:
            message = f"{self.user.getName()} has left the chat"
            self.user.sockUser.send(message.encode("utf-32"))
            self.user.closeConection()
            self.user.sockUser.close()
        except Exception as e:
            print(e)
            print("uai")
            self.destroy()

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

class NewChat(tk.Canvas):
    def __init__(self,parent, firstFrame, user: ClientUser,chatName, tipoChat):
        super().__init__()
        self.user = user
        self.destName = chatName
        self.tipoChat = tipoChat
        print(user.sockUser)

        self.running = True
        self.interface_done = False 

        self.window = f"Chat room:"
        
        self.first_frame = firstFrame
        self.first_frame.pack_forget()
        
        self.parent = parent
        # self.parent.bind('<Return>')
        self.parent.protocol("WM_DELETE_WINDOW", self.stop)


        screen_width, screen_height = self.winfo_screenwidth(), self.winfo_screenheight()

        x_co = int((screen_width / 2) - (680 / 2))
        y_co = int((screen_height / 2) - (750 / 2)) - 80
        self.parent.geometry(f"680x750+{x_co}+{y_co}")

        container = tk.Frame(self)
        container.place(x=40, y=120, width=450, height=550)
        self.canvas = tk.Canvas(container, bg=PRIMARY_COLOR)
        self.scrollable_frame = tk.Frame(self.canvas, bg="cyan")

        scrollable_window = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        def configure_scroll_region(e):
            self.canvas.configure(scrollregion=self.canvas.bbox('all'))

        def resize_frame(e):
            self.canvas.itemconfig(scrollable_window, width=e.width)

        self.scrollable_frame.bind("<Configure>", configure_scroll_region)

        scrollbar = ttk.Scrollbar(container, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=scrollbar.set)
        self.yview_moveto(1.0)

        scrollbar.pack(side="right", fill="y")

        self.canvas.bind("<Configure>", resize_frame)
        self.canvas.pack(fill="both", expand=True)

        self.send_button = tk.Button(self, text="Send", font="lucida 11 bold", bg="red", padx=10, relief="solid", bd=2, command=self.write)
        self.send_button.place(x=500, y=680)

        self.file_transfer_button = tk.Button(self, text= "Upload",font="lucida 11 bold", bg="red", padx=10, relief="solid", bd=2, command=self.upload)
        self.file_transfer_button.place(x=350, y=680)

        self.input_area = tk.Text(self, font="lucida 10 bold", width=38, height=2, highlightcolor="cyan", highlightthickness=1)
        self.input_area.place(x=40, y=681)
        self.input_area.focus_set()

        m_frame = tk.Frame(self.scrollable_frame, bg=PRIMARY_COLOR)

        m_label = tk.Label(m_frame, wraplength=250, text=f"{self.destName} {CONNECTION_TYPE[self.tipoChat]}:",font="lucida 10 bold", bg="red")
        m_label.pack(fill="x")

        m_frame.pack(pady=10, padx=10, fill="x", expand=True, anchor="e")

        self.pack(fill="both", expand=True)

        self.interface_done = True

        if(self.tipoChat == CONNECTION_TYPE["GROUP"]):
            self.connectToGroup()
        else:
            self.connectToUser()

        receiving_thread = threading.Thread(target=self.receive)
        receiving_thread.daemon = True
        receiving_thread.start()

    def unpackMessages(self, message):
        data = dict()
        if not message.strip(): 
            return
        if(message[0] == "*"):
            message = message.split(":")
            filename = str(message[1])
            filesize = int(message[2])
            filedata = self.user.getSingleFile(filename, filesize)
            type_ = None
            if(filename.endswith(".mp3")):
                type_ = DATA_TYPE["AUDIO"]
            else:
                type_ = DATA_TYPE["IMAGE"]
            data_dict = {
                "type": type_,
                "from": message[0][1:],
                "message": filedata
            }
            self.received_message_format(data_dict)
        elif ":" in message:
            message = message.split(":")
            sender = message[0].strip()
            text_data = message[1].strip()
            data_dict = {
                "type": DATA_TYPE["TEXT"],
                "from": sender,
                "message": text_data
            }
            self.received_message_format(data_dict)
        else:
            data_dict = {
                "type": DATA_TYPE["JOIN_NOTIFICATION"],
                "from": "_",
                "message": message
            }
            self.received_message_format(data_dict)

    def connectToUser(self):
        messages = self.user.openConection(CONNECTION_TYPE["CHANNEL"], self.destName)
        for message in messages: 
            self.unpackMessages(message)

    def connectToGroup(self):
        # self.user.acceptInGroup(self.destName)
        messages = self.user.openConection(CONNECTION_TYPE["GROUP"], self.destName)
        for message in messages: 
            self.unpackMessages(message)


    def write(self):
        if (self.tipoChat == CONNECTION_TYPE["GROUP"]):
            self.user.sendMsgGroup(self.destName, self.user.getName(), self.input_area.get('1.0', 'end'))
        elif (self.tipoChat == CONNECTION_TYPE["CHANNEL"]): 
            self.user.sendMsgUser(self.destName, self.user.getName(), self.input_area.get('1.0', 'end'))
    
        self.input_area.delete('1.0', 'end')

    def upload(self):
        filename = tkinter.filedialog.askopenfilename()
        if filename:
            self.user.sendUploadGroup(self.destName, self.user.getName(), filename)

    def stop(self):
        self.running = False
        self.interface_done = False
        self.input_area.delete('1.0', 'end')
        self.parent.destroy()
        self.user.closeConection()
        self.user.sockUser.close()


    def receive(self):
        while self.running:
            try:
                if self.interface_done:
                    message = self.user.sockUser.recv(1024)
                    message = message.decode("utf-32")
                    if ("|" in message):
                        message = message.split("|")
                        for m in message:
                            self.unpackMessages(m)
                    elif not message.strip():
                        continue
                    elif ("joined this chat" in message):
                        data_dict = {
                            "type": DATA_TYPE["JOIN_NOTIFICATION"],
                            "from": "_",
                            "message": message
                        }
                        self.received_message_format(data_dict)
                    elif message[0] =="*":
                        message = message.split(":")
                        filename = "./rec/" + message[1]
                        filesize = int(message[2])
                        sender = message[0][1:]
                        with open(filename, "wb") as file:
                                c = 0
                                while c < filesize:
                                    data = self.user.sockUser.recv(1024)
                                    if not (data):
                                        break
                                    file.write(data)
                                    c += len(data)
                        if(filename.endswith(".mp3")):
                            data_dict = {
                                "type": DATA_TYPE["AUDIO"],
                                "from": sender,
                                "message": filename
                            }
                        else:
                            image = Image.open(filename)
                            image = image.resize((120, 120))
                            data_dict = {
                                "type": DATA_TYPE["IMAGE"],
                                "from": sender,
                                "message": image
                            }
                        self.received_message_format(data_dict)

                    else:
                        message = message.split(":")
                        sender = message[0].strip()
                        text_data = message[1].strip()
                        data_dict = {
                            "type": DATA_TYPE["TEXT"],
                            "from": sender,
                            "message": text_data
                        }
                        self.received_message_format(data_dict)
            except ConnectionAbortedError: 
                break
            except Exception as e:
                print("Receiving error")
                print(e)
                self.user.closeConection()
                break

    def received_message_format(self, data):

        message = data['message']
        from_ = data['from']
        data_type = data['type']

        if (data_type == DATA_TYPE["JOIN_NOTIFICATION"] or data_type == DATA_TYPE["LEAVE_NOTIFICATION"]):
            m_frame = tk.Frame(self.scrollable_frame, bg="cyan")

            m_label = tk.Label(m_frame, wraplength=250, text=message, font="lucida 10 bold", justify="left", bg="cyan")
            m_label.pack()

            m_frame.pack(pady=6, padx=10, fill="x", expand=True, anchor="e")

            self.canvas.yview_moveto(1.0)
        elif (data_type == DATA_TYPE["TEXT"]): 

            m_frame = tk.Frame(self.scrollable_frame, bg=PRIMARY_COLOR)

            m_frame.columnconfigure(1, weight=1)

            m_label = tk.Label(m_frame, wraplength=250,fg="black", bg="#ff7e62", text=message, font="lucida 9 bold", justify="left", anchor="w")
            m_label.grid(row=1, column=1, padx=2, pady=2, sticky="w")

            t_label = tk.Label(m_frame, bg=PRIMARY_COLOR, text=from_, font="lucida 7 bold",justify="left", anchor="w")
            t_label.grid(row=0, column=1, padx=2, sticky="w")

            m_frame.pack(pady=10, padx=10, fill="x", expand=True, anchor="e")

            self.canvas.update_idletasks()
            self.canvas.yview_moveto(1.0)
        elif (data_type == DATA_TYPE["IMAGE"]):
            im = ImageTk.PhotoImage(message)

            m_frame = tk.Frame(self.scrollable_frame, bg=PRIMARY_COLOR)

            m_frame.columnconfigure(1, weight=1)

            i_label = tk.Label(m_frame, bg=PRIMARY_COLOR, image=im)
            i_label.image = im
            i_label.grid(row=1, column=1, padx=2, pady=2, sticky="w")

            t_label = tk.Label(m_frame, bg="#595656",fg="white", text=from_, font="lucida 7 bold", justify="left", anchor="w")
            t_label.grid(row=0, column=1, padx=2, sticky="w")

            m_frame.pack(pady=10, padx=10, fill="x", expand=True, anchor="e")

            self.canvas.update_idletasks()
            self.canvas.yview_moveto(1.0)
        elif (data_type == DATA_TYPE["AUDIO"]):
            pygame.mixer.init()
            self.is_playing = False
            self.btn_text = "TOCAR"
            def play():
                pygame.mixer.music.load(message)
                pygame.mixer.music.play(loops=0)
            def stop():
                pygame.mixer.music.stop()

            def handle_click():
                if (self.is_playing):
                    self.is_playing = False
                    self.btn_text = "PARAR"
                    stop()
                else:
                    self.is_playing = True
                    self.btn_text = "TOCAR"
                    play()

            

            m_frame = tk.Frame(self.scrollable_frame, bg=PRIMARY_COLOR)

            m_frame.columnconfigure(1, weight=1)

            i_label = tk.Button(m_frame,fg="white", font="lucida 7 bold",justify="left", anchor="w", bg="cyan", text=self.btn_text, command=handle_click)
            i_label.grid(row=1, column=1, padx=2, pady=2, sticky="w")

            t_label = tk.Label(m_frame, bg="#595656",fg="white", text=from_, font="lucida 7 bold",
                           justify="left", anchor="w")
            t_label.grid(row=0, column=1, padx=2, sticky="w")

            m_frame.pack(pady=10, padx=10, fill="x", expand=True, anchor="e")

            self.canvas.update_idletasks()
            self.canvas.yview_moveto(1.0)

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

        self.frame.mainloop()
    
    def openChat(self):

        self.user.sockUser.send((f"4|{self.resp[0]}").encode("utf-32"))

        NewChat(self, self.frame, self.user, self.resp[0], CONNECTION_TYPE["CHANNEL"])
        pass

class GroupPerfilScreen(tk.Tk):
    
    def __init__(self, user : ClientUser, groupName : str):
        super().__init__()

        self.geometry("360x300")
        self.title("Informações pessoais")

        self.frame = tk.Frame(self, background= "#95ECEC")
        self.frame.pack(fill="both", expand=True)

        tk.Label(self.frame, text="Informações pessoais").place(relwidth=1, y=24)

        self.user = user
        self.groupName = groupName
        self.user.sockUser.send((f"14|{groupName}").encode("utf-32"))

        self.resp = self.user.sockUser.recv(1024).decode("utf-32")

        self.resp = self.resp.split('|')

        tk.Label(self.frame, text="Nome:", background="#4EABB0",foreground="#006666", font=("Arial", 14)).place(y=100, x=24)
        tk.Label(self.frame, text=self.resp[0], background="#4EABB0",foreground="#006666", font=("Arial", 14)).place(y=100, x=95)
        tk.Label(self.frame, text="Admin:", background="#4EABB0",foreground="#006666", font=("Arial", 14)).place(y=150, x=24)
        tk.Label(self.frame, text=self.resp[1], background="#4EABB0",foreground="#006666", font=("Arial", 14)).place(y=150, x=95)
        if(self.resp[1] != self.user.getName()):
            tk.Button(self.frame,  text="Sair do grupo", command=self.outGroup, bg="red", relief="raised", height=1, width=10).place(y=50, x=260)
            tk.Button(self.frame, text="Pedir pra entrar", bg="red", command=self.askInGroup, relief="raised", height=1, width=10).place(y=250, x=75)
        else:
            tk.Button(self.frame, text="Enviar convite", command=self.abreInviteScreen, bg="red", relief="raised", height=1, width=10).place(y=250, x=75)
        tk.Button(self.frame,  text="Abrir o chat", bg="red", command=self.abreGroup, relief="raised", height=1, width=10).place(y=250, x=200)

        self.frame.mainloop()

    def abreGroup(self):

        nomeGrupo = self.resp[0]
        self.user.sockUser.send(f"15|{nomeGrupo}".encode("utf-32"))
        resp = self.user.sockUser.recv(1024).decode("utf-32")
        if(resp == "voce nao esta no grupo"):

            self.destroy()
            GroupPerfilScreen(self.user, self.groupName)
            ErrorMsg(resp)
            return

        NewChat(self, self.frame, self.user, self.groupName, CONNECTION_TYPE["GROUP"])
    
    def outGroup(self):

        self.user.sockUser.send(f"9|{self.resp[0]}|{self.user.getName()}|".encode("utf-32"))

        resp = self.user.sockUser.recv(1024).decode("utf-32")

        if (resp == f"{self.user.getName()} nao esta no grupo"):

            ErrorMsg(resp)
            return

    def askInGroup(self):

        nomeGrupo = self.resp[0]
        self.user.sockUser.send(f"6|{nomeGrupo}|{self.user.getName()}".encode("utf-32"))

        resp = self.user.sockUser.recv(1024).decode("utf-32")

        if(resp == "ok"):
            return
        
        self.destroy()
        GroupPerfilScreen(self.user, self.groupName)
        ErrorMsg(resp)
        return

    def abreInviteScreen(self):
        self.destroy()
        ConvidarUsuarios(self.user, self.groupName)

class ConvidarUsuarios(tk.Tk):

    def __init__(self, user : ClientUser, nameGrupo : str):

        super().__init__()

        self.user, self.nomeGrupo = user, nameGrupo

        self.geometry("360x300")
        self.title("Convidar usuarios")
        self.frame = tk.Frame(self, background= "#95ECEC")
        self.frame.pack(fill="both", expand=True)

        tk.Label(self.frame, text="Convidar Usuarios").place(relwidth=1, y=24)

        self.users_dropdown_label = tk.Label(self.frame, text="Usuários:", background="white")
        self.users_dropdown_label.place(x=94, y=90)


        self.users_click = tk.StringVar(self.frame)
        self.users_click.set("Escolher")
        self.users_dropdown = tk.OptionMenu(self.frame, self.users_click, None,*self.user.takeUsers())
        self.users_dropdown.place(x=154, y=90)
       
        self.users_button_dropdown = tk.Button(self.frame, background="#FFFFFF",text="Convidar usuário", command=self.sendInvite)
        self.users_button_dropdown.place(x=114, y=125)

        tk.Button(self.frame,  text="Voltar", bg="red", command=self.voltar, relief="raised", height=1, width=10).place(y=260, x=20)
    
    def sendInvite(self):

        who = self.users_click.get()
        mensagem = f"5|{self.nomeGrupo}|{who}"

        self.user.sockUser.send(mensagem.encode("utf-32"))
        resp = self.user.sockUser.recv(1024).decode("utf-32")

        if (resp == "ok"):
            return
        
        self.destroy()
        ConvidarUsuarios(self.user, self.nomeGrupo)
        ErrorMsg(resp)
        return
    
    def voltar(self):
        self.destroy()
        IntialPage(self.user)
Start()