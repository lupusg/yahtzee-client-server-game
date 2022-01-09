import socket
import pickle
import threading

from src.config.settings import *


class Client:
    def __init__(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((SERVER_NAME, SERVER_PORT))
        self.stop = False

    def check_status(self):
        print('Doriti sa incepeti jocul? (START/STOP): ', end='')

        command = str(input())
        self.__send(command)

        if command == 'START':
            self.__start_game()
        elif command == 'STOP':
            self.client_socket.close()
            return

    def __send(self, data):
        self.client_socket.send(pickle.dumps(data))

    def __receive(self):
        return pickle.loads(self.client_socket.recv(MAX_LENGTH))

    def __receiving(self):
        while True and not self.stop:
            data = self.__receive()
            if data == 'STOP GAME':
                print("Apasati enter pentru a inchide jocul.")
                self.stop = True
                break
            print(data)

    def __sending(self):
        while True and not self.stop:
            command = str(input())
            self.__send(command)

    def __start_game(self):
        table = self.__receive()

        print(table)

        receiving = threading.Thread(target=self.__receiving)
        sending = threading.Thread(target=self.__sending)

        receiving.start()
        sending.start()
