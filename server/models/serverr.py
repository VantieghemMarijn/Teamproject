import logging
import socket
import threading
import pandas as pd

from models.client_handler import ClientHandler

logging.basicConfig(level=logging.INFO)

class SommenServer(threading.Thread):

    # Init function
    def __init__(self, host, port, messages_queue):
        threading.Thread.__init__(self, name="Thread-Server")
        self.__is_connected = False
        self.host = host
        self.port = port              #server NIET onmiddellijk initialiseren (via GUI)
        self.messages_queue = messages_queue
        # Read in database once here so that not all clients have to do it
        # !!!! Path is absolute because of github errors, should be changed !!!!
        self.dataset = pd.read_csv('/Users/woutdemeyere/Documents/MCT/Advanced Programming & Maths/ProgrammingProject/server/models/artists.csv',
                                    dtype=str)

    @property
    def is_connected(self):
        return self.__is_connected


    def init_server(self):
        self.serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serversocket.bind((self.host, self.port))
        self.serversocket.listen(5)
        self.__is_connected = True
        self.print_bericht_gui_server("SERVER STARTED")
        self.live_connections = []


    def close_server_socket(self):
        self.serversocket.close()

    # When thread is created, make a new clienthandler instance for the new client
    def run(self):
        number_received_message = 0
        try:
            while True:
                self.print_bericht_gui_server("waiting for a new client...")

                # establish a connection
                socket_to_client, addr = self.serversocket.accept()
                self.print_bericht_gui_server(f"Got a connection from {addr}")
                clh = ClientHandler(socket_to_client, self.messages_queue, self.dataset)
                clh.start()

                self.live_connections.append(clh)
                self.print_bericht_gui_server(f"Current Thread count: {threading.active_count()}.")

        except Exception as ex:
            self.print_bericht_gui_server(ex)
            self.print_bericht_gui_server("Serversocket afgesloten")


    def print_bericht_gui_server(self, message):
        self.messages_queue.put(f"Server:> {message}")
    
    # Loop through all connections, if live send message
    def send_message_to_clients(self, message):
        for clh in self.live_connections:
            if clh.is_alive():
                clh.send_message(message)
            else:
                self.live_connections.remove(clh)