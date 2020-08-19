class Person:
    def __init__(self, first, last, ssid, did):
        self.__first = first;
        self.__last = last;
        self.ssid = ssid;
        self.did = did;

    def full_name(self):
        print(self.__first + " " + self.__last)

    def name(self):
        print(self.__last + ", " + self.__first)

    def __str__(self):
        return f'{self.ssid} - {self.full_name()}'