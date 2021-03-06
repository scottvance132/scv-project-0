from flask import Blueprint, request

from exception.acc_not_found import AccountNotFoundError
from exception.cus_not_found import CustomerNotFoundError
from exception.invalid_acc_balance import InvalidAccountBalanceError
from exception.invalid_acc_type import InvalidAccountTypeError
from exception.invalid_param import InvalidParameterError
from model.acc import Account
from service.acc_service import AccService

ac = Blueprint('acc_controller', __name__)

acc_service = AccService()


@ac.route('/accounts')
def get_all_accounts():
    return {
        "accounts": acc_service.get_all_accounts()
    }


@ac.route('/customers/<username>/accounts')
def get_all_accounts_by_username(username):
    args = request.args
    balance_gt = args.get('balanceGreaterThan')
    balance_lt = args.get('balanceLessThan')

    try:
        return {
            "accounts": acc_service.get_all_accounts_by_username(username, balance_gt, balance_lt)
        }
    except CustomerNotFoundError as e:
        return {
                   "message": str(e)
               }, 404


@ac.route('/customers/<username>/accounts/<account_id>')
def get_account_by_username_and_account_id(username, account_id):
    try:
        return acc_service.get_account_by_username_and_account_id(username, account_id)
    except CustomerNotFoundError as e:
        return {
            "message": str(e)
        }, 404
    except AccountNotFoundError as e:
        return {
            "message": str(e)
        }, 404


@ac.route('/customers/<username>/accounts', methods=['POST'])
def add_account_for_customer_by_username(username):
    acc_json_dict = request.get_json()
    acc_obj = Account(None, acc_json_dict['a_type'], acc_json_dict['a_balance'], acc_json_dict['username'])
    try:
        return acc_service.add_account_for_customer_by_username(acc_obj), 201
    except CustomerNotFoundError as e:
        return {
            "message": str(e)
        }, 404
    except InvalidAccountTypeError as e:
        return {
            "message": str(e)
        }, 400
    except InvalidAccountBalanceError as e:
        return {
            "message": str(e)
        }, 400
    except InvalidParameterError as e:
        return {
            "message": str(e)
        }, 400


@ac.route('/customers/<username>/accounts/<account_id>', methods=['PUT'])
def update_account_by_username_and_account_id(username, account_id):
    try:
        acc_json_dict = request.get_json()
        return acc_service.update_account_by_username_and_account_id(Account(account_id, acc_json_dict['a_type'],
                                                                     acc_json_dict['a_balance'], username))
    except AccountNotFoundError as e:
        return {
            "message": str(e)
        }, 404


@ac.route('/customers/<username>/accounts/<account_id>', methods=['DELETE'])
def delete_account_by_username_and_account_id(username, account_id):
    try:
        acc_service.delete_account_by_username_and_account_id(username, account_id)
        return {
            "message": f"Account with id {account_id} belonging to customer with username {username} "
                       f"deleted successfully"
        }
    except AccountNotFoundError as e:
        return {
            "message": str(e)
        }, 404
