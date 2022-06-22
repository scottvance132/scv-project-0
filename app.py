from service.customer import Customer, CustomerEncoder
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

customers = [
    c1
]


# c1JSONData = json.dumps(c1, indent=4, cls=CustomerEncoder)


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


# app.run(port=8080)
