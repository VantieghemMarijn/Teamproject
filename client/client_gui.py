import logging
import socket
from tkinter import *
from tkinter import messagebox
from tkinter import scrolledtext
from threading import Thread
from functools import partial
import jsonpickle
import json
from models.messagehandler import MessageHandler
from queue import Queue

import numpy as np
import seaborn as sns
import pandas as pd

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


# --- Main Client window where the user can query the server and receive messages

class WindowClient(Frame):
    def __init__(self, master=None,  user="", socket_to_server=None, write_obj=None):
        Frame.__init__(self, master)
        self.master = master
        self.username=user
        self.password=None
        self.socket_to_server = socket_to_server
        self.my_writer_obj = write_obj
        print(self.socket_to_server)
        #self.makeConnnectionWithServer()
        
        self.init_window()

        # Queue to store messages from server
        self.queue = Queue()

        # Thread to read messages from server
        receiver_thread = MessageHandler("Message-handler", self.my_writer_obj, self.queue)
        receiver_thread.start()

        self.monitor()       
    
    # Creation of init_window
    def init_window(self):
        # Tkinter UI declarations

        self.master.title(f"client: {self.username}")

        Label(self, text="Berichten van moderator:", fg='black').grid(row=6, column=1, padx=(5, 5))
        self.mod_messages = Listbox(self, height = 3)
        self.mod_messages.grid(row=7, column=1, sticky=N + S + E + W, padx=(5, 5), pady =(0,5))

        self.server_reply_header = StringVar(self)
        self.server_reply_header.set("Placeholderdebolder")

        Label(self, text=self.server_reply_header, fg='black').grid(row=0, column=1, padx=(5, 5))
        self.server_reply_box = Text(self, width = 20, height = 20, font = ("Times New Roman", 15), fg='black', bg='grey', bd=4)
        self.server_reply_box.grid(row=0, rowspan=8, column=2, sticky=E + W, padx=(5, 5), pady =(5,5))
        self.server_reply_box.configure(state ='disabled')

        self.artist_name = Entry(self, width=20)
        self.artist_counrty = Entry(self, width=20)
        self.artist_genre = Entry(self, width=20)

        self.artist_name.grid(row=0, column=0, sticky=E + W, padx=(5, 5), pady =(5,5))
        self.artist_counrty.grid(row=1, column=0, sticky=E + W, padx=(5, 5), pady =(5,0))
        self.artist_genre.grid(row=2, column=0, sticky=E + W, padx=(5, 5), pady =(5,0))

        
        plt.tight_layout()
        
        self.fig = Figure(figsize=(3, 3))
        self.a = self.fig.subplots()

        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        #self.canvas.grid(row=0, rowspan=6, column=3, sticky=E + W, padx=(5, 5), pady =(5,5))
        self.canvas.get_tk_widget().grid(row=0, rowspan=8, column=3, sticky=E + W, padx=(5, 5), pady =(5,5))

        Button(self,command= lambda: self.sendmessage("Q0", self.artist_name.get()),text="Search artist info by name",width=30).grid(row=0,column=1,sticky=E+W,padx=(5, 5), pady =(5,5))
        Button(self,command= lambda: self.sendmessage("Q1", self.artist_counrty.get()),text="Search artist by country",width=30).grid(row=1,column=1,sticky=E+W,padx=(5, 5), pady =(5,5))
        Button(self,command= lambda: self.sendmessage("Q2", self.artist_genre.get()),text="Search top artists by genre",width=30).grid(row=2,column=1,sticky=E+W,padx=(5, 5), pady =(5,5))
        Button(self,command= lambda: self.sendmessage("Q3", "no param"),text="Give a histogram of most popular genres",width=60).grid(row=4,column=0,columnspan = 2,sticky=E+W,padx=(5, 5), pady =(5,5))
        Button(self,command= lambda: self.sendmessage("Q4", "no param"),text="Give a histogram of most popular countries",width=10).grid(row=5,column=0,columnspan = 2,sticky=E+W,padx=(5, 5), pady =(5,5))
        Button(self,command= lambda: self.close_connection,text="close connection",width=20).grid(row=6,column=0,sticky=E+S+W,pady=(20,0),padx=(10,0))

        Grid.rowconfigure(self, 8, weight=1)
        Grid.columnconfigure(self, 3, weight=1)

        self.pack(fill=BOTH, expand=1)

        
    
    def __del__(self):
        self.close_connection()

    # When client stops, let the server know 
    def close_connection(self):
        try:
            logging.info("Close connection with server...")
            self.my_writer_obj.write("CLOSE\n")
            self.my_writer_obj.flush()
            self.socket_to_server.close()
        except Exception as ex:
            print("testerror")
        
        self.master.destroy()
    
    # Send a message to the server with query number & param
    def sendmessage(self, query_number, query_param):
        try:
            logging.info(f"Sending {query_number} with param {query_param}")
            self.my_writer_obj.write(f"{self.username};{query_number};{query_param}\n")
            self.my_writer_obj.flush()
        
        except Exception as ex:
            print(ex)

    # Function to create the client itself
    def create_client(username, socket_server, write_obj):
        root = Tk()
        root.geometry("1000x500")
        app = WindowClient(root, username, socket_server, write_obj)
        root.mainloop()

    # Write new data to the display list
    def write_to_list(self, data, header):
        self.server_reply_header.set(header)
        self.server_reply_box.configure(state ='normal')
        self.server_reply_box.delete('1.0', END)
        for index, text in enumerate(data):
            self.server_reply_box.insert(INSERT, f'{index+1}. {text}\n')
        self.server_reply_box.configure(state ='disabled')
    
    # Plot a new graph if user requested
    def plot_data(self, data, header):

        self.a.clear()

        my_df = pd.DataFrame(data)
        sns.barplot(x=0, y=1, data=my_df, ax=self.a)

        self.a.set(yticks=[], title=header)
        self.a.set_xticklabels(self.a.get_xticklabels(), rotation=40, ha="right")
        self.canvas.figure = self.fig
        self.canvas.draw_idle()

    # Monitor the Queue every 100ms to see if server has sent a new message
    def monitor(self):

        if self.queue.empty():
            pass
        else:
            message = self.queue.get_nowait()

            if message[0] != 'CLOSE':

                # If the message came from the moderator, print it to the log window
                if message[0] == 'moderator':
                    print(self.mod_messages)
                    self.mod_messages.insert(END, f"> Moderator: {message[1]}")
                    logging.info(f"> Moderator: {message[1]}")

                # If the message is for the list window
                elif message[0] == 'text_response':

                    pickle_data = jsonpickle.decode(message[1])
                    clean_data = json.loads(pickle_data)      
                    self.write_to_list(clean_data, message[2])
                    logging.info(f"Answer server: {clean_data}")

                # If the message is a graph send it to the plotter
                elif message[0] == 'plot_response':

                    pickle_data = jsonpickle.decode(message[1])    
                    self.plot_data(pickle_data, message[2])
        
        self.after(100, self.monitor)

if __name__ == '__main__':
    client = WindowClient.create_client("test", "tester")
    client = mainloop()