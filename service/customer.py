class Customer:
    def __init__(self, first_name, last_name, birthday):
        self.__first_name = first_name
        self.__last_name = last_name
        self.__birthday = birthday.replace("/", '')
        self.username = f"{self.__first_name}{self.__last_name}{self.__birthday}"

