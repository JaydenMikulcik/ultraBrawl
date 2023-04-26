import socket
import pickle


# Object Used to test serialization with pickle
class MyCustomObject:
    def __init__(self, x, y):
        self.x = x
        self.y = y



# Client Used in the game to communicate with the server
class Client:
    def __init__(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # For OHIO server
        self.client_socket.connect(('3.17.4.161', 5000))
        self.client_socket.settimeout(0.2)
        # self.client_socket.connect(('localhost', 8000))
        #threading.Thread(target=self.receive_data).start()
        #self.send_data()

    def create_game(self, gameId):
        """
        Method to create a new game
        instance in the server game 
        dictionary
        Param gameId: The id that will be used to create game
        """
        notCreated = True
        while True:
            try:
                # create a custom object to send
                if notCreated:
                    self.client_socket.sendall(gameId)
                    notCreated = False
                bothPlayers = self.client_socket.recv(1024)
                if bothPlayers:
                    return True
                else:
                    return False
            except Exception as e:
                print(f'Error sending data: {e}')
                self.client_socket.close()
                return
            
    def join_game(self, gameId):
        """
        Method to create a join a existing game
        instance in the server game 
        dictionary
        Param gameId: The id that will be used to create game
        """
        notCreated = True
        try:
            # create a custom object to send
            if notCreated:
                self.client_socket.sendall(gameId)
                notCreated = False
            try:
                bothPlayers = self.client_socket.recv(1024).decode()
                if bothPlayers != "not":
                    return True
                return False
            except socket.timeout:
                return False
        except Exception as e:
            return False

    def receive_data(self):
        """
        This is used to recieve the player from the 
        other connected computer
        """
        try:
            data = self.client_socket.recv(2000)
            if data:
                # Recieve the Character Object
                my_custom_obj = pickle.loads(data)
                print('Keys Recieved')
                return my_custom_obj
                
            else:
                print('No Keys Recieved')
                return None
        except Exception as e:
            print(f'Error receiving data: {e}')
            return None

    def send_data(self, playerObj):
        """
        Method to send data to the server and the 
        other player
        Param data: The data of your player
        """
        try:

            # serialize the custom object using pickle
            data = pickle.dumps(playerObj)
            self.client_socket.sendall(data)
        except Exception as e:
            print(f'Error sending data: {e}')



# Client with While loop in sending and recieving data
class ClientWhile:
    def __init__(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect(('3.17.4.161', 5000))
        print("done")
        #threading.Thread(target=self.receive_data).start()
        #self.send_data()

    def receive_data(self):
        while True:
            try:
                data = self.client_socket.recv(1024)
                if data:

                    # Recieve the Character Object
                    # my_custom_obj = pickle.loads(data)
                    print(f'Received custom object: {data.decode()}')
                    
                else:
                    print('Disconnected from server.')
                    self.client_socket.close()
                    return
            except Exception as e:
                print(f'Error receiving data: {e}')
                self.client_socket.close()
                return

    def send_data(self, data):
        while True:
            try:
                # data = input('Enter data to send to server: ')

                # create a custom object to send
                my_custom_obj = MyCustomObject(10, 20)

                # serialize the custom object using pickle
                data = pickle.dumps(my_custom_obj)
                self.client_socket.sendall(data.encode())


            except Exception as e:
                print(f'Error sending data: {e}')
                self.client_socket.close()
                return

if __name__ == '__main__':
    which = input("enter 1 send 2 recieve")
    if which == "1":
        client = Client()
        client.send_data("401")
        client = Client()
        client.send_data("401")
    else:
        client = ClientWhile()
        client.receive_data()