from flask import Blueprint

from exception.cus_not_found import CustomerNotFoundError
from service.acc_service import AccService

ac = Blueprint('acc_controller', __name__)

acc_service = AccService()


@ac.route('/customers/<customer_id>/accounts')
def get_all_accounts_by_customer_id(customer_id):
    try:
        return {
            "accounts": acc_service.get_all_accounts_by_user(customer_id)
        }
    except CustomerNotFoundError as e:
        return {
            "message": str(e)
        }, 404
