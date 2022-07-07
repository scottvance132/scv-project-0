import dao.customer_dao
import dao.acc_dao
from exception.cus_not_found import CustomerNotFoundError
from exception.customer_exists import CustomerAlreadyExistsError
from exception.invalid_param import InvalidParameterError
from exception.acc_not_found import AccountNotFoundError
from exception.invalid_acc_type import InvalidAccountTypeError
from exception.invalid_acc_balance import InvalidAccountBalanceError
from model.customer import Customer
from model.acc import Account
from service.customer_service import CustomerService
from service.acc_service import AccService
import pytest


def test_get_all_accounts(mocker):
    def mock_get_all_accounts(self):
        return [Account(1, "savings", 1000, 'JeffSmith0101'), Account(2, "checking", 2000, 'JeffSmith0101'),
                Account(3, "savings", 1200, 'JeffSmith0102')]

    mocker.patch('dao.acc_dao.AccDao.get_all_accounts', mock_get_all_accounts)

    acc_service = AccService()

    actual = acc_service.get_all_accounts()

    assert actual == [
        {
            "a_id": 1,
            "a_type": "savings",
            "a_balance": 1000,
            "username": 'JeffSmith0101'
        },
        {
            "a_id": 2,
            "a_type": "checking",
            "a_balance": 2000,
            "username": 'JeffSmith0101'
        },
        {
            "a_id": 3,
            "a_type": "savings",
            "a_balance": 1200,
            "username": 'JeffSmith0102'
        }
    ]


def test_get_all_accounts_by_username(mocker):
    def mock_get_all_accounts_by_username(self, username):
        if username == "ScottVance0712":
            return [Account(1, "savings", 1000, 'ScottVance0712'), Account(2, "checking", 2000, 'ScottVance0712')]
        else:
            return []

    mocker.patch('dao.acc_dao.AccDao.get_all_accounts_by_username', mock_get_all_accounts_by_username)

    acc_service = AccService()

    actual = acc_service.get_all_accounts_by_username("ScottVance0712", None, None)

    assert actual == [
        {
            "a_id": 1,
            "a_type": "savings",
            "a_balance": 1000,
            "username": 'ScottVance0712'
        },
        {
            "a_id": 2,
            "a_type": "checking",
            "a_balance": 2000,
            "username": 'ScottVance0712'
        }
    ]


def test_get_all_accounts_by_username_greater(mocker):
    def mock_get_all_accounts_greater_by_username(self, username, query_value):
        if username == "ScottVance0712":
            return [Account(2, "checking", 2000, 'ScottVance0712')]
        else:
            return []

    mocker.patch('dao.acc_dao.AccDao.get_all_accounts_greater_by_username',
                 mock_get_all_accounts_greater_by_username)

    acc_service = AccService()

    actual = acc_service.get_all_accounts_by_username("ScottVance0712", 1200, None)

    assert actual == [
        {
            "a_id": 2,
            "a_type": "checking",
            "a_balance": 2000,
            "username": 'ScottVance0712'
        }
    ]


def test_get_all_accounts_less_by_username(mocker):
    def mock_get_all_accounts_less_by_username(self, username, query_value):
        if username == "ScottVance0712":
            return [Account(1, "savings", 1000, 'ScottVance0712')]
        else:
            return []

    mocker.patch('dao.acc_dao.AccDao.get_all_accounts_less_by_username', mock_get_all_accounts_less_by_username)

    acc_service = AccService()

    actual = acc_service.get_all_accounts_by_username("ScottVance0712", None, 1700)

    assert actual == [
        {
            "a_id": 1,
            "a_type": "savings",
            "a_balance": 1000,
            "username": 'ScottVance0712'
        }
    ]


def test_get_all_accounts_between_by_username(mocker):
    def mock_get_all_accounts_between_by_username(self, username, query_1, query_2):
        if username == "ScottVance0712":
            return [Account(1, "savings", 1000, 'ScottVance0712'), Account(2, "checking", 2000, 'ScottVance0712')]
        else:
            return []

    mocker.patch('dao.acc_dao.AccDao.get_all_accounts_between_by_username',
                 mock_get_all_accounts_between_by_username)

    acc_service = AccService()

    actual = acc_service.get_all_accounts_by_username("ScottVance0712", 700, 3000)

    assert actual == [
        {
            "a_id": 1,
            "a_type": "savings",
            "a_balance": 1000,
            "username": 'ScottVance0712'
        },
        {
            "a_id": 2,
            "a_type": "checking",
            "a_balance": 2000,
            "username": 'ScottVance0712'
        }
    ]


