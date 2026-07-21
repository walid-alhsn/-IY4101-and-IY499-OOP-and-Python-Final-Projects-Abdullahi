# AIRLINE / FLIGHT BOOKING MANAGEMENT SYSTEM

import json
from pathlib import Path


# FILE PATHS

# The folder containing this Python file
BASE_DIR = Path(__file__).resolve().parent

# The folder where the JSON data files will be stored
DATA_DIR = BASE_DIR / "data"

# Individual JSON file locations
USERS_FILE = DATA_DIR / "users.json"
FLIGHTS_FILE = DATA_DIR / "flights.json"
BOOKINGS_FILE = DATA_DIR / "bookings.json"


# FILE-HANDLING FUNCTIONS

def create_data_files():
    """
    Create the data folder and JSON files if they do not
    already exist.
    """

    # Create the data folder
    DATA_DIR.mkdir(exist_ok=True)

    data_files = [
        USERS_FILE,
        FLIGHTS_FILE,
        BOOKINGS_FILE
    ]

    for file_path in data_files:
        if not file_path.exists():
            with open(file_path, "w", encoding="utf-8") as file:
                json.dump([], file, indent=4)

            print(f"Created: {file_path.name}")


def load_json_file(file_path):
    """
    Load and return data from a JSON file.

    If the file is missing or contains invalid JSON,
    an empty list is returned instead of crashing.
    """

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)

    except FileNotFoundError:
        print(f"Error: {file_path.name} could not be found.")
        return []

    except json.JSONDecodeError:
        print(f"Error: {file_path.name} contains invalid JSON data.")
        return []


def save_json_file(file_path, data):
    """
    Save Python data to a JSON file.

    Returns True when the data is saved successfully.
    Returns False when an error occurs.
    """

    try:
        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)

        return True

    except OSError as error:
        print(f"Error saving {file_path.name}: {error}")
        return False


# PROGRAM START

def main():
    """
    Prepare the data files and test that they can be loaded.
    """

    create_data_files()

    users = load_json_file(USERS_FILE)
    flights = load_json_file(FLIGHTS_FILE)
    bookings = load_json_file(BOOKINGS_FILE)

    print("\nAirline Booking System data loaded successfully.")
    print(f"Registered users: {len(users)}")
    print(f"Available flights: {len(flights)}")
    print(f"Saved bookings: {len(bookings)}")


if __name__ == "__main__":
    main()
