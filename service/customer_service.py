from dao.customer_dao import CustomerDao
from exception.cus_not_found import CustomerNotFoundError
from exception.invalid_param import InvalidParameterError
from utility.contains_num import containsNumber
from utility.contains_space import containsSpace
from utility.contains_spec_char import containsSpecChar


class CustomerService:

    def __init__(self):
        self.customer_dao = CustomerDao()

    def get_all_customers(self):
        list_of_customer_objects = self.customer_dao.get_all_customers()

        return list(map(lambda x: x.to_dict(), list_of_customer_objects))

    def get_customer_by_id(self, customer_id):
        if self.customer_dao.get_customer_by_id(customer_id) is None:
            raise CustomerNotFoundError(f"Customer with id {customer_id} was not found")

        return self.customer_dao.get_customer_by_id(customer_id).to_dict()

    def add_customer(self, customer_object):
        if containsSpace(customer_object.first_name) or containsSpace(customer_object.last_name) or \
                containsSpace(customer_object.birthday) or containsSpace(customer_object.username):
            print('error caught')
            raise InvalidParameterError(f"Invalid input (space) for the new customer! Please try again")
        elif containsNumber(customer_object.first_name) or containsNumber(customer_object.last_name):
            raise InvalidParameterError(f"Invalid input (number) for the new customer! Please try again")
        elif containsSpecChar(customer_object.first_name) or containsSpecChar(customer_object.last_name) or \
                containsSpecChar(customer_object.birthday) or containsSpecChar(customer_object.username):
            raise InvalidParameterError(f"Invalid input (special character) for the new customer! Please try again")
        else:
            print('error not caught')
            return self.customer_dao.add_customer(customer_object).to_dict()

    def update_customer_by_id(self, customer_object):
        if self.customer_dao.update_customer_by_id(customer_object) is None:
            raise CustomerNotFoundError(f"Customer was not found")
        return self.customer_dao.update_customer_by_id(customer_object).to_dict()

    def delete_customer_by_id(self, cus_id):
        if not self.customer_dao.delete_customer_by_id(cus_id):
            raise CustomerNotFoundError(f"Customer with id {cus_id} was not found")
