import sqlite3
import json
from models import Location

LOCATIONS = [
	{
		"id": 1,
		"address": "101 Main St."
	}
]

def get_all_locations():
	with sqlite3.connect("./kennel.db") as conn:

		conn.row_factory = sqlite3.Row
		db_cursor = conn.cursor()

		db_cursor.execute("""
		SELECT
			l.id,
			l.name,
			l.address
		FROM location l
		""")

		dataset = db_cursor.fetchall()

		locations = []

		for row in dataset:
			loc = Location(row["id"], row["name"], row["address"])
			locations.append(loc.__dict__)
		
	return json.dumps(locations)


def get_single_location(id):
	with sqlite3.connect("./kennel.db") as conn:

		conn.row_factory = sqlite3.Row
		db_cursor = conn.cursor()

		db_cursor.execute("""
		SELECT
			l.id,
			l.name,
			l.address
		FROM location l
		WHERE l.id = ?
		""", (id, ))

		data = db_cursor.fetchone()
		loc = Location(data["id"], data["name"], data["address"])
	
	return json.dumps(loc.__dict__)

def create_location(location):

	max_id = LOCATIONS[-1]["id"]
	max_id += 1
	location["id"] = max_id

	LOCATIONS.append(location)

	return location

def delete_location(id):
    with sqlite3.connect("./kennel.db") as conn:
        
        db_cursor = conn.cursor()

        db_cursor.execute("""
        DELETE FROM location
        WHERE id = ?
        """, (id, ))

def update_location(id, new_location):
    with sqlite3.connect("./kennel.db") as conn:

        db_cursor = conn.cursor()

        db_cursor.execute("""
        UPDATE location
            SET
             id = ?,
             name = ?,
             address = ?
        WHERE id = ?
        """, (new_location["id"], new_location["name"], new_location["address"], id))
        
        rowcount = db_cursor.rowcount

        if rowcount == 0:
            return False
        else:
            return True