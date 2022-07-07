from dao.customer_dao import CustomerDao
from dao.acc_dao import AccDao
from exception.acc_not_found import AccountNotFoundError
from exception.cus_not_found import CustomerNotFoundError
from exception.invalid_acc_balance import InvalidAccountBalanceError
from exception.invalid_acc_type import InvalidAccountTypeError
from exception.invalid_param import InvalidParameterError
from utility.contains_letter import containsLetter
from utility.contains_num import containsNumber
from utility.contains_space import containsSpace
from utility.contains_spec_char import containsSpecChar


class AccService:

    def __init__(self):
        # self.test = None
        self.acc_dao = AccDao()
        self.customer_dao = CustomerDao()

    def get_all_accounts(self):
        list_of_accounts = self.acc_dao.get_all_accounts()
        return list(map(lambda a: a.to_dict(), list_of_accounts))

    def get_all_accounts_by_username(self, username, query_1, query_2):
        if self.customer_dao.get_customer_by_username(username) is None:
            raise CustomerNotFoundError(f"Customer with username {username} was not found")

        if query_1 is None and query_2 is None:
            return list(map(lambda a: a.to_dict(), self.acc_dao.get_all_accounts_by_username(username)))

        elif query_1 is not None and query_2 is not None:
            return list(map(lambda a: a.to_dict(), self.acc_dao.get_all_accounts_between_by_username(username,
                                                                                                     query_1, query_2)))

        elif query_1 is not None:
            return list(map(lambda a: a.to_dict(), self.acc_dao.get_all_accounts_greater_by_username(username,
                                                                                                     query_1)))

        elif query_2 is not None:
            return list(map(lambda a: a.to_dict(), self.acc_dao.get_all_accounts_less_by_username(username,
                                                                                                  query_2)))

        else:
            return []

    def get_account_by_username_and_account_id(self, username, account_id):
        if self.customer_dao.get_customer_by_username(username) is None:
            raise CustomerNotFoundError(f"Customer with username {username} was not found")
        elif self.acc_dao.get_account_by_username_and_account_id(username, account_id) is None:
            raise AccountNotFoundError(f"Customer with username {username} does not have account with id {account_id}")

        return self.acc_dao.get_account_by_username_and_account_id(username, account_id).to_dict()

    def add_account_for_customer_by_username(self, account_obj):
        valid_acc_type = ["savings", "checking", "investment", "retirement"]
        if self.customer_dao.get_customer_by_username(account_obj.username) is None:
            raise CustomerNotFoundError(f"Customer with username {account_obj.username} was not found")
        elif containsSpace(account_obj.type):
            raise InvalidParameterError(f"Invalid input (space) for the new account! Please try again")
        elif containsNumber(account_obj.type):
            raise InvalidParameterError(f"Invalid input (number) for the new account! Please try again")
        elif containsSpecChar(account_obj.type):
            raise InvalidParameterError(f"Invalid input (special character) for the new account! Please try again")
        elif account_obj.type not in valid_acc_type:
            raise InvalidAccountTypeError(f"Invalid account type. Account type must be savings, checking, investment "
                                          f"or retirement")
        elif account_obj.balance < 0:
            raise InvalidAccountBalanceError(f"Invalid account balance. Account balance must be greater than 0.")

        return self.acc_dao.add_account_for_customer_by_username(account_obj).to_dict()

    def update_account_by_username_and_account_id(self, acc_obj):
        if self.acc_dao.update_account_by_username_and_account_id(acc_obj) is None:
            raise AccountNotFoundError(f"Account with id {acc_obj.id} not found")
        return self.acc_dao.update_account_by_username_and_account_id(acc_obj).to_dict()

    def delete_account_by_username_and_account_id(self, username, a_id):
        if not self.acc_dao.delete_account_by_username_and_account_id(username, a_id):
            raise AccountNotFoundError(f"Customer with username {username} does not have an account with id {a_id}")
