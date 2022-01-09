import random


class Game:
    def __init__(self):
        self.table = Table()
        self.hand = Hand()


class Table:
    def __init__(self):
        # Tabelul care este format dintr-un tuplu=(scor, daca a fost introdus ceva in el).
        self.table = {
            "N1": (0, False),
            "N2": (0, False),
            "N3": (0, False),
            "N4": (0, False),
            "N5": (0, False),
            "N6": (0, False),
            "BONUS": (0, False),
            "JOKER": (0, False),
            "TRIPLA": (0, False),
            "CHINTA": (0, False),
            "FULL": (0, False),
            "CAREU": (0, False),
            "YAMS": (0, False),
            "TOTAL": (0, False)
        }

        # Function map-ul care ne ajuta sa calculam mai usor regula introdusa.
        self.table_map = {
            "N1": self.n1,
            "N2": self.n2,
            "N3": self.n3,
            "N4": self.n4,
            "N5": self.n5,
            "N6": self.n6,
            "JOKER": self.joker,
            "TRIPLA": self.tripa,
            "CHINTA": self.chinta,
            "FULL": self.full,
            "CAREU": self.careu,
            "YAMS": self.yams,
        }

    def update(self, key, value):
        self.table[key] = value

    def get_value(self, key):
        return self.table[key]

    def n1(self, hand: list):
        points = 0
        for elem in hand:
            if elem == 1:
                points += elem

        self.table['TOTAL'] = (self.table['TOTAL'][0] + points, True)
        return points

    def n2(self, hand: list):
        points = 0
        for elem in hand:
            if elem == 2:
                points += elem

        self.table['TOTAL'] = (self.table['TOTAL'][0] + points, True)
        return points

    def n3(self, hand: list):
        points = 0
        for elem in hand:
            if elem == 3:
                points += elem

        self.table['TOTAL'] = (self.table['TOTAL'][0] + points, True)
        return points

    def n4(self, hand: list):
        points = 0
        for elem in hand:
            if elem == 4:
                points += elem

        self.table['TOTAL'] = (self.table['TOTAL'][0] + points, True)
        return points

    def n5(self, hand: list):
        points = 0
        for elem in hand:
            if elem == 5:
                points += elem

        self.table['TOTAL'] = (self.table['TOTAL'][0] + points, True)
        return points

    def n6(self, hand: list):
        points = 0
        for elem in hand:
            if elem == 6:
                points += elem

        self.table['TOTAL'] = (self.table['TOTAL'][0] + points, True)
        return points

    def joker(self, hand: list):
        self.table['TOTAL'] = (self.table['TOTAL'][0] + sum(hand), True)
        return sum(hand)

    # Multe metode folosesc un vector de frecventa pentru a calcula mai usor rezultatul regulilor, totodata
    # modificand si scorul total.

    def tripa(self, hand: list):
        frequency = [0, 0, 0, 0, 0, 0, 0]

        for elem in hand:
            frequency[elem] += 1

        for elem in frequency:
            if elem >= 3:
                self.table['TOTAL'] = (self.table['TOTAL'][0] + sum(hand), True)
                return sum(hand)
        return 0

    def chinta(self, hand: list):
        hand.sort()
        try:
            if len(hand) >= 5:
                for idx, val in enumerate(hand):
                    if hand[idx + 1] == val + 1 and \
                            hand[idx + 2] == val + 2 and \
                            hand[idx + 3] == val + 3 and \
                            hand[idx + 4] == val + 4:
                        self.table['TOTAL'] = (self.table['TOTAL'][0] + 40, True)
                        return 40
            return 0
        except IndexError:
            pass
        return 0

    def full(self, hand: list):
        frequency = [0, 0, 0, 0, 0, 0, 0]
        tripla = (0, False)
        pair = False

        for elem in hand:
            frequency[elem] += 1

        for elem in frequency:
            if elem >= 3:
                tripla = (elem, True)

            if elem == 2:
                pair = True

        if pair and tripla[1]:
            self.table['TOTAL'] = (self.table['TOTAL'][0] + 30, True)
            return 30
        else:
            return 0

    def careu(self, hand: list):
        frequency = [0, 0, 0, 0, 0, 0, 0]

        for elem in hand:
            frequency[elem] += 1

        for elem in frequency:
            if elem == 4:
                self.table['TOTAL'] = (self.table['TOTAL'][0] + 40, True)
                return 40
        return 0

    def yams(self, hand: list):
        frequency = [0, 0, 0, 0, 0, 0, 0]

        for elem in hand:
            frequency[elem] += 1

        for elem in frequency:
            if elem == 5:
                self.table['TOTAL'] = (self.table['TOTAL'][0] + 50, True)
                return 50
        return 0

    def available_rows(self):
        count = 0

        for key in self.table:
            if not self.table[key][1] and key != 'BONUS':
                count += 1

        return count

    def check_bonus(self):
        if self.table['BONUS'][1] == False:
            points = 0
            for i in range(1, 7):
                points += self.table['N' + str(i)][0]

            if points >= 63:
                self.table['BONUS'] = (50, True)
                self.table['TOTAL'] = (self.table['TOTAL'][0] + 50, True)

    def get(self):
        return self.table

    def get_formated(self):
        """
        Afiseaza tabelul formatat.
        """
        return f"N1 -----> {'' if self.table['N1'][1] == False else self.table['N1'][0]}\n" + \
               f"N2 -----> {'' if self.table['N2'][1] == False else self.table['N2'][0]}\n" + \
               f"N3 -----> {'' if self.table['N3'][1] == False else self.table['N3'][0]}\n" + \
               f"N4 -----> {'' if self.table['N4'][1] == False else self.table['N4'][0]}\n" + \
               f"N5 -----> {'' if self.table['N5'][1] == False else self.table['N5'][0]}\n" + \
               f"N6 -----> {'' if self.table['N6'][1] == False else self.table['N6'][0]}\n" + \
               f"BONUS --> {'' if self.table['BONUS'][1] == False else self.table['BONUS'][0]}\n" + \
               f"JOKER --> {'' if self.table['JOKER'][1] == False else self.table['JOKER'][0]}\n" + \
               f"TRIPLA -> {'' if self.table['TRIPLA'][1] == False else self.table['TRIPLA'][0]}\n" + \
               f"CHINTA -> {'' if self.table['CHINTA'][1] == False else self.table['CHINTA'][0]}\n" + \
               f"FULL ---> {'' if self.table['FULL'][1] == False else self.table['FULL'][0]}\n" + \
               f"CAREU --> {'' if self.table['CAREU'][1] == False else self.table['CAREU'][0]}\n" + \
               f"YAMS ---> {'' if self.table['YAMS'][1] == False else self.table['YAMS'][0]}\n" + \
               f"TOTAL --> {'' if self.table['TOTAL'][1] == False else self.table['TOTAL'][0]}"


class Hand:
    def __init__(self):
        self.__arr = []

    def roll(self):
        for i in range(0, 5):
            self.__arr.append(random.randint(1, 6))
        self.__arr.sort()

    def keep(self, positions):
        for i in range(0, 5):
            if i not in list(positions):
                self.__arr[i] = random.randint(1, 6)

    def clear(self):
        self.__arr = []

    def get(self):
        return self.__arr
