from dao.customer_dao import CustomerDao
from exception.cus_not_found import CustomerNotFoundError


class CustomerService:

    def __init__(self):
        self.customer_dao = CustomerDao()

    def get_all_customers(self):
        list_of_customer_objects = self.customer_dao.get_all_customers()
        # list_of_customer_dictionaries = []
        # for customer_object in list_of_customer_objects:
        #     list_of_customer_dictionaries.append(customer_object.to_dict())

        return list(map(lambda x: x.to_dict(), list_of_customer_objects))

    def get_customer_by_id(self, username):
        customer_object = self.customer_dao.get_customer_by_id(username)
        return customer_object.to_dict()

    def add_customer(self, customer_object):
        added_customer_object = self.customer_dao.add_customer(customer_object)
        return added_customer_object.to_dict()

    def update_customer_by_id(self, customer_object):
        edited_customer_object = self.customer_dao.update_customer_by_id(customer_object)
        return edited_customer_object.to_dict()

    def delete_customer_by_id(self, cus_id):
        if not self.customer_dao.delete_customer_by_id(cus_id):
            raise CustomerNotFoundError(f"Customer with id {cus_id} was not found")
