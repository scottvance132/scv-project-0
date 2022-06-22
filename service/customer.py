from json import JSONEncoder


class Customer:
    def __init__(self, first_name, last_name, birthday, account_type, account_balance):
        self.__first_name = first_name
        self.__last_name = last_name
        self.__birthday = birthday.replace("/", '')
        self.username = f"{self.__first_name}{self.__last_name}{self.__birthday}"
        self.__account = {"type": account_type, "balance": account_balance}

    def __str__(self):
        return f"Customer Object has the username: {self.username}"

    def get_first_name(self):
        return self.__first_name

    def get_last_name(self):
        return self.__last_name

    def get_birthday(self):
        return self.__birthday

    def get_username(self):
        return self.username

    def get_account_info(self):
        return self.__account

    def set_first_name(self, first_name):
        self.__first_name = first_name
        self.username = f"{self.__first_name}{self.__last_name}{self.__birthday}"

    def set_last_name(self, last_name):
        self.__last_name = last_name
        self.username = f"{self.__first_name}{self.__last_name}{self.__birthday}"

    def set_birthday(self, birthday):
        self.__birthday = birthday
        self.username = f"{self.__first_name}{self.__last_name}{self.__birthday}"

    def set_account_info(self, account_type, account_balance):
        self.__account = {"type": account_type, "balance": account_balance}


class CustomerEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__
