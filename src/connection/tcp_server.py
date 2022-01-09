import socket
import ast
import pickle

from src.config.settings import *
from src.game.yahtzee import *


class Server:
    def __init__(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((SERVER_NAME, SERVER_PORT))
        self.server_socket.listen(1)
        self.connection_socket, self.addr = self.server_socket.accept()
        self.server_socket.close()

    def check_status(self):
        received_command = self.__receive()

        if received_command == 'START':
            self.__start_game()
        elif received_command == 'STOP':
            self.connection_socket.close()
            return

    def __send(self, data):
        self.connection_socket.send(pickle.dumps(data))

    def __receive(self):
        return pickle.loads(self.connection_socket.recv(MAX_LENGTH))

    def __packet_to_list(self, packet):
        packet = str(packet)
        packet = packet.split()
        print(len(packet))
        while len(packet) != 2:
            self.__send('Comanda introdusa nu este corecta.\n'
                        'Asigurati-va ca elementele din lista sunt introduse fara spatii.\n'
                        'Reintroduceti comanda: ')
            packet = self.__receive()
            packet = str(packet)
            packet = packet.split()
        array = str(packet[1])
        array = ast.literal_eval(array)
        return array

    def __start_game(self):
        game = Game()
        available_rules = ['N1', 'N2', 'N3', 'N4', 'N5', 'N6', 'JOKER', 'TRIPLA', 'CHINTA', 'FULL', 'CAREU', 'YAMS']

        self.__send(game.table.get_formated())

        while game.table.available_rows() > 0:
            self.__send("Tastati comanda dorita: ")
            packet = self.__receive()

            if packet == 'ARUNCA':
                rolls_left = 2

                game.hand.clear()
                game.hand.roll()

                while True:
                    self.__send(str(game.hand.get()) + f' R = {rolls_left}')
                    self.__send("Tastati KEEP [] pentru a rearunca zarurile sau KEEP [N1,N2...] (0<=N<=5).\n"
                                "Apasati [ENTER] pentru a alege coloana in care doriti sa completati punctajul.")

                    packet = self.__receive()

                    if 'KEEP' in packet:
                        rolls_left -= 1

                        array = self.__packet_to_list(packet)
                        game.hand.keep(array)
                    else:
                        self.__send("Alegeti randul in care doriti sa treceti punctajul: ")

                        packet = self.__receive()

                        while (not (packet in available_rules)) or (game.table.table[packet][1] != False):
                            self.__send("Randul introdus nu exista sau a fost deja trecut punctaj in el.\n"
                                        "Reintroduceti randul: ")

                            packet = self.__receive()

                        game.table.table[packet] = (game.table.table_map[packet](game.hand.get()), True)
                        game.table.check_bonus()
                        break

                    if rolls_left == 0:
                        self.__send(str(game.hand.get()) + f' R = {rolls_left}')
                        self.__send("Nu mai sunt aruncari disponbilile. Apasati enter si alegeti randul\n"
                                    "in care doriti sa treceti punctajul.")

                        valid = False
                        while not valid:
                            packet = self.__receive()

                            if packet in available_rules:
                                if not game.table.table[packet][1]:
                                    game.table.table[packet] = (game.table.table_map[packet](game.hand.get()), True)
                                    game.table.check_bonus()
                                    valid = True
                                else:
                                    self.__send("Coloana introdusa nu exista sau a fost deja marcat rezultatul in ea.")

                        if valid:
                            break
            elif packet == 'TABEL':
                self.__send(game.table.get_formated())

        self.__send(f'Felicitari, ati terminat jocul cu un punctaj total de {game.table.table["TOTAL"][0]}')
        self.__send('Doriti sa incepeti alta sesiune? (DA/NU)')
        data = self.__receive()

        if data == 'DA':
            self.__start_game()
        elif data == 'NU':
            self.__send("STOP GAME")
            self.connection_socket.close()
