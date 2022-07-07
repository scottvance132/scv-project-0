import psycopg
from model.customer import Customer


class CustomerDao:

    def get_all_customers(self):
        with psycopg.connect(host="127.0.0.1", port='5432', dbname="p0db", user="postgres",
                             password='mAshgAey208') as conn:
            with conn.cursor() as cur:
                cur.execute('SELECT * FROM customers')

                my_list_of_cus_objs = []
                for cus in cur:
                    c_id = cus[0]
                    first_name = cus[1]
                    last_name = cus[2]
                    birthday = cus[3]
                    username = cus[4]

                    my_cus_obj = Customer(c_id, first_name, last_name, birthday, username)
                    my_list_of_cus_objs.append(my_cus_obj)

                return my_list_of_cus_objs

    def get_customer_by_username(self, username):
        with psycopg.connect(host="127.0.0.1", port='5432', dbname="p0db", user="postgres",
                             password='mAshgAey208') as conn:
            with conn.cursor() as cur:

                cur.execute('SELECT * FROM customers WHERE username = %s', (username,))

                c_row = cur.fetchone()
                if not c_row:
                    return None

                c_id = c_row[0]
                first_name = c_row[1]
                last_name = c_row[2]
                birthday = c_row[3]
                username = c_row[4]

                return Customer(c_id, first_name, last_name, birthday, username)

    def add_customer(self, customer_object):
        fn_to_add = customer_object.first_name
        ln_to_add = customer_object.last_name
        bday_to_add = customer_object.birthday
        username_to_add = customer_object.username

        with psycopg.connect(host="127.0.0.1", port='5432', dbname="p0db", user="postgres",
                             password='mAshgAey208') as conn:
            with conn.cursor() as cur:
                cur.execute("INSERT INTO customers (first_name, last_name, birthday, username) VALUES (%s, %s, %s, %s) "
                            "RETURNING *", (fn_to_add, ln_to_add, bday_to_add, username_to_add))

                inserted_cus_row = cur.fetchone()

                conn.commit()

                return Customer(inserted_cus_row[0], inserted_cus_row[1], inserted_cus_row[2], inserted_cus_row[3],
                                inserted_cus_row[4])

    def update_customer_by_username(self, cus_obj):
        with psycopg.connect(host="127.0.0.1", port='5432', dbname="p0db", user="postgres",
                             password='mAshgAey208') as conn:
            with conn.cursor() as cur:
                cur.execute("UPDATE customers SET first_name = %s, last_name = %s, birthday = %s, username = %s"
                            "WHERE username = %s RETURNING *", (cus_obj.first_name, cus_obj.last_name, cus_obj.birthday,
                                                                cus_obj.username, cus_obj.id))

                conn.commit()

                updated_cus_row = cur.fetchone()
                if updated_cus_row is None:
                    return None

                return Customer(updated_cus_row[0], updated_cus_row[1], updated_cus_row[2], updated_cus_row[3],
                                updated_cus_row[4])

    def delete_customer_by_username(self, username):
        with psycopg.connect(host="127.0.0.1", port='5432', dbname="p0db", user="postgres",
                             password='mAshgAey208') as conn:
            with conn.cursor() as cur:
                cur.execute('DELETE FROM customers WHERE username = %s', (username,))

                rows_deleted = cur.rowcount

                if rows_deleted != 1:
                    return False
                else:
                    conn.commit()
                    return True
