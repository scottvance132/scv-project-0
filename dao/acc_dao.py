import psycopg
from model.acc import Account


class AccDao:

    def get_all_accounts_by_customer_id(self, customer_id):
        with psycopg.connect(host="127.0.0.1", port='5432', dbname="p0db", user="postgres",
                             password='mAshgAey208') as conn:
            with conn.cursor() as cur:
                cur.execute('SELECT * FROM accounts WHERE c_id = %s', (customer_id,))

                acc_list = []

                for row in cur:
                    acc_list.append(Account(row[0], row[1], row[2], row[3]))

                return acc_list
