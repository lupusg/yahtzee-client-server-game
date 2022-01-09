import socket
import pickle
import threading

from src.config.settings import *


class Client:
    def __init__(self):
        """
        Initializeaza conexiune cu server-ul.
        """
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((SERVER_NAME, SERVER_PORT))
        self.stop = False

    def check_status(self):
        """
        Metoda care trimite un packet in server pentru a se decide daca jocul incepe sau nu.
        """
        print('Doriti sa incepeti jocul? (START/STOP): ', end='')

        command = str(input())
        self.__send(command)

        if command == 'START':
            self.__start_game()
        elif command == 'STOP':
            self.client_socket.close()
            return

    def __send(self, data):
        """
        Metoda principala pentru a trimite date in server serializate cu pickle.
        """
        self.client_socket.send(pickle.dumps(data))

    def __receive(self):
        """
        Metoda principala care deserializeaza datele primite de la server.
        """
        return pickle.loads(self.client_socket.recv(MAX_LENGTH))

    def __receiving(self):
        """
        Primul fir de executie (Thread 1) care lucreaza incontinuu pentru a primi date de la server.
        Varianta de a avea un thread ne scapa de nevoia sa fim atenti de cate ori trimitem ceva de la server
        sa fie primit in client (mai pe scurt, fara a trebuie sa fim atenti ca numarul metodelor de send sa fie egal
        cu numarul metodelor de receive).
        """
        while True and not self.stop:
            data = self.__receive()
            if data == 'STOP GAME':
                print("Apasati enter pentru a inchide jocul.")
                self.stop = True
                break
            print(data)

    def __sending(self):
        """
        Al doilea fir de executie (Thread 2) care citeste de la tastatura si trimite incontinuu date in server
        citite de la tastatura.
        :return:
        """
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
