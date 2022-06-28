from model.customer import Customer

c1 = Customer("ScottVance0712", "Scott", "Vance", "07/12")
c2 = Customer("MariiaVance0729", "Mariia", "Vance", "07/29")
print(c1.get_username())
print(c2.get_username())
customers = {
    "ScottVance0712": Customer("ScottVance0712", "Scott", "Vance", "07/12"),
    "MariiaVance0729": Customer("MariiaVance0729", "Mariia", "Vance", "07/29")
}


class CustomerDao:
    def get_customer_by_username(self, username):
        return customers[username]

    def get_all_customers(self):
        customer_values = []
        for value in customers.values():
            customer_values.append(value)

        return customer_values

    def add_customer(self, customer_object):
        customers[customer_object.username] = customer_object

        return customer_object

    def edit_customer_by_username(self, username, new_customer_info_object):
        if username == new_customer_info_object.username:
            customers[username] = new_customer_info_object
        else:
            del customers[username]
            customers[new_customer_info_object.username] = new_customer_info_object

        return new_customer_info_object