def test_get_all_accounts_by_username_negative(mocker):
    def mock_get_all_accounts_by_username(self, username):
        if username == "ScottVance0712":
            return [Account(1, "savings", 1000, 'ScottVance0712'), Account(2, "checking", 2000, 'ScottVance0712')]
        else:
            return []

    mocker.patch('dao.acc_dao.AccDao.get_all_accounts_by_username', mock_get_all_accounts_by_username)

    acc_service = AccService()

    with pytest.raises(CustomerNotFoundError) as excinfo:
        actual = acc_service.get_all_accounts_by_username("ScottVance0713", None, None)

    assert str(excinfo.value) == "Customer with username ScottVance0713 was not found"


def test_get_account_by_username_and_account_id_positive(mocker):
    def mock_get_account_by_username_and_account_id(self, username, account_id):
        if username == 'ScottVance0712' and account_id == 1:
            return Account(1, "checking", 200, 'ScottVance0712')
        else:
            return None

    mocker.patch('dao.acc_dao.AccDao.get_account_by_username_and_account_id',
                 mock_get_account_by_username_and_account_id)

    acc_service = AccService()

    actual = acc_service.get_account_by_username_and_account_id('ScottVance0712', 1)

    assert actual == \
        {
            "a_id": 1,
            "a_type": "checking",
            "a_balance": 200,
            "username": 'ScottVance0712'
        }


def test_get_account_by_username_and_account_id_negative_cus_not_found(mocker):
    def mock_get_account_by_username_and_account_id(self, username, account_id):
        if username == 'ScottVance0712' and account_id == 1:
            return Account(1, "checking", 200, 'ScottVance0712')
        else:
            return None

    mocker.patch('dao.acc_dao.AccDao.get_account_by_username_and_account_id',
                 mock_get_account_by_username_and_account_id)

    acc_service = AccService()

    with pytest.raises(CustomerNotFoundError) as excinfo:
        actual = acc_service.get_account_by_username_and_account_id('ScottVance0713', 1)

    assert str(excinfo.value) == "Customer with username ScottVance0713 was not found"


def test_get_account_by_username_and_account_id_negative_acc_not_found(mocker):
    def mock_get_account_by_username_and_account_id(self, username, account_id):
        if username == 'ScottVance0712' and account_id == 1:
            return Account(1, "checking", 200, 'ScottVance0712')
        else:
            return None

    mocker.patch('dao.acc_dao.AccDao.get_account_by_username_and_account_id',
                 mock_get_account_by_username_and_account_id)

    acc_service = AccService()

    with pytest.raises(AccountNotFoundError) as excinfo:
        actual = acc_service.get_account_by_username_and_account_id('ScottVance0712', 22)

    assert str(excinfo.value) == "Customer with username ScottVance0712 does not have account with id 22"


def test_add_account_for_customer_by_username_positive(mocker):
    def mock_get_customer_by_username(self, username):
        return {
                "id": 1,
                "first_name": "Scott",
                "last_name": "Vance",
                "birthday": "07-12",
                "username": "ScottVance0712"
            }

    mocker.patch("dao.customer_dao.CustomerDao.get_customer_by_username", mock_get_customer_by_username)

    acc_obj_to_add = Account(1, "savings", 200, 'ScottVance0712')

    def mock_add_account_for_customer_by_username(self, acc_obj):
        if acc_obj == acc_obj_to_add:
            return Account(1, "savings", 200, 'ScottVance0712')
        else:
            return None

    mocker.patch('dao.acc_dao.AccDao.add_account_for_customer_by_username', mock_add_account_for_customer_by_username)

    acc_service = AccService()

    actual = acc_service.add_account_for_customer_by_username(acc_obj_to_add)

    assert actual == {
        "a_id": 1,
        "a_type": "savings",
        "a_balance": 200,
        "username": 'ScottVance0712'
    }


def test_add_account_for_customer_by_username_negative_no_customer(mocker):
    def mock_get_customer_by_username(self, username):
        return None

    mocker.patch("dao.customer_dao.CustomerDao.get_customer_by_username", mock_get_customer_by_username)

    acc_obj_to_add = Account(1, "savings", 200, 'ScottVance0712')

    def mock_add_account_for_customer_by_username(self, acc_obj):
        if acc_obj == acc_obj_to_add:
            return Account(1, "savings", 200, 'ScottVance0712')
        else:
            return None

    mocker.patch('dao.acc_dao.AccDao.add_account_for_customer_by_username', mock_add_account_for_customer_by_username)

    acc_service = AccService()

    with pytest.raises(CustomerNotFoundError) as excinfo:
        actual = acc_service.add_account_for_customer_by_username(acc_obj_to_add)

    assert str(excinfo.value) == "Customer with username ScottVance0712 was not found"


