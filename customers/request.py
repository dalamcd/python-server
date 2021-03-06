import sqlite3
import json
from sqlite3 import dbapi2
from models import Customer

CUSTOMERS = [
    {
        "id": 1,
        "name": "Devin Kent",
    },
    {
        "id": 2,
        "name": "Travis Milner",
    },
    {
        "id": 3,
        "name": "Silas Lowe",
    },
    {
        "id": 4,
        "name": "Sanjeet Parsad",
    }
]


def get_all_customers():
    with sqlite3.connect("./kennel.db") as conn:

        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            c.id,
            c.name,
            c.address,
            c.email,
            c.password
        FROM customer c
        """)

        customers = []

        dataset = db_cursor.fetchall()

        for row in dataset:
            cust = Customer(row['id'], row['name'], row['address'],
                            row['email'], row['password'])

            customers.append(cust.__dict__)

    return json.dumps(customers)

def get_single_customer(id):
    with sqlite3.connect("./kennel.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            c.id,
            c.name,
            c.address,
            c.email,
            c.password
        FROM customer c
        WHERE c.id = ?
        """, ( id, ))

        data = db_cursor.fetchone()

        cust = Customer(data['id'], data['name'], data['address'],
                            data['email'], data['password'])

        return json.dumps(cust.__dict__)

def get_customers_by_email(email):

    with sqlite3.connect("./kennel.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
        select
            c.id,
            c.name,
            c.address,
            c.email,
            c.password
        from Customer c
        WHERE c.email = ?
        """, ( email, ))

        customers = []
        dataset = db_cursor.fetchall()

        for row in dataset:
            customer = Customer(row['id'], row['name'], row['address'], row['email'], row['password'])
            customers.append(customer.__dict__)

    return json.dumps(customers)

def create_customer(customer):

	max_id = CUSTOMERS[-1]["id"]

	max_id += 1

	customer["id"] = max_id

	CUSTOMERS.append(customer)

	return customer

def delete_customer(id):
    with sqlite3.connect("./kennel.db") as conn:
        
        db_cursor = conn.cursor()

        db_cursor.execute("""
        DELETE FROM customer
        WHERE id = ?
        """, (id, ))

def update_customer(id, new_customer):
    with sqlite3.connect("./kennel.db") as conn:

        db_cursor = conn.cursor()

        db_cursor.execute("""
        UPDATE customer
            SET
              id = ?,
              name = ?,
              address = ?,
              email = ?,
              password = ?
        WHERE id = ?
        """, (new_customer["id"], new_customer["name"], new_customer["address"], new_customer["email"],
                    new_customer["password"], id))
        
        rowcount = db_cursor.rowcount

        if rowcount == 0:
            return False
        else:
            return True