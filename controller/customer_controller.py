from flask import Blueprint, request

from exception.cus_not_found import CustomerNotFoundError
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
    customer_object = Customer(None, customer_json_dictionary['first_name'], customer_json_dictionary['last_name'],
                               customer_json_dictionary['birthday'], customer_json_dictionary['username'])

    return customer_service.add_customer(customer_object), 201


@cc.route('/customers/<customer_id>', methods=['PUT'])
def update_customer_by_id(customer_id):
    customer_json_dictionary = request.get_json()
    return customer_service.update_customer_by_id(Customer(customer_id, customer_json_dictionary['first_name'],
                                                           customer_json_dictionary['last_name'],
                                                           customer_json_dictionary['birthday'],
                                                           customer_json_dictionary['username']))


@cc.route('/customers/<customer_id>', methods=['DELETE'])
def delete_customer_by_id(customer_id):
    try:
        customer_service.delete_customer_by_id(customer_id)
        return {
            "message": f"Customer with id {customer_id} deleted successfully"
        }
    except CustomerNotFoundError as e:
        return {
            "message": str(e)
        }, 404