def test_add_account_for_customer_by_username_negative_invalid_acc_type(mocker):
    def mock_get_customer_by_username(self, username):
        return {
                "id": 1,
                "first_name": "Scott",
                "last_name": "Vance",
                "birthday": "07-12",
                "username": "ScottVance0712"
            }

    mocker.patch("dao.customer_dao.CustomerDao.get_customer_by_username", mock_get_customer_by_username)

    acc_obj_to_add = Account(1, "cool", 200, 'ScottVance0712')

    def mock_add_account_for_customer_by_username(self, acc_obj):
        if acc_obj == acc_obj_to_add:
            return Account(1, "savings", 200, 'ScottVance0712')
        else:
            return None

    mocker.patch('dao.acc_dao.AccDao.add_account_for_customer_by_username', mock_add_account_for_customer_by_username)

    acc_service = AccService()

    with pytest.raises(InvalidAccountTypeError) as excinfo:
        actual = acc_service.add_account_for_customer_by_username(acc_obj_to_add)

    assert str(excinfo.value) == "Invalid account type. Account type must be savings, checking, investment " \
                                 "or retirement"


def test_add_account_for_customer_by_username_negative_invalid_acc_balance(mocker):
    def mock_get_customer_by_username(self, username):
        return {
                "id": 1,
                "first_name": "Scott",
                "last_name": "Vance",
                "birthday": "07-12",
                "username": "ScottVance0712"
            }

    mocker.patch("dao.customer_dao.CustomerDao.get_customer_by_username", mock_get_customer_by_username)

    acc_obj_to_add = Account(1, "savings", -1, 'ScottVance0712')

    def mock_add_account_for_customer_by_username(self, acc_obj):
        if acc_obj == acc_obj_to_add:
            return Account(1, "savings", 200, 'ScottVance0712')
        else:
            return None

    mocker.patch('dao.acc_dao.AccDao.add_account_for_customer_by_username', mock_add_account_for_customer_by_username)

    acc_service = AccService()

    with pytest.raises(InvalidAccountBalanceError) as excinfo:
        actual = acc_service.add_account_for_customer_by_username(acc_obj_to_add)

    assert str(excinfo.value) == "Invalid account balance. Account balance must be greater than 0."


def test_add_account_for_customer_by_username_negative_invalid_acc_parameter(mocker):
    def mock_get_customer_by_username(self, username):
        return {
                "id": 1,
                "first_name": "Scott",
                "last_name": "Vance",
                "birthday": "07-12",
                "username": "ScottVance0712"
            }

    mocker.patch("dao.customer_dao.CustomerDao.get_customer_by_username", mock_get_customer_by_username)

    acc_obj_to_add = Account(1, "sav ings", 1, 'ScottVance0712')

    def mock_add_account_for_customer_by_username(self, acc_obj):
        if acc_obj == acc_obj_to_add:
            return Account(1, "savings", 200, 'ScottVance0712')
        else:
            return None

    mocker.patch('dao.acc_dao.AccDao.add_account_for_customer_by_username', mock_add_account_for_customer_by_username)

    acc_service = AccService()

    with pytest.raises(InvalidParameterError) as excinfo:
        actual = acc_service.add_account_for_customer_by_username(acc_obj_to_add)

    assert str(excinfo.value) == "Invalid input (space) for the new account! Please try again"


def test_add_account_for_customer_by_username_negative_invalid_acc_parameter_num(mocker):
    def mock_get_customer_by_username(self, username):
        return {
                "id": 1,
                "first_name": "Scott",
                "last_name": "Vance",
                "birthday": "07-12",
                "username": "ScottVance0712"
            }

    mocker.patch("dao.customer_dao.CustomerDao.get_customer_by_username", mock_get_customer_by_username)

    acc_obj_to_add = Account(1, "sav1ngs", 1, 'ScottVance0712')

    def mock_add_account_for_customer_by_username(self, acc_obj):
        if acc_obj == acc_obj_to_add:
            return Account(1, "savngs", 200, 'ScottVance0712')
        else:
            return None

    mocker.patch('dao.acc_dao.AccDao.add_account_for_customer_by_username', mock_add_account_for_customer_by_username)

    acc_service = AccService()

    with pytest.raises(InvalidParameterError) as excinfo:
        actual = acc_service.add_account_for_customer_by_username(acc_obj_to_add)

    assert str(excinfo.value) == "Invalid input (number) for the new account! Please try again"


