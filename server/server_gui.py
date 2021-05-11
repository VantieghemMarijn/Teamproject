# https://pythonprogramming.net/python-3-tkinter-basics-tutorial/
import logging
import socket
from queue import Queue
from threading import Thread
from tkinter import *

from models.repositories.DataRepositoryV2 import DataRepository
from models.serverr import SommenServer

# --- Main GUI window where the moderator can see all incoming requests and query the client database


class ServerWindow(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.init_window()
        self.init_messages_queue()
        self.init_server()
        

    # Creation of init_window
    def init_window(self):
        # changing the title of our master widget
        self.master.title("Server")

        # allowing the widget to take the full space of the root window
        self.pack(fill=BOTH, expand=1)

        Label(self, text="Log-berichten server:").grid(row=0)
        self.scrollbar = Scrollbar(self, orient=VERTICAL)
        self.lstnumbers = Listbox(self, yscrollcommand=self.scrollbar.set, width=60)
        self.scrollbar.config(command=self.lstnumbers.yview)

        self.lstnumbers.grid(row=1, column=0, columnspan=2,  sticky=N + S + E + W, padx=(5, 5), pady =(5,5))
        self.scrollbar.grid(row=1, column=2, sticky=N + S)

        self.message_to_client = Entry(self, width=5)
        self.message_to_client.grid(row=2, column=0,  sticky=E + W, padx=(5, 5), pady =(5,5))

        Button(self,command=self.send_message_to_clients,text="Send msg to clients",width=5).grid(row=2,column=1, sticky=E+W,padx=(5, 5), pady =(5,5))

        self.client_info = Entry(self, width=5)
        self.client_info.grid(row=3, column=0,  sticky=E + W, padx=(5, 5), pady =(5,5))

        Button(self,command=self.get_client_info,text="Get client info",width=5).grid(row=3,column=1, sticky=E+W,padx=(5, 5), pady =(5,5))


        self.btn_clienttext = StringVar()
        self.btn_clienttext.set("See active clients")
        self.buttonClients = Button(self, textvariable=self.btn_clienttext, command=self.get_users)
        self.buttonClients.grid(row=4, column=0, pady=(5, 5), padx=(5, 5), sticky=N + S + E + W)

        self.btn_clienttext = StringVar()
        self.btn_clienttext.set("Most popular queries")
        self.buttonClients = Button(self, textvariable=self.btn_clienttext, command=self.get_most_popular)
        self.buttonClients.grid(row=4, column=1, pady=(5, 5), padx=(5, 5), sticky=N + S + E + W)


        self.btn_text = StringVar()
        self.btn_text.set("Start server")
        self.buttonServer = Button(self, textvariable=self.btn_text, command=self.start_stop_server)
        self.buttonServer.grid(row=5, column=0, columnspan=2, pady=(5, 5), padx=(5, 5), sticky=N + S + E + W)

        Grid.rowconfigure(self, 6, weight=1)
        Grid.columnconfigure(self, 2, weight=1)

    def init_server(self):
        # server - init
        self.server = SommenServer(socket.gethostname(), 9999, self.messages_queue)

    # Function to start and stop the serverv
    def start_stop_server(self):
        if self.server.is_connected == True:
            self.server.close_server_socket()
            self.server.send_message_to_clients("Server has stoped!")
            self.btn_text.set("Start server")
        else:
            self.server.init_server()
            self.server.start()             #thread!
            self.btn_text.set("Stop server")

    # Function to close it all down
    def afsluiten_server(self):
        if self.server != None:
            self.server.close_server_socket()
            self.messages_queue.put("CLOSE_SERVER")
    
    # Function to get queries per user
    def get_client_info(self):
        data=DataRepository.read_querys_per_client(self.client_info.get())

        if(len(data)>0):
            self.lstnumbers.insert(END, f"> Queries for user {self.client_info.get()}")

            for i in data:
                self.lstnumbers.insert(END, f"> {i['queryname']}: {i['queryparam']}")
        else:
            self.lstnumbers.insert(END, f"User has no queries")
    
    # Function to get all active users
    def get_users(self):
        data=DataRepository.read_active_clients()

        if(len(data)>0):
            users=[]
            for i in data:
                users.append(i["clientname"])
            self.lstnumbers.insert(END, f"active users: "+" ".join(users))
        else:
            self.lstnumbers.insert(END, f"no active users!")

    # Function to get most popular queries
    def get_most_popular(self):
        data=DataRepository.get_querys()

        if(len(data)>0):
            self.lstnumbers.insert(END, f"> Most popular queries")

            for i in data:
                print(i)
                self.lstnumbers.insert(END, f'> {i["queryname"]} count: {i["count(queryname)"]}')
        else:
            self.lstnumbers.insert(END, f"no active users!")


    # QUEUE
    def init_messages_queue(self):
        self.messages_queue = Queue()
        t = Thread(target=self.print_messsages_from_queue, name="Thread-queue")
        t.start()

    # Print messages stored in the queue
    def print_messsages_from_queue(self):
        message = self.messages_queue.get()
        while not "CLOSE_SERVER" in message:
            self.lstnumbers.insert(END, message)
            self.messages_queue.task_done()
            message = self.messages_queue.get()
    
    # Function to send messages to all clients
    def send_message_to_clients(self):
        self.server.send_message_to_clients(self.message_to_client.get())

    def close_connection(self):
        self.afsluiten_server()
        self.master.destroy()


    def __del__(self):
        self.close_connection()

if __name__ == '__main__':
    root = Tk()
    root.geometry("550x350")
    app = ServerWindow(root)
    root.mainloop()

