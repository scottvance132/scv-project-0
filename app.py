from service.customer import Customer
from flask import Flask, request

app = Flask(__name__)

c1 = Customer("Scott", "Vance", "07/12")
print(c1.username)

app.run(port=8080)