def test_add_account_for_customer_by_username_negative_invalid_acc_parameter_spec_char(mocker):
    def mock_get_customer_by_username(self, username):
        return {
                "id": 1,
                "first_name": "Scott",
                "last_name": "Vance",
                "birthday": "07-12",
                "username": "ScottVance0712"
            }

    mocker.patch("dao.customer_dao.CustomerDao.get_customer_by_username", mock_get_customer_by_username)

    acc_obj_to_add = Account(1, "sav!ngs", 1, 'ScottVance0712')

    def mock_add_account_for_customer_by_username(self, acc_obj):
        if acc_obj == acc_obj_to_add:
            return Account(1, "savings", 200, 'ScottVance0712')
        else:
            return None

    mocker.patch('dao.acc_dao.AccDao.add_account_for_customer_by_username', mock_add_account_for_customer_by_username)

    acc_service = AccService()

    with pytest.raises(InvalidParameterError) as excinfo:
        actual = acc_service.add_account_for_customer_by_username(acc_obj_to_add)

    assert str(excinfo.value) == "Invalid input (special character) for the new account! Please try again"


def test_update_account_by_username_and_account_id_positive(mocker):
    def mock_get_account_by_username(self):
        return {
            "a_id": 1,
            "a_type": "savings",
            "a_balance": 200,
            "username": 'ScottVance0712'
        }

    mocker.patch("dao.customer_dao.CustomerDao.get_customer_by_username", mock_get_account_by_username)

    acc_obj_to_update = Account(1, "savings", 1200, 'ScottVance0712')

    def mock_update_account_by_username_and_account_id(self, acc_obj):
        if acc_obj.username == 'ScottVance0712':
            return Account(1, "savings", 1200, 'ScottVance0712')
        else:
            return None

    mocker.patch('dao.acc_dao.AccDao.update_account_by_username_and_account_id',
                 mock_update_account_by_username_and_account_id)

    acc_service = AccService()

    actual = acc_service.update_account_by_username_and_account_id(acc_obj_to_update)

    assert actual == {
        "a_id": 1,
        "a_type": "savings",
        "a_balance": 1200,
        "username": 'ScottVance0712'
    }


def test_update_account_by_username_and_account_id_negative(mocker):
    def mock_get_account_by_username(self):
        return {
            "a_id": 1,
            "a_type": "savings",
            "a_balance": 200,
            "username": 'ScottVance0712'
        }

    mocker.patch("dao.acc_dao.AccDao.get_all_accounts_by_username", mock_get_account_by_username)

    acc_obj_to_update = Account(10, "savings", 1200, 'ScottVance0712')

    def mock_update_account_by_username_and_account_id(self, username):
        if username == 'ScottVance0712':
            return Account(1, "savings", 1200, 'ScottVance0712')
        else:
            return None

    mocker.patch('dao.acc_dao.AccDao.update_account_by_username_and_account_id',
                 mock_update_account_by_username_and_account_id)

    acc_service = AccService()

    with pytest.raises(AccountNotFoundError) as excinfo:
        actual = acc_service.update_account_by_username_and_account_id(acc_obj_to_update)

    assert str(excinfo.value) == "Account with id 10 not found"


def test_delete_account_by_username_and_account_id_positive(mocker):
    def mock_get_customer_by_username(self, c_id):
        return {
            "id": 1,
            "first_name": "Scott",
            "last_name": "Vance",
            "birthday": "07-12",
            "username": "ScottVance0712"
        }

    mocker.patch("dao.customer_dao.CustomerDao.get_customer_by_username", mock_get_customer_by_username)

    def mock_delete_account_by_username_and_account_id(self, username, a_id):
        if username == 'ScottVance0712':
            if a_id == '1':
                return True
        else:
            return False

    mocker.patch('dao.acc_dao.AccDao.delete_account_by_username_and_account_id',
                 mock_delete_account_by_username_and_account_id)

    acc_service = AccService()

    actual = acc_service.delete_account_by_username_and_account_id('ScottVance0712', '1')

    assert actual is None


def test_delete_account_by_username_and_account_id_negative(mocker):
    def mock_get_customer_by_username(self, username):
        return {
            "id": 1,
            "first_name": "Scott",
            "last_name": "Vance",
            "birthday": "07-12",
            "username": "ScottVance0712"
        }

    mocker.patch("dao.customer_dao.CustomerDao.get_customer_by_username", mock_get_customer_by_username)

    def mock_delete_account_by_username_and_account_id(self, username, a_id):
        if username == 'ScottVance0712':
            if a_id == '1':
                return True
        else:
            return False

    mocker.patch('dao.acc_dao.AccDao.delete_account_by_username_and_account_id',
                 mock_delete_account_by_username_and_account_id)

    acc_service = AccService()

    with pytest.raises(AccountNotFoundError) as excinfo:
        actual = acc_service.delete_account_by_username_and_account_id('ScottVance0713', '5')

    assert str(excinfo.value) == 'Customer with username ScottVance0713 does not have an account with id 5'

