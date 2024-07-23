import tkinter as tk
import tkinter.scrolledtext
import socket 
from ClientUser import ClientUser

HOST = "127.0.0.1"
PORT = 3300

class Start(tk.Tk):
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
        self.passw_input = tk.Entry(self.frame, width=25, bg="#D3D3D3")
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
            print("usiduaisudbia")
            message = f"0|{email}|{name}|{passw}|{cep}"
            self.user = ClientUser(name, email, passw, cep, self.socket)

            self.socket.send(message.encode('utf-32'))
            Chat(self.user)


    def login(self): 
         # definitions of the client socket


        self.sockUser = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # socket definitions done
        # this is the first connection so we need to
        # sign up this big person

        self.sockUser.connect(socket.gethostbyname(), PORT)

        mensagem = "0|" + _email + "|" + _name + "|" + _passw + "|" + _cep + "|"

        self.sockUser.send(mensagem)

        # A gente tem q fazer close aqui né?

        self.sockUser.close()


class Chat(tk.Tk): 
    def __init__(self, user):
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

    def write(self):
        message = f"{self.user.getName()}: {self.input_area.get('1.0', 'end')}"
        self.user.sockUser.send(message.encode("utf-32"))
        self.input_area.delete('1.0', 'end')
    def stop(self):
        self.destroy()
        self.sock.close()

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