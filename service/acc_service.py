from dao.customer_dao import CustomerDao
from dao.acc_dao import AccDao
from exception.cus_not_found import CustomerNotFoundError


class AccService:

    def __init__(self):
        self.acc_dao = AccDao()
        self.customer_dao = CustomerDao()

    def get_all_accounts_by_user(self, customer_id):
        if self.customer_dao.get_customer_by_id(customer_id) is None:
            raise CustomerNotFoundError(f"Customer with id {customer_id} was not found")

        return list(map(lambda a: a.to_dict(), self.acc_dao.get_all_accounts_by_customer_id(customer_id)))