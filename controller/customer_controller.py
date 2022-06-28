from flask import Blueprint, request
from model.customer import Customer
from service.customer_service import CustomerService

cc = Blueprint('customer_controller', __name__)
customer_service = CustomerService()


@cc.route('/customers')
def get_all_customers():
    return{
        "customers": customer_service.get_all_customers()
    }


@cc.route('/customers/<username>')
def get_customer_by_username(username):
    try:
        return customer_service.get_customer_by_username(username)
    except KeyError as e:
        return{
            "message": f"Customer with username {username} was not found!"
        }, 404


@cc.route('/customers', methods=['POST'])
def add_customer():
    customer_json_dictionary = request.get_json()
    customer_object = Customer(customer_json_dictionary['username'], customer_json_dictionary['first_name'],
                               customer_json_dictionary['last_name'], customer_json_dictionary['birthday'])

    return customer_service.add_customer(customer_object), 201


@cc.route('/customers/<username>', methods=['POST'])
def edit_customer_by_username(username):
    customer_json_dictionary = request.get_json()
    customer_object = Customer(customer_json_dictionary['first_name', customer_json_dictionary['last_name'],
                                                        customer_json_dictionary['birthday']])
    return customer_service.edit_customer_by_username(username, customer_object)

