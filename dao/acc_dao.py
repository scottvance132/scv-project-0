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

    def get_account_by_customer_id_and_account_id(self, customer_id, account_id):
        with psycopg.connect(host="127.0.0.1", port='5432', dbname="p0db", user="postgres",
                             password='mAshgAey208') as conn:
            with conn.cursor() as cur:
                cur.execute('SELECT * FROM accounts WHERE c_id = %s and id = %s', (customer_id, account_id))

                a_row = cur.fetchone()
                if not a_row:
                    return None

                a_id = a_row[0]
                a_type = a_row[1]
                a_balance = a_row[2]
                a_c_id = a_row[3]

                return Account(a_id, a_type, a_balance, a_c_id)

    def add_account_for_customer_by_customer_id(self, account_object):
        a_type_to_add = account_object.type
        a_balance_to_add = account_object.balance
        c_id_to_add = account_object.c_id
        with psycopg.connect(host="127.0.0.1", port='5432', dbname="p0db", user="postgres",
                             password='mAshgAey208') as conn:
            with conn.cursor() as cur:
                cur.execute('INSERT INTO accounts (a_type, a_balance, c_id) VALUES (%s, %s, %s) RETURNING *',
                            (a_type_to_add, a_balance_to_add, c_id_to_add))

                inserted_acc_row = cur.fetchone()

                conn.commit()

                return Account(inserted_acc_row[0], inserted_acc_row[1], inserted_acc_row[2], inserted_acc_row[3])

    def update_account_by_customer_id_and_account_id(self, acc_obj):
        with psycopg.connect(host="127.0.0.1", port='5432', dbname="p0db", user="postgres",
                             password='mAshgAey208') as conn:
            with conn.cursor() as cur:
                cur.execute('UPDATE accounts SET a_type = %s, a_balance = %s WHERE id = %s AND c_id = %s RETURNING *',
                            (acc_obj.type, acc_obj.balance, acc_obj.id, acc_obj.c_id))

                conn.commit()

                updated_acc_row = cur.fetchone()
                if updated_acc_row is None:
                    return None

                return Account(updated_acc_row[0], updated_acc_row[1], updated_acc_row[2], updated_acc_row[3])

    def delete_account_by_customer_id_and_account_id(self, c_id, acc_id):
        with psycopg.connect(host="127.0.0.1", port='5432', dbname="p0db", user="postgres",
                             password='mAshgAey208') as conn:
            with conn.cursor() as cur:
                cur.execute('DELETE FROM accounts WHERE c_id = %s AND id = %s', (c_id, acc_id))

                rows_deleted = cur.rowcount
                print(rows_deleted)

                if rows_deleted != 1:
                    return False
                else:
                    conn.commit()
                    return True

