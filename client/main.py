import tkinter as tk
import socket 

HOST = "::1"
PORT = 3300

class Client(tk.Tk):
    def __init__(self):
        super().__init__()
        
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
        self.email_input = tk.Entry(self.frame, width=25, bg="#D3D3D3")
        self.email_input.place(x=150, y=210)
        self.cep = tk.Label(self.frame, text= "CEP", bg="gray")
        self.cep.place(x=80, y= 240)
        self.cep_input = tk.Entry(self.frame, width=20, bg="#D3D3D3")
        self.cep_input.place(x=150, y=240)

        self.submit = tk.Button(self.frame, text="Connect", bg="red", relief="solid")
        self.submit.place(x=200, y=275)

        self.mainloop()



Client()