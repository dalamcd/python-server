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
	location_index = -1

	for index, location in enumerate(LOCATIONS):
		if location["id"] == id:
			location_index = index

	if location_index >= 0:
		LOCATIONS.pop(location_index)

def update_location(id, new_location):

    for index, location in enumerate(LOCATIONS):
        if location["id"] == id:
            LOCATIONS[index] = new_location
            break