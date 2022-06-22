from service.customer import Customer
from flask import Flask, request

app = Flask(__name__)

c1 = Customer("Scott", "Vance", "07/12", "checking", 1000.00)
c2 = Customer("Mariia", "Vance", "07/29", "checking", 5.12)
print(c1)

print(c1.get_first_name())
print(c1.get_last_name())
print(c1.get_birthday())
print(c1.username)
print(c1.get_account_info())

# c1.set_last_name("Smith")
# print(c1.get_last_name())
# print(c1.get_username())

# c1.set_birthday("12/12")
# print(c1.get_username())

customers = {
    c1.username: c1.get_account_info()
}
print(customers)


@app.route("/test")
def hello():
    return "test executed successfully"


@app.route("/customers")
def get_all_customers():
    my_customers = []
    for key in customers:
        customer = {
            "username": key
        }

        my_customers.append(customer)

    return{
              "customers": my_customers
    }, 200


@app.route("/customers/<username>")
def get_customer_by_username(username):
    customers_by_username = {}
    if username in customers:
        customers_by_username['username'] = username
        return{
            "username": customers_by_username
        }
    else:
        return{
            "message": f"User with username {username} does not exist!"
        }, 404


@app.route("/customers", methods=['POST'])
def create_customer():
    data = request.get_json()
    print(data)

    if data['first_name'] in customers:
        return{
            "message": f"Customer with username {data['username']} already exists! Cannot create this customer"
        }, 400
    else:
        customers[(data['first_name'])] = {
            "first_name": data['first_name'],
            "last_name": data['last_name'],
            "birthday": data['birthday']
        }

        return {
            'customers': customers
        }, 201


app.run(port=8080)
