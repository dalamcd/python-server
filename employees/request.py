import sqlite3
import json
from models import Employee

EMPLOYEES = [
    {
        "id": 1,
        "name": "Kyle Simmons",
    },
    {
        "id": 2,
        "name": "Mario Campopiano",
    },
    {
        "id": 3,
        "name": "David Williams",
    }
]


def get_all_employees():
    with sqlite3.connect("./kennel.db") as conn:

        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            e.id,
            e.name,
            e.address,
            e.location_id
        FROM employee e
        """)

        employees = []

        dataset = db_cursor.fetchall()

        for row in dataset:
            emp = Employee(row['id'], row['name'], row['address'],
                            row['location_id'])

            employees.append(emp.__dict__)

    return json.dumps(employees)

def get_single_employee(id):

    with sqlite3.connect("./kennel.db") as conn:
        
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
            SELECT
                e.id,
                e.name,
                e.address,
                e.location_id
            FROM employee e
            WHERE e.id = ?
                """, ( id, ))
        
        data = db_cursor.fetchone()

        emp = Employee(data["id"], data["name"], data["address"], data["location_id"])
    
    return json.dumps(emp.__dict__)
        
def get_employees_by_location(location_id):
    with sqlite3.connect("./kennel.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
            SELECT
                e.id,
                e.name,
                e.address,
                e.location_id
            FROM employee e
            WHERE e.location_id = ?
                """, ( location_id, ))

        employees = []

        dataset = db_cursor.fetchall()

        for row in dataset:
            emp = Employee(row['id'], row['name'], row['address'], row['location_id'])
            employees.append(emp.__dict__)
    return json.dumps(employees)

def create_employee(employee): 

	max_id = EMPLOYEES[-1]["id"]
	max_id += 1
	employee["id"] = max_id
	
	EMPLOYEES.append(employee)

	return employee

def delete_employee(id):
	employee_index = -1

	for index, employee in enumerate(EMPLOYEES):
		if employee["id"] == id:
			employee_index = index

	if employee_index >= 0:
		EMPLOYEES.pop(employee_index)

def update_employee(id, new_employee):

    for index, employee in enumerate(EMPLOYEES):
        if employee["id"] == id:
            EMPLOYEES[index] = new_employee
            break