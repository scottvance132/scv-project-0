import dao.customer_dao
from exception.cus_not_found import CustomerNotFoundError
from exception.customer_exists import CustomerAlreadyExistsError
from exception.invalid_param import InvalidParameterError
from model.customer import Customer
from service.customer_service import CustomerService
import pytest


def test_get_all_customers(mocker):
    # Arrange
    def mock_get_all_customers(self):
        return [Customer(1, 'Scott', 'Vance', '07-12', 'ScottVance0712'),
                Customer(2, 'Mariia', 'Vance', '07-29', 'MariiaVance0729')]

    mocker.patch('dao.customer_dao.CustomerDao.get_all_customers', mock_get_all_customers)

    customer_service = CustomerService()
    # Act
    actual = customer_service.get_all_customers()

    # Assert
    assert actual == [
        {
            "id": 1,
            "first_name": "Scott",
            "last_name": "Vance",
            "birthday": "07-12",
            "username": "ScottVance0712"
        },
        {
            "id": 2,
            "first_name": "Mariia",
            "last_name": "Vance",
            "birthday": "07-29",
            "username": "MariiaVance0729"
        }
    ]


def test_get_customer_by_id_positive(mocker):
    def mock_get_customer_by_id(self, username):
        if username == 'ScottVance0712':
            return Customer(1, 'Scott', 'Vance', '07-12', 'ScottVance0712')
        else:
            return None

    mocker.patch('dao.customer_dao.CustomerDao.get_customer_by_username', mock_get_customer_by_id)

    customer_service = CustomerService()

    actual = customer_service.get_customer_by_username("ScottVance0712")

    assert actual == {
            "id": 1,
            "first_name": "Scott",
            "last_name": "Vance",
            "birthday": "07-12",
            "username": "ScottVance0712"
        }


def test_get_customer_by_id_negative(mocker):
    def mock_get_customer_by_id(self, username):
        if username == 'ScottVance0712':
            return Customer(1, 'Scott', 'Vance', '07-12', 'ScottVance0712')
        else:
            return None

    mocker.patch('dao.customer_dao.CustomerDao.get_customer_by_username', mock_get_customer_by_id)

    customer_service = CustomerService()

    with pytest.raises(CustomerNotFoundError) as excinfo:
        actual = customer_service.get_customer_by_username("JoeBob1212")

    assert str(excinfo.value) == "Customer with username JoeBob1212 was not found"


def test_add_customer_positive(mocker):
    def mock_get_customer_by_username(self, c_id):
        if c_id == "1":
            return None

    mocker.patch("dao.customer_dao.CustomerDao.get_customer_by_username", mock_get_customer_by_username)

    cus_obj_to_add = Customer(1, 'Scott', 'Vance', '07-12', 'ScottVance0712')

    def mock_add_customer(self, cus_obj):
        if cus_obj == cus_obj_to_add:
            return Customer(1, 'Scott', 'Vance', '07-12', 'ScottVance0712')
        else:
            return None

    mocker.patch('dao.customer_dao.CustomerDao.add_customer', mock_add_customer)

    customer_service = CustomerService()

    actual = customer_service.add_customer(cus_obj_to_add)

    assert actual == {
            "id": 1,
            "first_name": "Scott",
            "last_name": "Vance",
            "birthday": "07-12",
            "username": "ScottVance0712"
        }


def test_add_customer_negative_space_in_fn(mocker):
    cus_obj_to_add = Customer(1, 'Sco tt', 'Vance', '07-12', 'ScottVance0712')

    customer_service = CustomerService()

    with pytest.raises(InvalidParameterError) as excinfo:
        actual = customer_service.add_customer(cus_obj_to_add)

    assert str(excinfo.value) == "Invalid input (space) for the new customer! Please try again"


def test_add_customer_negative_space_in_ln(mocker):
    cus_obj_to_add = Customer(1, 'Scott', 'Van ce', '07-12', 'ScottVance0712')

    customer_service = CustomerService()

    with pytest.raises(InvalidParameterError) as excinfo:
        actual = customer_service.add_customer(cus_obj_to_add)

    assert str(excinfo.value) == "Invalid input (space) for the new customer! Please try again"


def test_add_customer_negative_space_in_bday(mocker):
    cus_obj_to_add = Customer(1, 'Scott', 'Vance', '07- 12', 'ScottVance0712')

    customer_service = CustomerService()

    with pytest.raises(InvalidParameterError) as excinfo:
        actual = customer_service.add_customer(cus_obj_to_add)

    assert str(excinfo.value) == "Invalid input (space) for the new customer! Please try again"


def test_add_customer_negative_space_in_username(mocker):
    cus_obj_to_add = Customer(1, 'Scott', 'Vance', '07-12', 'ScottVanc e0712')

    customer_service = CustomerService()

    with pytest.raises(InvalidParameterError) as excinfo:
        actual = customer_service.add_customer(cus_obj_to_add)

    assert str(excinfo.value) == "Invalid input (space) for the new customer! Please try again"


def test_add_customer_negative_num_in_fn(mocker):
    cus_obj_to_add = Customer(1, 'Sco1tt', 'Vance', '07-12', 'ScottVance0712')

    customer_service = CustomerService()

    with pytest.raises(InvalidParameterError) as excinfo:
        actual = customer_service.add_customer(cus_obj_to_add)

    assert str(excinfo.value) == "Invalid input (number) for the new customer! Please try again"


