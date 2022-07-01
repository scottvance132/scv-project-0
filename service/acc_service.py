from dao.customer_dao import CustomerDao
from dao.acc_dao import AccDao
from exception.acc_not_found import AccountNotFoundError
from exception.cus_not_found import CustomerNotFoundError


class AccService:

    def __init__(self):
        # self.test = None
        self.acc_dao = AccDao()
        self.customer_dao = CustomerDao()

    def get_all_accounts(self):
        list_of_accounts = self.acc_dao.get_all_accounts()
        return list(map(lambda a: a.to_dict(), list_of_accounts))

    def get_all_accounts_by_customer_id(self, customer_id, query_1, query_2):
        if self.customer_dao.get_customer_by_id(customer_id) is None:
            raise CustomerNotFoundError(f"Customer with id {customer_id} was not found")

        if query_1 is None and query_2 is None:
            return list(map(lambda a: a.to_dict(), self.acc_dao.get_all_accounts_by_customer_id(customer_id)))

        elif query_1 is not None and query_2 is not None:
            return list(map(lambda a: a.to_dict(), self.acc_dao.get_all_accounts_between_by_customer_id(customer_id,
                                                                                                        query_1,
                                                                                                        query_2)))

        elif query_1 is not None:
            return list(map(lambda a: a.to_dict(), self.acc_dao.get_all_accounts_greater_by_customer_id(customer_id,
                                                                                                        query_1)))

        elif query_2 is not None:
            return list(map(lambda a: a.to_dict(), self.acc_dao.get_all_accounts_less_by_customer_id(customer_id,
                                                                                                     query_2)))

        else:
            return []

    def get_account_by_customer_id_and_account_id(self, customer_id, account_id):
        if self.customer_dao.get_customer_by_id(customer_id) is None:
            raise CustomerNotFoundError(f"Customer with id {customer_id} was not found")
        elif self.acc_dao.get_account_by_customer_id_and_account_id(customer_id, account_id) is None:
            raise AccountNotFoundError(f"Customer with id {customer_id} does not have account with id {account_id}")

        return self.acc_dao.get_account_by_customer_id_and_account_id(customer_id, account_id).to_dict()

    def add_account_for_customer_by_customer_id(self, account_id):
        # if self.customer_dao.get_customer_by_id(customer_id) is None:
        #     raise CustomerNotFoundError(f"Customer with id {customer_id} was not found")

        return self.acc_dao.add_account_for_customer_by_customer_id(account_id).to_dict()

    def update_account_by_customer_id_and_account_id(self, acc_obj):
        edited_acc_obj = self.acc_dao.update_account_by_customer_id_and_account_id(acc_obj)
        return edited_acc_obj.to_dict()

    def delete_account_by_customer_id_and_account_id(self, c_id, a_id):
        if not self.acc_dao.delete_account_by_customer_id_and_account_id(c_id, a_id):
            raise AccountNotFoundError(f"Customer with id {c_id} does not have an account with id {a_id}")
