import logging
import socket
from tkinter import *
from tkinter import messagebox
from client_gui import WindowClient
from register_gui import WindowRegister
import functools


# ---- Main login window where user selects to login or register a new acc

class Window(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.init_window()
             
    # Creation of init_window
    def init_window(self):

        # Tkinter UI declarations

        self.master.title("login_screen")
        self.pack(fill=BOTH, expand=1)

        Label(self, text="username:").grid(row=0)
        self.entry_username = Entry(self, width=40)
        self.entry_username.grid(row=1, column=0, sticky=E + W, padx=(5, 5), pady =(5,5))

        Label(self, text="nickname:", pady=10).grid(row=2)
        self.entry_nick = Entry(self, width=40)
        self.entry_nick.grid(row=3, column=0, sticky=E + W, padx=(10, 10), pady =(5,0))


        Button(self,command=self.makeConnnectionWithServer,text="login",width=10).grid(row=4,column=0,sticky=S,pady=(20,0))
        Button(self,command=self.register,text="register",width=10).grid(row=5,column=0,sticky=S,pady=(20,0))

        Grid.rowconfigure(self, 6, weight=1)
        Grid.columnconfigure(self, 1, weight=1)

    
    def __del__(self):
        self.close_connection()

    # Connect to server
    def makeConnnectionWithServer(self):
        try:
            logging.info("Making connection with server...")
            # get local machine name
            host = socket.gethostname()
            port = 9999
            self.socket_to_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # connection to hostname on the port.
            self.socket_to_server.connect((host, port))
            self.my_writer_obj = self.socket_to_server.makefile(mode='rw')
            logging.info("Open connection with server succesfully")

            #   If connection was made, login user
            self.requestlogin()
        except Exception as ex:
            logging.error(f"Foutmelding: {ex}")

    

    def close_connection(self):
        try:
            logging.info("Close connection with server...")
            self.my_writer_obj.write("CLOSE\n")
            self.my_writer_obj.flush()
            self.socket_to_server.close()
        except Exception as ex:
            logging.error(f"Foutmelding: {ex}")
            messagebox.showinfo("Sommen", "Something has gone wrong...")
    
    def requestlogin(self):
        try:
            logging.info("loggin in")

            username=self.entry_username.get()
            nick=self.entry_nick.get()
            email=''

            user=f"{username}|{nick}|{email}"
            logging.info(f"{username},{nick},{email}")
            
            # Write the users info to the server
            self.my_writer_obj.write(f"{username};{'U0'};{user}\n")
            self.my_writer_obj.flush()

            message=self.my_writer_obj.readline().rstrip('\n')
            
            print(message)

            #If user is logged in SUCCES
            if message=="succes":
                self.master.destroy()
                #Create client GUI
                client = WindowClient.create_client(username, self.socket_to_server, self.my_writer_obj)
            else:
                #Else print fout, maybe a message window
                print("fout")

        except Exception as ex:
            print(ex)

    #Create new window if user wants to register
    def register(self):
        logging.info("to register screen")
        self.master.destroy()
        client = WindowRegister.create_client()

logging.basicConfig(level=logging.INFO)

root = Tk()
root.geometry("400x400")
app = Window(root)
root.mainloop()