def test_add_customer_negative_num_in_ln(mocker):
    cus_obj_to_add = Customer(1, 'Scott', 'Vanc2e', '07-12', 'ScottVance0712')

    customer_service = CustomerService()

    with pytest.raises(InvalidParameterError) as excinfo:
        actual = customer_service.add_customer(cus_obj_to_add)

    assert str(excinfo.value) == "Invalid input (number) for the new customer! Please try again"


def test_add_customer_negative_spec_char_in_fn(mocker):
    cus_obj_to_add = Customer(1, 'Sco@tt', 'Vance', '07-12', 'ScottVance0712')

    customer_service = CustomerService()

    with pytest.raises(InvalidParameterError) as excinfo:
        actual = customer_service.add_customer(cus_obj_to_add)

    assert str(excinfo.value) == "Invalid input (special character) for the new customer! Please try again"


def test_add_customer_negative_spec_char_in_ln(mocker):
    cus_obj_to_add = Customer(1, 'Scott', 'Vanc!e', '07-12', 'ScottVance0712')

    customer_service = CustomerService()

    with pytest.raises(InvalidParameterError) as excinfo:
        actual = customer_service.add_customer(cus_obj_to_add)

    assert str(excinfo.value) == "Invalid input (special character) for the new customer! Please try again"


def test_add_customer_negative_spec_char_in_bday(mocker):
    cus_obj_to_add = Customer(1, 'Scott', 'Vance', '07-1_2', 'ScottVance0712')

    customer_service = CustomerService()

    with pytest.raises(InvalidParameterError) as excinfo:
        actual = customer_service.add_customer(cus_obj_to_add)

    assert str(excinfo.value) == "Invalid input (special character) for the new customer! Please try again"


def test_add_customer_negative_spec_char_in_username(mocker):
    cus_obj_to_add = Customer(1, 'Scott', 'Vance', '07-12', 'ScottV%ance0712')

    customer_service = CustomerService()

    with pytest.raises(InvalidParameterError) as excinfo:
        actual = customer_service.add_customer(cus_obj_to_add)

    assert str(excinfo.value) == "Invalid input (special character) for the new customer! Please try again"


def test_add_customer_negative_letter_in_bday(mocker):
    cus_obj_to_add = Customer(1, 'Scott', 'Vance', '07-f12', 'ScottVance0712')

    customer_service = CustomerService()

    with pytest.raises(InvalidParameterError) as excinfo:
        actual = customer_service.add_customer(cus_obj_to_add)

    assert str(excinfo.value) == "Invalid input (letter) for the new birthday! Please try again"


def test_add_customer_negative_customer_already_exists(mocker):
    cus_obj_to_add = Customer(1, 'Scott', 'Vance', '07-12', 'ScottVance0712')

    def mock_get_customer_by_username(self, username):
        if username == "ScottVance0712":
            return Customer(1, "Scott", "Vance", "07-12", "ScottVance0712")

    mocker.patch("dao.customer_dao.CustomerDao.get_customer_by_username", mock_get_customer_by_username)

    customer_service = CustomerService()

    with pytest.raises(CustomerAlreadyExistsError) as excinfo:
        actual = customer_service.add_customer(cus_obj_to_add)

    assert str(excinfo.value) == "Customer with username ScottVance0712 already exists"


def test_update_customer_by_id_positive(mocker):
    update_cus_obj = Customer(1, "Jeff", "Smith", "01-01", "JeffSmith0101")

    def mock_update_customer_by_id(self, customer_obj):
        if customer_obj.id == 1:
            return Customer(1, "Jeff", "Smith", "01-01", "JeffSmith0101")
        else:
            return None

    mocker.patch("dao.customer_dao.CustomerDao.update_customer_by_id", mock_update_customer_by_id)

    customer_service = CustomerService()

    actual = customer_service.update_customer_by_id(update_cus_obj)

    assert actual == {
        "id": 1,
        "first_name": "Jeff",
        "last_name": "Smith",
        "birthday": "01-01",
        "username": "JeffSmith0101"
    }


def test_update_customer_by_id_negative(mocker):
    update_cus_obj = Customer(1, "Jeff", "Smith", "01-01", "JeffSmith0101")

    def mock_update_customer_by_id(self, customer_obj):
        if customer_obj.id == 20:
            return Customer(1, "Jeff", "Smith", "01-01", "JeffSmith0101")
        else:
            return None

    mocker.patch('dao.customer_dao.CustomerDao.update_customer_by_id', mock_update_customer_by_id)

    customer_service = CustomerService()

    with pytest.raises(CustomerNotFoundError) as excinfo:
        actual = customer_service.update_customer_by_id(update_cus_obj)

    assert str(excinfo.value) == "Customer was not found"


def test_delete_customer_by_id_positive(mocker):
    def mock_delete_customer_by_id(self, cus_id):
        if cus_id == '1':
            return True
        else:
            return False

    mocker.patch("dao.customer_dao.CustomerDao.delete_customer_by_id", mock_delete_customer_by_id)

    customer_service = CustomerService()

    actual = customer_service.delete_customer_by_id('1')

    assert actual is None


def test_delete_customer_by_id_negative(mocker):
    def mock_delete_customer_by_id(self, cus_id):
        if cus_id == '1':
            return True
        else:
            return False

    mocker.patch("dao.customer_dao.CustomerDao.delete_customer_by_id", mock_delete_customer_by_id)

    customer_service = CustomerService()

    with pytest.raises(CustomerNotFoundError) as excinfo:
        actual = customer_service.delete_customer_by_id("200")

    assert str(excinfo.value) == "Customer with id 200 was not found"
