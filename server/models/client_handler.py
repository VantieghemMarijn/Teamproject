import logging
import threading
from .ArtistRepository import ArtistRepository
from .repositories.DataRepositoryV2 import DataRepository
import jsonpickle
import pickle

# Class to handle all requests a client makes to the server

class ClientHandler(threading.Thread):

    def __init__(self, socketclient, server_message_queue, dataset):
        threading.Thread.__init__(self)
        self.socket_to_client = socketclient
        self.ArtistRepository = ArtistRepository(dataset)
        self.server_message_queue = server_message_queue
        self.io_stream_client = None

    
    # Main thread function
    def run(self):
        username = ''
        self.io_stream_client = self.socket_to_client.makefile(mode='rw')
        logging.info("CLH - started & waiting...")

        # While loop to constantly listen to socket, if client made a request execute function. If close = end thread
        commando = self.io_stream_client.readline().rstrip('\n')
        while commando != "CLOSE":
            logging.info(commando)
            logging.info("CLH - Something came in")

            # Extract all params from the messsage
            message = commando.split(';')
            logging.info(message)

            username = message[0]
            query_number = message[1]
            query_param = message[2]

            # Send message to server moderator of new request
            self.server_message_queue.put(f"New request from user {username} for query {query_number} with param {query_param}")

            logging.debug(f"CLH - Username: {username}")
            logging.debug(f"CLH - Query number: {query_number}")
            logging.debug(f"CLH - Query param: {query_param}")

            # If U0 = new login
            if query_number=="U0":#request login
                query_param = query_param.split('|')

                check=DataRepository.read_client(query_param[0])

                print(check,flush=True)

                try:

                    if(check["clientnick"]==query_param[1]):
                        DataRepository.add_active_client(query_param[0])
                        self.io_stream_client.write("succes\n")

                        self.server_message_queue.put(f'User {username} succefully logged in')
                    else:
                        logging.info("wrong loggin")
                        self.io_stream_client.write("failed\n")
                        self.server_message_queue.put(f'Error when loging in user {username}')

                    self.io_stream_client.flush()

                except Exception as ex:
                    self.io_stream_client.write(f"{ex}\n")
                    self.io_stream_client.flush()
                    logging.error(ex)

            # If U0 = new register
            elif query_number=="U1":
                try:
                    query_param = query_param.split('|')
                    DataRepository.create_client(query_param[0],query_param[1],query_param[2])
                    self.io_stream_client.write("succes\n")
                    self.io_stream_client.flush()

                    self.server_message_queue.put(f'User {username} succefully registered')

                except Exception as ex:
                    self.io_stream_client.write(f"{ex}\n")
                    self.io_stream_client.flush()
                    logging.error(ex)

                    self.server_message_queue.put(f'Error when registring user {username}')  
            else:
                try:

                    # Execute query with correct param & number
                    DataRepository.add_query(username, query_number, query_param)
                    response_type, data, header = self.ArtistRepository.execute_query(query_number, query_param)

                    # Serialise data to send to the socket
                    json_pickle = jsonpickle.encode(data)
                    logging.debug(json_pickle)
                    
                    self.io_stream_client.write(f"{response_type};{json_pickle};{header}\n")
                    self.io_stream_client.flush()
                except Exception as ex: 
                    
                    # If request wasnt found, give error
                    self.io_stream_client.write(f"moderator;'404 not found'\n")
                    self.io_stream_client.flush()
                    logging.error(ex)

                    self.server_message_queue.put(f'Error when executing query') 
                    
            # Wait for new command
            commando = self.io_stream_client.readline().rstrip('\n')

        DataRepository.remove_active_client(username)
        logging.debug(f"CLH - Connection closed...")
        #self.stop()
        self.socket_to_client.close()
    
    def send_message(self, message):
        self.io_stream_client.write(f"moderator;{message}\n")
        self.io_stream_client.flush()
