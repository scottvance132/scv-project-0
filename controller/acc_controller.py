from flask import Blueprint, request

from exception.acc_not_found import AccountNotFoundError
from exception.cus_not_found import CustomerNotFoundError
from model.acc import Account
from service.acc_service import AccService

ac = Blueprint('acc_controller', __name__)

acc_service = AccService()


@ac.route('/customers/<customer_id>/accounts')
def get_all_accounts_by_customer_id(customer_id):
    args = request.args
    balance_gt = args.get('balanceGreaterThan')
    balance_lt = args.get('balanceLessThan')

    try:
        return {
            "accounts": acc_service.get_all_accounts_by_customer_id(customer_id, balance_gt, balance_lt)
        }
    except CustomerNotFoundError as e:
        return {
                   "message": str(e)
               }, 404


@ac.route('/customers/<customer_id>/accounts/<account_id>')
def get_account_by_customer_id_and_account_id(customer_id, account_id):
    try:
        return acc_service.get_account_by_customer_id_and_account_id(customer_id, account_id)
    except CustomerNotFoundError as e:
        return {
            "message": str(e)
        }, 404
    except AccountNotFoundError as e:
        return {
            "message": str(e)
        }, 404


@ac.route('/customers/<customer_id>/accounts', methods=['POST'])
def add_account_for_customer_by_customer_id(customer_id):
    acc_json_dict = request.get_json()
    acc_obj = Account(None, acc_json_dict['a_type'], acc_json_dict['a_balance'], acc_json_dict['customer_id'])

    return acc_service.add_account_for_customer_by_customer_id(acc_obj), 201


@ac.route('/customers/<customer_id>/accounts/<account_id>', methods=['PUT'])
def update_account_by_customer_id_and_account_id(customer_id, account_id):
    acc_json_dict = request.get_json()
    return acc_service.update_account_by_customer_id_and_account_id(Account(account_id, acc_json_dict['a_type'],
                                                                            acc_json_dict['a_balance'], customer_id))


@ac.route('/customers/<customer_id>/accounts/<account_id>', methods=['DELETE'])
def delete_account_by_customer_id_and_account_id(customer_id, account_id):
    try:
        acc_service.delete_account_by_customer_id_and_account_id(customer_id, account_id)
        return {
            "message": f"Account with id {account_id} belonging to customer with id {customer_id} deleted successfully"
        }
    except AccountNotFoundError as e:
        return {
            "message": str(e)
        }, 404
