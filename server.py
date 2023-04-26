import socket
import threading


# The Code for the server that is used to connect the clients
# (COPY of this code is deployed on EC2 instance at ip 3.17.4.161)
# This Class just used for testing purposes
class Server:
    def __init__(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind(('localhost', 8000))
        self.server_socket.listen(1)
        self.clients = {}
        print('Server started, waiting for clients...')

    def get_game_status(self, client_socket):
        # Getting the value for the game id
        gameId = None
        while not gameId:
            gameIdbyte = client_socket.recv(1024)
            try:
                gameId = gameIdbyte.decode('utf-8')
            except UnicodeDecodeError:
                # Remove the invalid bytes
                cleaned_bytes = gameIdbyte.translate(None, b'\x80')
                # Decode with error handling
                gameId = cleaned_bytes.decode('utf-8', 'replace')
            # gameId = gameIdbyte.decode()
        print(gameId)
            
        print("recieved game id")
        while True:
            if gameId in self.clients:
                self.clients[gameId].append(client_socket)
            else:
                self.clients[gameId] = [client_socket]

            if len(self.clients[gameId]) == 2:
                client_socket.sendall("ready".encode('utf-8'))
                return True, gameId
            else:
                client_socket.sendall("not".encode('utf-8'))
                return False, gameId

    def handle_client(self, client_socket, client_address, game_id):
        print(f'Client {client_address} connected.')
        while True:
            try:
                data = client_socket.recv(1024)
                if data:
                    print(f'Received data from {client_address}: pickle object')
                    # send data to the other client
                    other_client = self.clients[0] if client_socket == self.clients[1] else self.clients[1]
                    other_client.sendall(data)
                else:
                    print(f'Client {client_address} disconnected.')
                    self.clients.pop(game_id)
                    client_socket.close()
                    return
            except Exception as e:
                print(f'Error handling client {client_address}: {e}')
                if game_id in self.clients:
                    self.clients.pop(game_id)
                client_socket.close()
                return

    def run(self):
        while True:
            client_socket, client_address = self.server_socket.accept()
            start_game, game_id = self.get_game_status(client_socket)
            if start_game:
                print('Starting a game now with id: ' + game_id)
                # start chat between the two clients
                threading.Thread(target=self.handle_client, args=(self.clients[game_id][0], client_address, game_id)).start()
                threading.Thread(target=self.handle_client, args=(self.clients[game_id][1], client_address, game_id)).start()
            if len(self.clients) > 2:
                self.clients = []

if __name__ == '__main__':
    server = Server()
    server.run()