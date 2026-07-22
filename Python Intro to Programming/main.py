# ==========================================================
# AIRLINE / FLIGHT BOOKING MANAGEMENT SYSTEM
#
# Name: Abdullahi Alhassan
# Student ID: 303069863
# ==========================================================

import calendar
import copy
import hashlib
import hmac
import json
import secrets
import tkinter as tk
import uuid
import webbrowser
from collections import Counter
from datetime import date, datetime, timedelta
from pathlib import Path
from tkinter import messagebox, ttk

APP_TITLE = "Airline Booking Management System"  # Main window title
CONTACT_EMAIL = "qkf526@york.ac.uk"  # Address used by Contact Us
ADMIN_EMAIL = "admin@airline.local"  # Demonstration administrator login
ADMIN_PASSWORD = "Admin123"  # Demonstration administrator password
DEMO_PASSENGER_EMAIL = "passenger@airline.local"  # Tutor passenger login
DEMO_PASSENGER_PASSWORD = "Passenger123"  # Tutor passenger password

BASE_DIR = Path(__file__).resolve().parent  # Folder containing this program
# Storage paths for persisted app data and generated boarding passes.
DATA_DIR = BASE_DIR / "data"  # Persistent JSON storage folder
BOARDING_PASSES_DIR = BASE_DIR / "boarding_passes"  # Exported pass folder
USERS_FILE = DATA_DIR / "users.json"  # Registered user records
FLIGHTS_FILE = DATA_DIR / "flights.json"  # Timetable and seat inventory
BOOKINGS_FILE = DATA_DIR / "bookings.json"  # Passenger booking records

COLOURS = {  # Shared colour palette for a consistent interface
    "primary": "#173B63",
    "primary_dark": "#102A46",
    # Darker action blue keeps white button text easy to read.
    "secondary": "#1F6AC7",
    "secondary_hover": "#1857A4",
    "secondary_pressed": "#124781",
    "accent": "#F2C94C",
    "background": "#F4F7FB",
    "surface": "#FFFFFF",
    "text": "#172033",
    "muted": "#667085",
    "success": "#1F8A5B",
    "danger": "#C83E4D",
    "danger_dark": "#A92F3D",
    "button_neutral": "#E7EDF4",
    "button_neutral_hover": "#D9E2EC",
    "disabled": "#AAB7C4",
    "border": "#D9E2EC",
}


# The app keeps a complete rolling timetable and can also create flights
# automatically when the user searches for a date outside this window.
SCHEDULE_DAYS = 30  # Days generated when the program starts
FLIGHTS_PER_ROUTE_PER_DAY = 2  # Morning and evening services

CITY_DATA = {  # Supported cities, airport codes and regions
    "Abuja": {"code": "ABV", "region": "Nigeria"},
    "Dubai": {"code": "DXB", "region": "Middle East"},
    "Kano": {"code": "KAN", "region": "Nigeria"},
    "Lagos": {"code": "LOS", "region": "Nigeria"},
    "London": {"code": "LON", "region": "Europe"},
    "Manchester": {"code": "MAN", "region": "Europe"},
    "New York": {"code": "NYC", "region": "North America"},
    "Paris": {"code": "PAR", "region": "Europe"},
}

AIRLINES = [  # Demonstration airline codes and names
    ("SK", "SkyLink Airways"),
    ("EA", "Emerald Air"),
    ("AW", "Atlantic Wings"),
    ("HA", "Horizon Airlines"),
]


# ==========================================================
# FILE HANDLING
# ==========================================================

def create_data_files():
    """Create the folders and JSON files used by the program."""
    # Ensure disk storage exists before the app starts.
    DATA_DIR.mkdir(exist_ok=True)
    BOARDING_PASSES_DIR.mkdir(exist_ok=True)

    # Each JSON file begins as an empty list of records.
    for path in (USERS_FILE, FLIGHTS_FILE, BOOKINGS_FILE):
        if not path.exists():
            save_json_file(path, [])


def load_json_file(path):
    """Load a JSON record list safely and return an empty list on failure."""
    try:
        with open(path, "r", encoding="utf-8") as file:
            data = json.load(file)  # Convert JSON text into Python records
        # All application data files must contain a list of records.
        if not isinstance(data, list):
            print(f"Error: {path.name} must contain a JSON list.")
            return []
        return data
    except FileNotFoundError:
        print(f"Error: {path.name} was not found.")
    except json.JSONDecodeError:
        print(f"Error: {path.name} contains invalid JSON.")
    except OSError as error:
        print(f"Error reading {path.name}: {error}")
    return []


def save_json_file(path, data):
    """Save JSON using a temporary file to reduce corruption risk."""
    temporary = path.with_suffix(path.suffix + ".tmp")  # Safer temporary save path
    try:
        path.parent.mkdir(exist_ok=True)
        # Write to a temp file first, then atomically replace the original.
        with open(temporary, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)
        temporary.replace(path)
        return True
    except OSError as error:
        print(f"Error saving {path.name}: {error}")
        try:
            if temporary.exists():
                temporary.unlink()
        except OSError:
            pass
        return False


# ==========================================================
# VALIDATION
# ==========================================================

def validate_name(name):
    """Check whether a full name is valid for registration."""
    # Normalize whitespace and ensure the name is present.
    name = name.strip()
    if not name:
        return False, "Full name cannot be empty."
    if len(name) < 2:
        return False, "Full name must contain at least two characters."

    # Only ordinary name characters are permitted.
    for character in name:
        if not (character.isalpha() or character.isspace() or character in "-'"):
            return False, "Full name can only contain letters, spaces, hyphens and apostrophes."
    return True, ""


def validate_email(email):
    """Validate an email address format for registration and login."""
    # Simple normalized email validation for login and registration.
    email = email.strip()
    if not email:
        return False, "Email address cannot be empty."
    if " " in email:
        return False, "Email address cannot contain spaces."
    if email.count("@") != 1:
        return False, "Email address must contain one @ symbol."
    local, domain = email.split("@")
    if not local or not domain or "." not in domain:
        return False, "Please enter a valid email address."
    if domain.startswith(".") or domain.endswith("."):
        return False, "Please enter a valid email domain."
    return True, ""


def validate_phone(phone):
    """Validate telephone number formatting and length."""
    # Normalize phone formatting and validate digit length.
    phone = phone.strip()
    if not phone:
        return False, "Telephone number cannot be empty."
    cleaned = phone.replace(" ", "").replace("-", "").replace("(", "").replace(")", "")  # Remove allowed separators
    digits = cleaned[1:] if cleaned.startswith("+") else cleaned  # Ignore an optional plus sign
    if not digits.isdigit():
        return False, "Telephone number can only contain numbers."
    if len(digits) < 7 or len(digits) > 15:
        return False, "Telephone number must contain between 7 and 15 digits."
    return True, ""


def validate_password(password):
    """Check that a password meets basic security requirements."""
    # Enforce a basic secure password policy.
    if not password:
        return False, "Password cannot be empty."
    if len(password) < 8:
        return False, "Password must contain at least eight characters."
    if not any(character.isupper() for character in password):
        return False, "Password must contain at least one uppercase letter."
    if not any(character.islower() for character in password):
        return False, "Password must contain at least one lowercase letter."
    if not any(character.isdigit() for character in password):
        return False, "Password must contain at least one number."
    return True, ""


def validate_flight_search(origin, destination, departure_date):
    """Validate search criteria before looking for flights."""
    # Ensure the user picked a valid route and date.
    if not origin.strip():
        return False, "Please select an origin."
    if not destination.strip():
        return False, "Please select a destination."
    if origin.strip().lower() == destination.strip().lower():
        return False, "Origin and destination cannot be the same."
    if not departure_date.strip():
        return False, "Please select a departure date."
    try:
        selected = datetime.strptime(departure_date.strip(), "%Y-%m-%d").date()  # Parse the required format
    except ValueError:
        return False, "Date must use the format YYYY-MM-DD."
    if selected < date.today():
        return False, "Departure date cannot be in the past."
    return True, ""


# ==========================================================
# AUTHENTICATION
# ==========================================================

def normalise_email(email):
    """Normalize email for consistent lookup and comparison."""
    # Normalise email for consistent lookup and comparison.
    return email.strip().lower()


# PBKDF2 implementation informed by the official hashlib documentation and OWASP guidance:
# https://docs.python.org/3/library/hashlib.html
# https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html
def create_password_hash(password, salt):
    """Hash a password using PBKDF2-HMAC-SHA256."""
    # PBKDF2 stores a derived hash instead of the original password.
    return hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        bytes.fromhex(salt),
        600000,  # OWASP-recommended PBKDF2 work factor
    ).hex()


def find_user_by_email(email, users):
    """Linear search for a user account."""
    wanted = normalise_email(email)  # Case-insensitive lookup value
    for user in users:
        if normalise_email(user.get("email", "")) == wanted:
            return user
    return None


# UUID4 identifier use informed by the official Python uuid documentation:
# https://docs.python.org/3/library/uuid.html
def register_user(full_name, email, phone, password, confirm_password, role="passenger"):
    """Create a new user account after validating all registration data."""
    # Run all input validators before creating the account.
    for validator, value in (
        (validate_name, full_name),
        (validate_email, email),
        (validate_phone, phone),
        (validate_password, password),
    ):
        valid, message = validator(value)
        if not valid:
            return False, message

    # Both password fields must match exactly.
    if password != confirm_password:
        return False, "Passwords do not match."

    users = load_json_file(USERS_FILE)  # Existing account records
    if not isinstance(users, list):
        return False, "The user data file has an invalid structure."
    if find_user_by_email(email, users) is not None:
        return False, "An account already exists with this email address."

    # A different random salt protects each stored password hash.
    salt = secrets.token_hex(16)  # Unique random salt for this account
    users.append({
        "user_id": f"USR-{uuid.uuid4().hex[:8].upper()}",  # Random unique user ID
        "full_name": full_name.strip(),
        "email": normalise_email(email),
        "phone": phone.strip(),
        "password_hash": create_password_hash(password, salt),
        "salt": salt,
        "role": role,
        "created_at": datetime.now().isoformat(timespec="seconds"),
    })

    if save_json_file(USERS_FILE, users):
        return True, "Account created successfully."
    return False, "The account could not be saved."


def authenticate_user(email, password):
    """Verify a user's login credentials against stored accounts."""
    # Verify credentials against stored user records.
    if not email.strip() or not password:
        return False, "Email and password are required.", None

    users = load_json_file(USERS_FILE)
    user = find_user_by_email(email, users)

    # Unknown emails and wrong passwords deliberately use the same message.
    if user is None:
        return False, "Invalid email address or password.", None

    salt = user.get("salt", "")
    stored_hash = user.get("password_hash", "")
    if not salt or not stored_hash:
        return False, "The account data is incomplete.", None

    try:
        entered_hash = create_password_hash(password, salt)  # Hash the supplied password identically
    except ValueError:
        return False, "The account data is invalid.", None

    # Timing-resistant comparison informed by the official hmac documentation:
    # https://docs.python.org/3/library/hmac.html
    if not hmac.compare_digest(entered_hash, stored_hash):
        return False, "Invalid email address or password.", None

    return True, "Login successful.", {
        "user_id": user.get("user_id", ""),
        "full_name": user.get("full_name", ""),
        "email": user.get("email", ""),
        "phone": user.get("phone", ""),
        "role": user.get("role", "passenger"),
    }


def ensure_default_admin():
    """Create the default administrator account if it is missing."""
    users = load_json_file(USERS_FILE)
    if find_user_by_email(ADMIN_EMAIL, users) is not None:
        return
    # Create a default admin user only when none exists.
    salt = secrets.token_hex(16)  # Unique random salt for this account
    users.append({
        "user_id": f"USR-{uuid.uuid4().hex[:8].upper()}",  # Random unique user ID
        "full_name": "System Administrator",
        "email": ADMIN_EMAIL,
        "phone": "+440000000000",
        "password_hash": create_password_hash(ADMIN_PASSWORD, salt),
        "salt": salt,
        "role": "admin",
        "created_at": datetime.now().isoformat(timespec="seconds"),
    })
    save_json_file(USERS_FILE, users)


def ensure_default_passenger():
    """Create a passenger account that the tutor can use for testing."""
    users = load_json_file(USERS_FILE)
    if find_user_by_email(DEMO_PASSENGER_EMAIL, users) is not None:
        return

    # The demonstration account is created only when it is missing.
    salt = secrets.token_hex(16)  # Unique random salt for this account
    users.append({
        "user_id": f"USR-{uuid.uuid4().hex[:8].upper()}",  # Random unique user ID
        "full_name": "Demo Passenger",
        "email": DEMO_PASSENGER_EMAIL,
        "phone": "+4407000000000",
        "password_hash": create_password_hash(DEMO_PASSENGER_PASSWORD, salt),
        "salt": salt,
        "role": "passenger",
        "created_at": datetime.now().isoformat(timespec="seconds"),
    })
    save_json_file(USERS_FILE, users)


# ==========================================================
# FLIGHTS, SEARCHING AND SORTING
# ==========================================================

def generate_seat_list(rows=6):
    """Generate seat labels for a standard small aircraft cabin."""
    # Create a fixed list of seat labels for a small cabin.
    seats = []  # Generated seat labels
    for row in range(1, rows + 1):
        for letter in ("A", "B", "C", "D"):
            seats.append(f"{row}{letter}")
    return seats


def get_route_fare_and_duration(origin, destination, route_number):
    """Estimate a sensible demonstration fare, tax and journey duration."""
    origin_region = CITY_DATA[origin]["region"]  # Used to estimate route pricing
    destination_region = CITY_DATA[destination]["region"]
    regions = {origin_region, destination_region}  # Unordered route-region pair

    # Different route groups use different approximate prices and durations.
    if origin_region == destination_region == "Nigeria":
        base_price, tax, duration = 85, 15, 80
    elif origin_region == destination_region == "Europe":
        base_price, tax, duration = 145, 25, 105
    elif regions == {"Europe", "Middle East"}:
        base_price, tax, duration = 390, 45, 420
    elif regions == {"Europe", "North America"}:
        base_price, tax, duration = 495, 60, 465
    elif regions == {"Nigeria", "Europe"}:
        base_price, tax, duration = 335, 45, 390
    elif regions == {"Nigeria", "Middle East"}:
        base_price, tax, duration = 360, 45, 430
    elif regions == {"Nigeria", "North America"}:
        base_price, tax, duration = 610, 70, 690
    elif regions == {"Middle East", "North America"}:
        base_price, tax, duration = 650, 75, 780
    else:
        base_price, tax, duration = 250, 35, 300

    # Small deterministic variations stop every route having the same fare.
    base_price += (route_number % 5) * 8
    duration += (route_number % 4) * 10
    return float(base_price), float(tax), duration


def build_flights_for_date(flight_date):
    """Create two flights for every ordered origin/destination combination."""
    seats = generate_seat_list(6)
    cities = sorted(CITY_DATA)  # Stable order keeps route numbering repeatable
    flights = []  # Generated or loaded flight records
    route_number = 0  # Ordered route sequence number

    for origin in cities:
        for destination in cities:
            if origin == destination:
                continue

            route_number += 1
            base_price, airport_tax, duration = get_route_fare_and_duration(
                origin, destination, route_number
            )

            for service_number in range(FLIGHTS_PER_ROUTE_PER_DAY):
                airline_index = (route_number + flight_date.toordinal() + service_number) % len(AIRLINES)  # Rotate airlines predictably
                airline_code, airline_name = AIRLINES[airline_index]

                # One morning and one evening service are produced for each route.
                departure_hour = 7 if service_number == 0 else 17  # Morning or evening service
                departure_minute = (route_number * 7 + flight_date.day * 3) % 60
                departure_text = f"{departure_hour:02d}:{departure_minute:02d}"
                departure_datetime = datetime.combine(
                    flight_date,
                    datetime.strptime(departure_text, "%H:%M").time(),
                )
                arrival_datetime = departure_datetime + timedelta(minutes=duration)  # Derive arrival time

                # The ID includes route, date and service, so it stays unique.
                flight_id = (
                    f"{airline_code}{route_number:02d}"
                    f"{flight_date.strftime('%y%j')}{service_number + 1}"
                )
                booked_seats = (route_number + flight_date.day + service_number * 4) % 9  # Simulated initial demand

                flights.append({
                    "flight_id": flight_id,
                    "airline": airline_name,
                    "origin": origin,
                    "destination": destination,
                    "departure_date": flight_date.isoformat(),
                    "departure_time": departure_text,
                    "arrival_time": arrival_datetime.strftime("%H:%M"),
                    "arrival_day_offset": (arrival_datetime.date() - flight_date).days,
                    "duration_minutes": duration,
                    "gate": f"{chr(65 + route_number % 4)}{(route_number * 3 + service_number) % 20 + 1:02d}",
                    "base_price": base_price + service_number * 15.0,
                    "airport_tax": airport_tax,
                    "total_seats": len(seats),
                    "available_seats": seats[booked_seats:].copy(),
                })

    return flights


def build_sample_flights(days=SCHEDULE_DAYS):
    """Create a complete rolling schedule beginning today."""
    flights = []  # Generated or loaded flight records
    for day_offset in range(days):
        flights.extend(build_flights_for_date(date.today() + timedelta(days=day_offset)))
    return flights


def merge_missing_flights(new_flights):
    """Add missing services while preserving seats already reserved by users."""
    flights = load_json_file(FLIGHTS_FILE)
    existing_ids = {flight.get("flight_id") for flight in flights}  # Prevent duplicate services
    changed = False

    for new_flight in new_flights:
        if new_flight["flight_id"] not in existing_ids:
            flights.append(new_flight)
            existing_ids.add(new_flight["flight_id"])
            changed = True

    if changed:
        save_json_file(FLIGHTS_FILE, flights)
    return flights


def ensure_sample_flights():
    """Ensure every route has two flights per day for the next 30 days."""
    merge_missing_flights(build_sample_flights())


def ensure_flights_for_date(departure_date):
    """Generate a complete timetable for a valid date searched by the user."""
    try:
        selected_date = datetime.strptime(departure_date, "%Y-%m-%d").date()  # Convert search text to a date
    except ValueError:
        return

    if selected_date >= date.today():
        merge_missing_flights(build_flights_for_date(selected_date))


def get_flight_locations():
    """Return every supported city for both search boxes."""
    locations = sorted(CITY_DATA)  # Same cities fill both route boxes
    return locations.copy(), locations.copy()


def search_flights(origin, destination, departure_date):
    """Linear search through every flight record."""
    # A date outside the rolling window is generated automatically on demand.
    ensure_flights_for_date(departure_date.strip())
    results = []  # Matching flight records
    for flight in load_json_file(FLIGHTS_FILE):
        if (
            flight.get("origin", "").lower() == origin.strip().lower()
            and flight.get("destination", "").lower() == destination.strip().lower()
            and flight.get("departure_date", "") == departure_date.strip()
        ):
            results.append(flight)
    return results


def find_alternative_flights(origin, destination, excluded_date=None):
    """Find other flights for the same route on different dates."""
    # Return a short list of other matching flights on different dates.
    alternatives = []
    for flight in load_json_file(FLIGHTS_FILE):
        if (
            flight.get("origin", "").lower() == origin.lower()
            and flight.get("destination", "").lower() == destination.lower()
            and flight.get("departure_date") != excluded_date
            and flight.get("available_seats")
        ):
            alternatives.append(flight)
    return sorted(alternatives, key=lambda item: (item["departure_date"], item["departure_time"]))[:5]


def bubble_sort_flights(flights, option):
    """Sort a copy of the results using bubble sort."""
    result = flights.copy()  # Preserve the original search list
    for pass_number in range(len(result) - 1):
        swapped = False  # Enables early exit when already sorted
        for index in range(len(result) - 1 - pass_number):
            first = result[index]
            second = result[index + 1]
            if option == "Price: Low to High":
                should_swap = first["base_price"] > second["base_price"]
            elif option == "Price: High to Low":
                should_swap = first["base_price"] < second["base_price"]
            elif option == "Departure Time":
                should_swap = first["departure_time"] > second["departure_time"]
            elif option == "Airline: A to Z":
                should_swap = first["airline"].lower() > second["airline"].lower()
            else:
                should_swap = (first["departure_date"], first["departure_time"]) > (second["departure_date"], second["departure_time"])

            # Adjacent flights are exchanged when in the wrong order.
            if should_swap:
                result[index], result[index + 1] = result[index + 1], result[index]
                swapped = True
        if not swapped:
            break
    return result


# ==========================================================
# FARES AND BOOKINGS
# ==========================================================

def calculate_total_fare(flight, seat):
    """Compute the total fare for a flight and seat choice."""
    # Determine price adjustments based on demand and seat type.
    base_price = float(flight.get("base_price", 0))
    airport_tax = float(flight.get("airport_tax", 0))
    total_seats = max(int(flight.get("total_seats", 0)), 1)
    available_percentage = len(flight.get("available_seats", [])) / total_seats * 100  # Demand indicator

    # Increase the fare gradually as fewer seats remain available.
    if available_percentage > 60:
        rate = 0.00
    elif available_percentage > 30:
        rate = 0.10
    elif available_percentage > 10:
        rate = 0.20
    else:
        rate = 0.30

    demand = round(base_price * rate, 2)  # Availability-based fare increase
    # Window seats are charged at a premium over aisle/middle seats.
    seat_charge = 15.0 if seat and seat[-1].upper() in ("A", "D") else 5.0
    total = round(base_price + airport_tax + demand + seat_charge, 2)  # Final payable fare
    return {
        "base_price": base_price,
        "airport_tax": airport_tax,
        "demand_rate": int(rate * 100),
        "demand_adjustment": demand,
        "seat_charge": seat_charge,
        "total_price": total,
    }


def generate_booking_reference(bookings):
    """Generate a unique booking reference not currently in use."""
    # A set makes duplicate-reference checks fast.
    existing = {booking.get("booking_reference") for booking in bookings}  # Fast duplicate check
    for _ in range(100):
        reference = f"BK-{uuid.uuid4().hex[:8].upper()}"  # Random booking reference
        if reference not in existing:
            return reference
    return None


def recursive_binary_search_booking(bookings, target, low, high):
    """Recursive binary search used for booking references."""
    if low > high:
        return None
    middle = (low + high) // 2  # Midpoint of the current search range
    middle_reference = bookings[middle].get("booking_reference", "")
    if middle_reference == target:
        return bookings[middle]
    if target < middle_reference:
        return recursive_binary_search_booking(bookings, target, low, middle - 1)
    return recursive_binary_search_booking(bookings, target, middle + 1, high)


def find_booking_by_reference(reference):
    """Look up a booking using its unique booking reference."""
    # Binary search requires the booking references to be sorted first.
    bookings = sorted(load_json_file(BOOKINGS_FILE), key=lambda item: item.get("booking_reference", ""))
    return recursive_binary_search_booking(bookings, reference.strip().upper(), 0, len(bookings) - 1)


def create_booking(user, flight_id, seat):
    """Reserve a seat on a flight and create a booking record."""
    flights = load_json_file(FLIGHTS_FILE)
    bookings = load_json_file(BOOKINGS_FILE)
    selected = next((flight for flight in flights if flight.get("flight_id") == flight_id), None)  # Requested flight
    if selected is None:
        return False, "The selected flight could not be found.", None
    if seat not in selected.get("available_seats", []):
        return False, "The selected seat is no longer available.", None

    reference = generate_booking_reference(bookings)
    if reference is None:
        return False, "A unique booking reference could not be generated.", None

    fare = calculate_total_fare(selected, seat)  # Fare stored with the booking
    booking = {
        "booking_reference": reference,
        "user_id": user["user_id"],
        "passenger_name": user["full_name"],
        "email": user["email"],
        "phone": user["phone"],
        "flight_id": selected["flight_id"],
        "airline": selected["airline"],
        "origin": selected["origin"],
        "destination": selected["destination"],
        "departure_date": selected["departure_date"],
        "departure_time": selected["departure_time"],
        "arrival_time": selected["arrival_time"],
        "gate": selected["gate"],
        "seat": seat,
        **fare,
        "status": "Booked",
        "checked_in": False,
        "booking_created_at": datetime.now().isoformat(timespec="seconds"),
        "change_history": [],
    }

    # Keep copies so both files can be restored if either save fails.
    original_flights = copy.deepcopy(flights)  # Rollback copy of seat inventory
    original_bookings = copy.deepcopy(bookings)  # Rollback copy of bookings
    # Reserve the chosen seat and queue the booking for persistence.
    selected["available_seats"].remove(seat)
    bookings.append(booking)

    # Roll back the first file if the second save fails.
    if not save_json_file(FLIGHTS_FILE, flights):
        return False, "The seat could not be reserved.", None
    if not save_json_file(BOOKINGS_FILE, bookings):
        save_json_file(FLIGHTS_FILE, original_flights)
        save_json_file(BOOKINGS_FILE, original_bookings)
        return False, "The booking could not be saved.", None
    return True, "Your booking has been confirmed.", booking


def get_user_bookings(user_id):
    """Return all bookings that belong to a given user."""
    # Return all bookings owned by a specific user.
    return [booking for booking in load_json_file(BOOKINGS_FILE) if booking.get("user_id") == user_id]


def seat_sort_key(seat):
    """Create a sortable key from a seat label like 12A."""
    # Sort seat strings by row number then seat letter.
    number = "".join(character for character in seat if character.isdigit())
    letter = "".join(character for character in seat if character.isalpha())
    return int(number or 0), letter


def cancel_booking(user_id, reference):
    """Cancel a user's booking and return the seat to availability."""
    # Cancel a booking and restore the seat to the flight if possible.
    flights = load_json_file(FLIGHTS_FILE)
    bookings = load_json_file(BOOKINGS_FILE)
    booking = next((item for item in bookings if item.get("booking_reference") == reference and item.get("user_id") == user_id), None)
    if booking is None:
        return False, "The booking could not be found."
    if booking.get("status") == "Cancelled":
        return False, "This booking has already been cancelled."
    if booking.get("checked_in"):
        return False, "A checked-in booking cannot be cancelled here."

    original_flights = copy.deepcopy(flights)  # Rollback copy of seat inventory
    original_bookings = copy.deepcopy(bookings)  # Rollback copy of bookings
    flight = next((item for item in flights if item.get("flight_id") == booking.get("flight_id")), None)
    if flight is not None and booking.get("seat") not in flight.get("available_seats", []):
        flight.setdefault("available_seats", []).append(booking["seat"])
        flight["available_seats"].sort(key=seat_sort_key)
    booking["status"] = "Cancelled"
    booking["cancelled_at"] = datetime.now().isoformat(timespec="seconds")

    if not save_json_file(FLIGHTS_FILE, flights) or not save_json_file(BOOKINGS_FILE, bookings):
        save_json_file(FLIGHTS_FILE, original_flights)
        save_json_file(BOOKINGS_FILE, original_bookings)
        return False, "The cancellation could not be saved."
    return True, "The booking has been cancelled."


def get_change_alternatives(booking):
    """Find replacement flights for the same route with available seats."""
    alternatives = []
    for flight in load_json_file(FLIGHTS_FILE):
        if (
            flight.get("flight_id") != booking.get("flight_id")
            and flight.get("origin") == booking.get("origin")
            and flight.get("destination") == booking.get("destination")
            and flight.get("departure_date", "") >= date.today().isoformat()
            and flight.get("available_seats")
        ):
            alternatives.append(flight)
    return bubble_sort_flights(alternatives, "Date")


def change_booking(user_id, reference, new_flight_id, new_seat):
    """Move an existing booking to a different flight and seat."""
    # Change a booking to another flight and adjust the seat inventory.
    flights = load_json_file(FLIGHTS_FILE)
    bookings = load_json_file(BOOKINGS_FILE)
    booking = next((item for item in bookings if item.get("booking_reference") == reference and item.get("user_id") == user_id), None)
    if booking is None:
        return False, "The booking could not be found.", 0.0
    if booking.get("status") == "Cancelled" or booking.get("checked_in"):
        return False, "This booking cannot be changed.", 0.0

    old_flight = next((item for item in flights if item.get("flight_id") == booking.get("flight_id")), None)
    new_flight = next((item for item in flights if item.get("flight_id") == new_flight_id), None)
    if new_flight is None or new_seat not in new_flight.get("available_seats", []):
        return False, "The replacement flight or seat is no longer available.", 0.0

    original_flights = copy.deepcopy(flights)  # Rollback copy of seat inventory
    original_bookings = copy.deepcopy(bookings)  # Rollback copy of bookings
    old_total = float(booking.get("total_price", 0))
    old_seat = booking.get("seat", "")

    if old_flight is not None and old_seat not in old_flight.get("available_seats", []):
        old_flight.setdefault("available_seats", []).append(old_seat)
        old_flight["available_seats"].sort(key=seat_sort_key)
    new_flight["available_seats"].remove(new_seat)
    fare = calculate_total_fare(new_flight, new_seat)
    difference = round(fare["total_price"] - old_total, 2)  # Charge or refund difference

    booking.setdefault("change_history", []).append({
        "changed_at": datetime.now().isoformat(timespec="seconds"),
        "old_flight_id": booking.get("flight_id"),
        "old_seat": old_seat,
        "old_total_price": old_total,
    })
    booking.update({
        "flight_id": new_flight["flight_id"],
        "airline": new_flight["airline"],
        "origin": new_flight["origin"],
        "destination": new_flight["destination"],
        "departure_date": new_flight["departure_date"],
        "departure_time": new_flight["departure_time"],
        "arrival_time": new_flight["arrival_time"],
        "gate": new_flight["gate"],
        "seat": new_seat,
        **fare,
        "status": "Booked",
        "changed_at": datetime.now().isoformat(timespec="seconds"),
    })

    if not save_json_file(FLIGHTS_FILE, flights) or not save_json_file(BOOKINGS_FILE, bookings):
        save_json_file(FLIGHTS_FILE, original_flights)
        save_json_file(BOOKINGS_FILE, original_bookings)
        return False, "The booking change could not be saved.", 0.0
    return True, "The booking has been changed.", difference


def check_in_booking(user_id, reference):
    """Mark a booking as checked in and persist the status."""
    # Mark a booking as checked in and save the updated record.
    bookings = load_json_file(BOOKINGS_FILE)
    booking = next((item for item in bookings if item.get("booking_reference") == reference and item.get("user_id") == user_id), None)
    if booking is None:
        return False, "The booking could not be found.", None
    if booking.get("status") == "Cancelled":
        return False, "A cancelled booking cannot be checked in.", None
    if booking.get("checked_in"):
        return False, "This booking has already been checked in.", booking
    # The booking status and check-in flag are saved together.
    booking["checked_in"] = True
    booking["status"] = "Checked In"
    booking["checked_in_at"] = datetime.now().isoformat(timespec="seconds")
    if not save_json_file(BOOKINGS_FILE, bookings):
        return False, "The check-in could not be saved.", None
    return True, "Check-in completed successfully.", booking


def save_boarding_pass_file(booking):
    """Write a plain-text boarding pass file for a checked-in booking."""
    # Write a simple text boarding pass for checked-in bookings.
    if not booking.get("checked_in"):
        return False, "You must check in first.", None
    path = BOARDING_PASSES_DIR / f"boarding_pass_{booking['booking_reference']}.txt"  # Unique export path
    text = (
        "==================================================\n"
        "                  BOARDING PASS\n"
        "==================================================\n"
        f"Passenger:       {booking['passenger_name']}\n"
        f"Booking Ref:     {booking['booking_reference']}\n"
        f"Airline:         {booking['airline']}\n"
        f"Flight:          {booking['flight_id']}\n"
        f"From:            {booking['origin']}\n"
        f"To:              {booking['destination']}\n"
        f"Date:            {booking['departure_date']}\n"
        f"Departure:       {booking['departure_time']}\n"
        f"Gate:            {booking['gate']}\n"
        f"Seat:            {booking['seat']}\n"
        "==================================================\n"
    )
    try:
        path.write_text(text, encoding="utf-8")
        return True, "Boarding pass saved successfully.", path
    except OSError as error:
        return False, f"The boarding pass could not be saved: {error}", None


# ==========================================================
# POP-UP CALENDAR
# ==========================================================

class CalendarPopup(tk.Toplevel):
    """Display a modal calendar that writes a selected date into an entry field."""
    def __init__(self, parent, target_entry):
        """Initialise the calendar popup with the current month and year."""
        super().__init__(parent)
        self.target_entry = target_entry  # Entry updated after selection
        self.month = date.today().month  # Month currently displayed
        self.year = date.today().year  # Year currently displayed
        self.title("Select a date")
        self.resizable(False, False)
        self.configure(bg=COLOURS["surface"])
        self.transient(parent)
        self.grab_set()
        self.frame = tk.Frame(self, bg=COLOURS["surface"], padx=12, pady=12)
        self.frame.pack()
        self.draw()

    def draw(self):
        """Redraw the calendar controls and day buttons for the selected month."""
        for widget in self.frame.winfo_children():
            widget.destroy()
        header = tk.Frame(self.frame, bg=COLOURS["surface"])
        header.grid(row=0, column=0, columnspan=7, sticky="ew", pady=(0, 8))
        tk.Button(header, text="‹", command=self.previous, relief="flat", width=3).pack(side="left")
        tk.Label(header, text=f"{calendar.month_name[self.month]} {self.year}", bg=COLOURS["surface"], font=("Arial", 13, "bold")).pack(side="left", expand=True, padx=22)
        tk.Button(header, text="›", command=self.next, relief="flat", width=3).pack(side="right")

        for column, weekday in enumerate(("Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun")):
            tk.Label(self.frame, text=weekday, bg=COLOURS["surface"], fg=COLOURS["muted"], width=4, font=("Arial", 9, "bold")).grid(row=1, column=column)

        for row, week in enumerate(calendar.monthcalendar(self.year, self.month), start=2):
            for column, day_number in enumerate(week):
                if day_number == 0:
                    tk.Label(self.frame, text="", bg=COLOURS["surface"], width=4).grid(row=row, column=column)
                    continue
                selected = date(self.year, self.month, day_number)
                is_past = selected < date.today()  # Past dates are disabled
                tk.Button(
                    self.frame,
                    text=str(day_number),
                    width=4,
                    relief="flat",
                    state="disabled" if is_past else "normal",
                    bg=COLOURS["surface"] if is_past else COLOURS["background"],
                    # Capture this date now instead of the loop's final value.
                    command=lambda chosen=selected: self.choose(chosen),
                ).grid(row=row, column=column, padx=2, pady=2)

    def previous(self):
        """Move the calendar to the previous month."""
        if self.month == 1:
            self.month, self.year = 12, self.year - 1
        else:
            self.month -= 1
        self.draw()

    def next(self):
        """Move the calendar to the next month."""
        if self.month == 12:
            self.month, self.year = 1, self.year + 1
        else:
            self.month += 1
        self.draw()

    def choose(self, selected):
        """Write the chosen date to the target entry and close the popup."""
        # Fill the target entry with the selected date and close the popup.
        self.target_entry.delete(0, tk.END)
        self.target_entry.insert(0, selected.isoformat())
        self.destroy()


# ==========================================================
# GUI
# ==========================================================

class AirlineBookingApp:
    """Manage application state, page navigation and all Tkinter user interfaces."""
    def __init__(self, root):
        """Initialise shared application state and open the login page."""
        # Store shared state for the current session and UI selections.
        self.root = root
        self.current_user = None  # Logged-in passenger or administrator
        self.selected_flight = None  # Flight being booked
        self.selected_seat = None  # Seat being booked
        self.fare_details = None  # Current fare breakdown
        self.completed_booking = None  # Most recently confirmed booking
        self.selected_booking = None  # Booking being managed
        self.search_results = []  # Flights currently displayed
        self.last_search = {"origin": "", "destination": "", "date": "", "sort": "Price: Low to High", "results": []}  # Restored after Back

        self.root.title(APP_TITLE)
        self.root.geometry("1100x720")
        self.root.minsize(950, 650)
        self.root.configure(bg=COLOURS["background"])
        self.configure_styles()
        self.show_login_page()

    # Themed-widget styling informed by the official ttk documentation:
    # https://docs.python.org/3/library/tkinter.ttk.html
    def configure_styles(self):
        """Configure reusable ttk styles and accessible button colours."""
        self.style = ttk.Style()
        try:
            # The clam theme respects custom colours consistently across platforms.
            self.style.theme_use("clam")
        except tk.TclError:
            pass

        self.style.configure("TFrame", background=COLOURS["background"])
        self.style.configure("Card.TFrame", background=COLOURS["surface"])
        self.style.configure("TLabel", background=COLOURS["background"], foreground=COLOURS["text"], font=("Arial", 11))
        self.style.configure("Card.TLabel", background=COLOURS["surface"], foreground=COLOURS["text"], font=("Arial", 11))

        # Default buttons use dark text on a clear neutral background.
        self.style.configure(
            "TButton",
            background=COLOURS["button_neutral"],
            foreground=COLOURS["primary_dark"],
            bordercolor=COLOURS["border"],
            lightcolor=COLOURS["button_neutral"],
            darkcolor=COLOURS["button_neutral"],
            font=("Arial", 10, "bold"),
            padding=8,
        )
        self.style.map(
            "TButton",
            background=[
                ("disabled", COLOURS["button_neutral"]),
                ("pressed", COLOURS["button_neutral_hover"]),
                ("active", COLOURS["button_neutral_hover"]),
            ],
            foreground=[("disabled", COLOURS["disabled"])],
        )

        # Explicit state colours prevent white text appearing on a pale button.
        self.style.configure(
            "Primary.TButton",
            background=COLOURS["secondary"],
            foreground="white",
            bordercolor=COLOURS["secondary"],
            lightcolor=COLOURS["secondary"],
            darkcolor=COLOURS["secondary"],
        )
        self.style.map(
            "Primary.TButton",
            background=[
                ("disabled", COLOURS["disabled"]),
                ("pressed", COLOURS["secondary_pressed"]),
                ("active", COLOURS["secondary_hover"]),
            ],
            foreground=[("disabled", "#F4F7FB"), ("pressed", "white"), ("active", "white")],
        )
        self.style.configure(
            "PrimaryLarge.TButton",
            background=COLOURS["secondary"],
            foreground="white",
            bordercolor=COLOURS["secondary"],
            lightcolor=COLOURS["secondary"],
            darkcolor=COLOURS["secondary"],
            font=("Arial", 12, "bold"),
            padding=(14, 11),
        )
        self.style.map(
            "PrimaryLarge.TButton",
            background=[
                ("disabled", COLOURS["disabled"]),
                ("pressed", COLOURS["secondary_pressed"]),
                ("active", COLOURS["secondary_hover"]),
            ],
            foreground=[("disabled", "#F4F7FB"), ("pressed", "white"), ("active", "white")],
        )

        self.style.configure(
            "Danger.TButton",
            background=COLOURS["danger"],
            foreground="white",
            bordercolor=COLOURS["danger"],
            lightcolor=COLOURS["danger"],
            darkcolor=COLOURS["danger"],
        )
        self.style.map(
            "Danger.TButton",
            background=[("pressed", COLOURS["danger_dark"]), ("active", COLOURS["danger_dark"])],
            foreground=[("pressed", "white"), ("active", "white")],
        )

        self.style.configure(
            "HeaderBack.TButton",
            background=COLOURS["primary_dark"],
            foreground="white",
            bordercolor=COLOURS["primary_dark"],
            font=("Arial", 11, "bold"),
            padding=(13, 8),
        )
        self.style.map(
            "HeaderBack.TButton",
            background=[("pressed", "#0A2037"), ("active", "#214F7C")],
            foreground=[("pressed", "white"), ("active", "white")],
        )
        self.style.configure(
            "Accent.TButton",
            background=COLOURS["accent"],
            foreground=COLOURS["primary_dark"],
            bordercolor=COLOURS["accent"],
            font=("Arial", 10, "bold"),
            padding=(14, 7),
        )
        self.style.map("Accent.TButton", background=[("pressed", "#D9AE2E"), ("active", "#E8BC38")])

        self.style.configure(
            "Link.TButton",
            background=COLOURS["surface"],
            foreground=COLOURS["secondary"],
            borderwidth=0,
            padding=4,
        )
        self.style.map(
            "Link.TButton",
            background=[("pressed", COLOURS["surface"]), ("active", COLOURS["surface"])],
            foreground=[("pressed", COLOURS["secondary_pressed"]), ("active", COLOURS["secondary_hover"])],
        )
        self.style.configure(
            "MutedLink.TButton",
            background=COLOURS["surface"],
            foreground=COLOURS["muted"],
            borderwidth=0,
            font=("Arial", 9),
            padding=3,
        )
        self.style.map(
            "MutedLink.TButton",
            background=[("pressed", COLOURS["surface"]), ("active", COLOURS["surface"])],
            foreground=[("pressed", COLOURS["primary_dark"]), ("active", COLOURS["text"])],
        )
        self.style.configure(
            "AdminCard.TButton",
            background=COLOURS["surface"],
            foreground=COLOURS["primary"],
            bordercolor=COLOURS["border"],
            font=("Arial", 15, "bold"),
            padding=(24, 28),
        )
        self.style.map(
            "AdminCard.TButton",
            background=[("pressed", COLOURS["button_neutral_hover"]), ("active", COLOURS["button_neutral"])],
            foreground=[("pressed", COLOURS["primary_dark"]), ("active", COLOURS["primary_dark"])],
        )

        self.style.configure("TLabelframe", background=COLOURS["surface"])
        self.style.configure("TLabelframe.Label", background=COLOURS["surface"], foreground=COLOURS["text"], font=("Arial", 11, "bold"))
        self.style.configure("Treeview", background=COLOURS["surface"], fieldbackground=COLOURS["surface"], rowheight=28)
        self.style.configure("Treeview.Heading", background=COLOURS["primary"], foreground="white", font=("Arial", 10, "bold"))
        self.style.map("Treeview", background=[("selected", COLOURS["secondary"])], foreground=[("selected", "white")])

    def clear_window(self):
        """Remove widgets and event bindings from the current page."""
        # Remove old page widgets before drawing the next screen.
        self.root.unbind_all("<MouseWheel>")
        for widget in self.root.winfo_children():
            widget.destroy()
        self.root.configure(bg=COLOURS["background"])

    def open_contact_email(self):
        """Open the contact email link or display the address as a fallback."""
        # Open the user's default email client or show the address if that fails.
        link = f"mailto:{CONTACT_EMAIL}?subject=Airline%20Booking%20System%20enquiry"
        try:
            if not webbrowser.open(link):
                raise RuntimeError
        except Exception:
            messagebox.showinfo("Contact Us", f"Please email us at:\n{CONTACT_EMAIL}")

    def make_header(self, title, subtitle="", back_command=None):
        """Create the shared page header with navigation and contact controls."""
        header = tk.Frame(self.root, bg=COLOURS["primary"], height=100)
        header.pack(fill="x")
        header.pack_propagate(False)
        if back_command:
            ttk.Button(
                header,
                text="← Back",
                command=back_command,
                style="HeaderBack.TButton",
                cursor="hand2",
            ).pack(side="left", padx=24)
        text = tk.Frame(header, bg=COLOURS["primary"])
        text.pack(side="left", padx=24, pady=17)
        tk.Label(text, text=title, bg=COLOURS["primary"], fg="white", font=("Arial", 22, "bold")).pack(anchor="w")
        if subtitle:
            tk.Label(text, text=subtitle, bg=COLOURS["primary"], fg="#D7E8FA", font=("Arial", 10)).pack(anchor="w", pady=(4, 0))
        ttk.Button(
            header,
            text="Contact Us",
            command=self.open_contact_email,
            style="Accent.TButton",
            cursor="hand2",
        ).pack(side="right", padx=24)

    def create_tree(self, parent, columns, height=12):
        """Create a reusable scrollable table for displaying records."""
        frame = ttk.Frame(parent)
        frame.pack(fill="both", expand=True)
        tree = ttk.Treeview(frame, columns=tuple(column[0] for column in columns), show="headings", height=height, selectmode="browse")
        for column_id, heading, width, anchor in columns:
            tree.heading(column_id, text=heading)
            tree.column(column_id, width=width, anchor=anchor)
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        return tree

    def create_scrollable(self):
        """Create a vertically scrollable content frame."""
        # Build a scrollable frame for content that may exceed the window height.
        container = tk.Frame(self.root, bg=COLOURS["background"])
        container.pack(fill="both", expand=True)
        canvas = tk.Canvas(container, bg=COLOURS["background"], highlightthickness=0)
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        content = ttk.Frame(canvas)
        window_id = canvas.create_window((0, 0), window=content, anchor="nw")  # Embedded scrollable frame
        content.bind("<Configure>", lambda _event: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.bind("<Configure>", lambda event: canvas.itemconfigure(window_id, width=event.width))
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        canvas.bind_all("<MouseWheel>", lambda event: canvas.yview_scroll(-1 if event.delta > 0 else 1, "units"))
        return content

    # ---------------- LOGIN / SIGN-UP ----------------

    def show_login_page(self):
        """Display the passenger and administrator login page."""
        self.clear_window()
        outer = tk.Frame(self.root, bg=COLOURS["background"])
        outer.pack(fill="both", expand=True)
        hero = tk.Frame(outer, bg=COLOURS["primary"], width=460)
        hero.pack(side="left", fill="both")
        hero.pack_propagate(False)
        tk.Label(hero, text="✈", bg=COLOURS["primary"], fg=COLOURS["accent"], font=("Arial", 54)).pack(anchor="w", padx=52, pady=(110, 10))
        tk.Label(hero, text="Plan. Book.\nFly with confidence.", bg=COLOURS["primary"], fg="white", justify="left", font=("Arial", 29, "bold")).pack(anchor="w", padx=52)
        tk.Label(hero, text="Search multiple airlines, reserve seats,\nmanage bookings, check in and generate\nyour boarding pass in one place.", bg=COLOURS["primary"], fg="#D7E8FA", justify="left", font=("Arial", 11)).pack(anchor="w", padx=52, pady=(24, 0))

        right = tk.Frame(outer, bg=COLOURS["background"])
        right.pack(side="right", fill="both", expand=True)
        card = tk.Frame(right, bg=COLOURS["surface"], highlightbackground=COLOURS["border"], highlightthickness=1, padx=44, pady=38)
        card.place(relx=0.5, rely=0.48, anchor="center", width=470, height=500)
        tk.Label(card, text="Welcome back", bg=COLOURS["surface"], fg=COLOURS["text"], font=("Arial", 25, "bold")).pack(anchor="w")
        tk.Label(card, text="Log in to continue to your dashboard.", bg=COLOURS["surface"], fg=COLOURS["muted"], font=("Arial", 10)).pack(anchor="w", pady=(6, 28))

        tk.Label(card, text="Email address", bg=COLOURS["surface"], fg=COLOURS["text"], font=("Arial", 10, "bold")).pack(anchor="w")
        self.login_email_entry = tk.Entry(card, font=("Arial", 12), relief="solid", bd=1)
        self.login_email_entry.pack(fill="x", ipady=9, pady=(7, 18))
        tk.Label(card, text="Password", bg=COLOURS["surface"], fg=COLOURS["text"], font=("Arial", 10, "bold")).pack(anchor="w")
        self.login_password_entry = tk.Entry(card, font=("Arial", 12), show="*", relief="solid", bd=1)
        self.login_password_entry.pack(fill="x", ipady=9, pady=(7, 12))
        self.login_password_entry.bind("<Return>", lambda _event: self.handle_login())
        ttk.Button(card, text="Log In", command=self.handle_login, style="PrimaryLarge.TButton", cursor="hand2").pack(fill="x", pady=(18, 15))
        ttk.Button(card, text="Create a passenger account", command=self.show_signup_page, style="Link.TButton", cursor="hand2").pack()
        ttk.Button(card, text=f"Contact us: {CONTACT_EMAIL}", command=self.open_contact_email, style="MutedLink.TButton", cursor="hand2").pack(pady=(22, 0))
        self.login_email_entry.focus()

    def handle_login(self):
        """Validate login details and open the correct dashboard."""
        # Authenticate credentials and switch to the appropriate dashboard.
        success, message, user = authenticate_user(self.login_email_entry.get(), self.login_password_entry.get())
        if not success:
            messagebox.showerror("Login Failed", message)
            return
        self.current_user = user  # Start the authenticated session
        if user["role"] == "admin":
            self.show_admin_dashboard()
        else:
            self.show_passenger_dashboard()

    def show_signup_page(self):
        """Display the passenger registration form."""
        # Display a registration form for new passenger accounts.
        self.clear_window()
        self.make_header("Create Passenger Account", "Register once to save and manage bookings.", self.show_login_page)
        card = tk.Frame(self.root, bg=COLOURS["surface"], highlightbackground=COLOURS["border"], highlightthickness=1, padx=42, pady=25)
        card.pack(padx=230, pady=32, fill="both", expand=True)
        self.signup_entries = {}
        for key, label, password_field in (
            ("name", "Full name", False),
            ("email", "Email address", False),
            ("phone", "Telephone number", False),
            ("password", "Password", True),
            ("confirm", "Confirm password", True),
        ):
            tk.Label(card, text=label, bg=COLOURS["surface"], fg=COLOURS["text"], font=("Arial", 9, "bold")).pack(anchor="w", pady=(6, 3))
            entry = tk.Entry(card, font=("Arial", 11), show="*" if password_field else "", relief="solid", bd=1)
            entry.pack(fill="x", ipady=7)
            self.signup_entries[key] = entry
        tk.Label(card, text="Password must have at least 8 characters, uppercase, lowercase and a number.", bg=COLOURS["surface"], fg=COLOURS["muted"], font=("Arial", 9)).pack(anchor="w", pady=(10, 12))
        ttk.Button(card, text="Create Account", command=self.handle_signup, style="PrimaryLarge.TButton", cursor="hand2").pack(fill="x")
        self.signup_entries["name"].focus()

    def handle_signup(self):
        """Validate the form and create a new passenger account."""
        # Attempt to create a new passenger account from the form fields.
        success, message = register_user(
            self.signup_entries["name"].get(),
            self.signup_entries["email"].get(),
            self.signup_entries["phone"].get(),
            self.signup_entries["password"].get(),
            self.signup_entries["confirm"].get(),
        )
        if not success:
            messagebox.showerror("Registration Failed", message)
            return
        email = normalise_email(self.signup_entries["email"].get())
        messagebox.showinfo("Account Created", message)
        self.show_login_page()
        self.login_email_entry.insert(0, email)

    # ---------------- PASSENGER DASHBOARD ----------------

    def show_passenger_dashboard(self):
        """Display the passenger's available services."""
        # Show the main passenger dashboard after login.
        self.clear_window()
        self.make_header("Passenger Dashboard", f"Signed in as {self.current_user['email']}")
        content = tk.Frame(self.root, bg=COLOURS["background"])
        content.pack(fill="both", expand=True, padx=55, pady=35)
        greeting = tk.Frame(content, bg=COLOURS["surface"], highlightbackground=COLOURS["border"], highlightthickness=1, padx=28, pady=20)
        greeting.pack(fill="x")
        tk.Label(greeting, text=f"Welcome, {self.current_user['full_name']}", bg=COLOURS["surface"], fg=COLOURS["text"], font=("Arial", 22, "bold")).pack(anchor="w")
        tk.Label(greeting, text="Choose one of the services below.", bg=COLOURS["surface"], fg=COLOURS["muted"], font=("Arial", 10)).pack(anchor="w", pady=(4, 0))

        grid = tk.Frame(content, bg=COLOURS["background"])
        grid.pack(fill="both", expand=True, pady=25)
        actions = [  # Dashboard cards and their commands
            ("Search & Book", "Compare airlines and reserve a seat.", "✈", lambda: self.show_flight_search_page(False)),
            ("My Bookings", "View, change or cancel bookings.", "▣", self.show_my_bookings_page),
            ("Check In", "Check in using a booking reference.", "✓", self.show_check_in_page),
            ("Contact Us", f"Email {CONTACT_EMAIL}.", "✉", self.open_contact_email),
        ]
        for index, (title, description, icon, command) in enumerate(actions):
            card = tk.Frame(grid, bg=COLOURS["surface"], highlightbackground=COLOURS["border"], highlightthickness=1, padx=24, pady=20)
            card.grid(row=index // 2, column=index % 2, sticky="nsew", padx=10, pady=10)
            tk.Label(card, text=icon, bg=COLOURS["surface"], fg=COLOURS["secondary"], font=("Arial", 27, "bold")).pack(anchor="w")
            tk.Label(card, text=title, bg=COLOURS["surface"], fg=COLOURS["text"], font=("Arial", 16, "bold")).pack(anchor="w", pady=(8, 4))
            tk.Label(card, text=description, bg=COLOURS["surface"], fg=COLOURS["muted"], font=("Arial", 10)).pack(anchor="w")
            ttk.Button(card, text="Open", command=command, style="Primary.TButton", cursor="hand2").pack(anchor="e", pady=(18, 0))
        for column in range(2):
            grid.grid_columnconfigure(column, weight=1)
        for row in range(2):
            grid.grid_rowconfigure(row, weight=1)
        ttk.Button(content, text="Log Out", command=self.logout, style="Danger.TButton", cursor="hand2").pack(anchor="e")

    def logout(self):
        """End the current session and return to the login page."""
        self.current_user = None
        self.show_login_page()

    # ---------------- SEARCH / BOOK ----------------

    def show_flight_search_page(self, preserve=False):
        """Display flight-search controls and optionally restore the previous search."""
        # Display the flight search form and results table.
        self.clear_window()
        self.make_header("Search Flights", "Choose a route and select a departure date.", self.show_passenger_dashboard)
        main = ttk.Frame(self.root, padding=24)
        main.pack(fill="both", expand=True)
        form = ttk.LabelFrame(main, text="Journey Details", padding=15)
        form.pack(fill="x", pady=(0, 15))
        origins, destinations = get_flight_locations()  # Populate route selectors
        ttk.Label(form, text="Origin", style="Card.TLabel").grid(row=0, column=0, sticky="w", padx=8)
        ttk.Label(form, text="Destination", style="Card.TLabel").grid(row=0, column=1, sticky="w", padx=8)
        ttk.Label(form, text="Departure date", style="Card.TLabel").grid(row=0, column=2, sticky="w", padx=8)
        self.origin_combobox = ttk.Combobox(form, values=origins, state="readonly", width=23)
        self.destination_combobox = ttk.Combobox(form, values=destinations, state="readonly", width=23)
        self.origin_combobox.grid(row=1, column=0, padx=8, pady=6)
        self.destination_combobox.grid(row=1, column=1, padx=8, pady=6)
        date_frame = ttk.Frame(form, style="Card.TFrame")
        date_frame.grid(row=1, column=2, padx=8, pady=6)
        self.departure_date_entry = ttk.Entry(date_frame, width=17)
        self.departure_date_entry.pack(side="left")
        ttk.Button(date_frame, text="📅", command=lambda: CalendarPopup(self.root, self.departure_date_entry)).pack(side="left", padx=(5, 0))
        ttk.Button(form, text="Search Flights", style="Primary.TButton", command=self.handle_flight_search).grid(row=1, column=3, padx=12)

        if preserve:
            # Restore the previous journey details when the user returns.
            self.origin_combobox.set(self.last_search["origin"])
            self.destination_combobox.set(self.last_search["destination"])
            self.departure_date_entry.insert(0, self.last_search["date"])
            self.search_results = self.last_search["results"].copy()
        else:
            self.search_results = []

        result_frame = ttk.LabelFrame(main, text="Available Flights", padding=10)
        result_frame.pack(fill="both", expand=True)
        self.flight_tree = self.create_tree(result_frame, [
            ("id", "Flight", 80, "center"), ("airline", "Airline", 160, "w"),
            ("date", "Date", 105, "center"), ("depart", "Departure", 90, "center"),
            ("arrive", "Arrival", 90, "center"), ("price", "Base Price", 90, "center"),
            ("seats", "Seats", 65, "center"),
        ], 11)
        controls = ttk.Frame(main)
        controls.pack(fill="x", pady=(12, 0))
        ttk.Label(controls, text="Sort by:").pack(side="left")
        self.sort_combobox = ttk.Combobox(controls, values=["Price: Low to High", "Price: High to Low", "Departure Time", "Airline: A to Z", "Date"], state="readonly", width=22)
        self.sort_combobox.pack(side="left", padx=8)
        self.sort_combobox.set(self.last_search["sort"])
        ttk.Button(controls, text="Sort", command=self.handle_sort).pack(side="left")
        ttk.Button(controls, text="Select Flight", style="Primary.TButton", command=self.handle_flight_selection).pack(side="right")
        if preserve:
            self.display_flights(self.search_results)

    def handle_flight_search(self):
        """Validate criteria, search the timetable and display sorted results."""
        # Validate the search input, then find and display matching flights.
        origin = self.origin_combobox.get()
        destination = self.destination_combobox.get()
        selected_date = self.departure_date_entry.get()
        valid, message = validate_flight_search(origin, destination, selected_date)
        if not valid:
            messagebox.showerror("Invalid Search", message)
            return
        # Apply the displayed sort option immediately to each new search.
        option = self.sort_combobox.get() or "Price: Low to High"  # Default sort order
        self.search_results = bubble_sort_flights(search_flights(origin, destination, selected_date), option)
        self.last_search.update({
            "origin": origin,
            "destination": destination,
            "date": selected_date,
            "sort": option,
            "results": self.search_results.copy(),
        })
        self.display_flights(self.search_results)
        if not self.search_results:
            alternatives = find_alternative_flights(origin, destination, selected_date)
            if alternatives:
                dates = ", ".join(sorted({flight["departure_date"] for flight in alternatives}))
                messagebox.showinfo("No Flights Found", f"No flights were found on that date.\n\nOther available dates: {dates}")
            else:
                messagebox.showinfo("No Flights Found", "No flights were found for the selected route.")

    def display_flights(self, flights):
        """Populate the flight-results table with supplied records."""
        for row in self.flight_tree.get_children():
            self.flight_tree.delete(row)
        for flight in flights:
            self.flight_tree.insert("", "end", values=(flight["flight_id"], flight["airline"], flight["departure_date"], flight["departure_time"], flight["arrival_time"], f"£{flight['base_price']:.2f}", len(flight.get("available_seats", []))))

    def handle_sort(self):
        """Sort the current flight results using the selected option."""
        if not self.search_results:
            messagebox.showerror("No Search Results", "Please search for flights before sorting.")
            return
        option = self.sort_combobox.get()
        self.search_results = bubble_sort_flights(self.search_results, option)
        self.last_search["sort"] = option
        self.last_search["results"] = self.search_results.copy()
        self.display_flights(self.search_results)

    def handle_flight_selection(self):
        """Validate the selected result and continue to seat selection."""
        selected = self.flight_tree.selection()
        if not selected:
            messagebox.showerror("No Flight Selected", "Please select a flight.")
            return
        flight_id = self.flight_tree.item(selected[0], "values")[0]  # ID in the first column
        self.selected_flight = next((flight for flight in self.search_results if flight["flight_id"] == flight_id), None)
        if self.selected_flight is None or not self.selected_flight.get("available_seats"):
            messagebox.showerror("Flight Unavailable", "The selected flight is unavailable.")
            return
        self.selected_seat = None
        self.show_booking_details_page()

    def show_booking_details_page(self):
        """Display flight, passenger, seat and fare information."""
        self.clear_window()
        self.make_header("Complete Your Booking", "Choose a seat and review the fare.", lambda: self.show_flight_search_page(True))
        content = self.create_scrollable()
        main = ttk.Frame(content, padding=25)
        main.pack(fill="both", expand=True)
        flight = self.selected_flight
        info = ttk.LabelFrame(main, text="Selected Flight", padding=18)
        info.pack(fill="x", pady=(0, 15))
        ttk.Label(info, text=f"{flight['flight_id']} — {flight['airline']}\n{flight['origin']} to {flight['destination']}\nDate: {flight['departure_date']}\nDeparture: {flight['departure_time']}    Arrival: {flight['arrival_time']}\nGate: {flight['gate']}", style="Card.TLabel", justify="left").pack(anchor="w")
        passenger = ttk.LabelFrame(main, text="Passenger Details", padding=18)
        passenger.pack(fill="x", pady=(0, 15))
        ttk.Label(passenger, text=f"Name: {self.current_user['full_name']}\nEmail: {self.current_user['email']}\nTelephone: {self.current_user['phone']}", style="Card.TLabel", justify="left").pack(anchor="w")
        fare_frame = ttk.LabelFrame(main, text="Seat and Fare", padding=18)
        fare_frame.pack(fill="x")
        ttk.Label(fare_frame, text="Select an available seat:", style="Card.TLabel").grid(row=0, column=0, sticky="w", padx=(0, 12))
        self.seat_combobox = ttk.Combobox(fare_frame, values=flight["available_seats"], state="readonly", width=20)
        self.seat_combobox.grid(row=0, column=1, sticky="w")
        self.seat_combobox.bind("<<ComboboxSelected>>", self.update_fare)
        ttk.Label(fare_frame, text="Window seats A and D: £15.00\nStandard seats B and C: £5.00", style="Card.TLabel", justify="left").grid(row=1, column=0, columnspan=2, sticky="w", pady=12)
        self.fare_label = ttk.Label(fare_frame, text="Select a seat to calculate the final fare.", style="Card.TLabel", justify="left")
        self.fare_label.grid(row=2, column=0, columnspan=2, sticky="w")
        buttons = ttk.Frame(main)
        buttons.pack(fill="x", pady=18)
        ttk.Button(buttons, text="Back to Search", command=lambda: self.show_flight_search_page(True)).pack(side="left")
        ttk.Button(buttons, text="Review Booking", style="Primary.TButton", command=self.review_booking).pack(side="right")
        if self.selected_seat in flight["available_seats"]:
            self.seat_combobox.set(self.selected_seat)
            self.update_fare()

    def update_fare(self, _event=None):
        """Recalculate and display the fare for the selected seat."""
        seat = self.seat_combobox.get()
        if not seat:
            return
        self.fare_details = calculate_total_fare(self.selected_flight, seat)  # Refresh displayed fare
        fare = self.fare_details
        self.fare_label.configure(text=f"Base fare: £{fare['base_price']:.2f}\nAirport tax: £{fare['airport_tax']:.2f}\nDemand adjustment ({fare['demand_rate']}%): £{fare['demand_adjustment']:.2f}\nSeat charge: £{fare['seat_charge']:.2f}\n--------------------------------\nTotal price: £{fare['total_price']:.2f}")

    def review_booking(self):
        """Recheck seat availability before opening the review page."""
        # Re-check availability before the final booking review step.
        seat = self.seat_combobox.get()
        if not seat:
            messagebox.showerror("No Seat Selected", "Please select a seat.")
            return
        current_flights = load_json_file(FLIGHTS_FILE)
        current = next((flight for flight in current_flights if flight["flight_id"] == self.selected_flight["flight_id"]), None)
        if current is None or seat not in current.get("available_seats", []):
            messagebox.showerror("Seat Unavailable", "The selected seat is no longer available.")
            return
        self.selected_flight = current
        self.selected_seat = seat
        self.fare_details = calculate_total_fare(current, seat)
        self.show_booking_review_page()

    def show_booking_review_page(self):
        """Display the complete booking summary before confirmation."""
        self.clear_window()
        self.make_header("Review Your Booking", "Confirm the journey and price.", self.show_booking_details_page)
        main = ttk.Frame(self.root, padding=30)
        main.pack(fill="both", expand=True)
        flight, fare = self.selected_flight, self.fare_details
        summary = ttk.LabelFrame(main, text="Booking Summary", padding=20)
        summary.pack(fill="x", padx=80, pady=(25, 15))
        ttk.Label(summary, text=f"Passenger: {self.current_user['full_name']}\nFlight: {flight['flight_id']} — {flight['airline']}\nRoute: {flight['origin']} to {flight['destination']}\nDate: {flight['departure_date']}\nDeparture: {flight['departure_time']}\nSeat: {self.selected_seat}\n\nBase fare: £{fare['base_price']:.2f}\nAirport tax: £{fare['airport_tax']:.2f}\nDemand adjustment: £{fare['demand_adjustment']:.2f}\nSeat charge: £{fare['seat_charge']:.2f}\nTotal: £{fare['total_price']:.2f}", style="Card.TLabel", justify="left").pack(anchor="w")
        self.confirm_button = ttk.Button(main, text="Confirm Booking", style="Primary.TButton", command=self.confirm_booking)
        self.confirm_button.pack(pady=20)

    def confirm_booking(self):
        """Confirm and save the selected flight booking."""
        # Create the booking and disable the confirm button while saving.
        if not messagebox.askyesno("Confirm Booking", f"Confirm this booking for £{self.fare_details['total_price']:.2f}?"):
            return
        self.confirm_button.configure(state="disabled")  # Prevent duplicate clicks
        success, message, booking = create_booking(self.current_user, self.selected_flight["flight_id"], self.selected_seat)
        if not success:
            self.confirm_button.configure(state="normal")
            messagebox.showerror("Booking Failed", message)
            return
        self.completed_booking = booking
        self.show_booking_confirmation_page()

    def show_booking_confirmation_page(self):
        """Display the confirmed booking and reference number."""
        self.clear_window()
        self.make_header("Booking Confirmed", "Your seat and booking have been saved.")
        booking = self.completed_booking
        frame = ttk.LabelFrame(self.root, text="Booking Reference", padding=25)
        frame.pack(fill="x", padx=180, pady=(70, 20))
        ttk.Label(frame, text=booking["booking_reference"], style="Card.TLabel", font=("Arial", 25, "bold")).pack()
        ttk.Label(frame, text=f"{booking['flight_id']} — {booking['airline']}\n{booking['origin']} to {booking['destination']}\nDate: {booking['departure_date']}\nSeat: {booking['seat']}\nTotal price: £{booking['total_price']:.2f}", style="Card.TLabel", justify="center").pack(pady=(15, 0))
        ttk.Button(self.root, text="Return to Dashboard", style="Primary.TButton", command=self.finish_booking).pack(pady=20)

    def finish_booking(self):
        """Clear temporary booking state and return to the dashboard."""
        self.selected_flight = self.selected_seat = self.fare_details = self.completed_booking = None
        self.show_passenger_dashboard()

    # ---------------- MY BOOKINGS ----------------

    def show_my_bookings_page(self):
        """Display the passenger's bookings and management controls."""
        self.clear_window()
        self.make_header("My Bookings", "View, change, cancel, check in or open a boarding pass.", self.show_passenger_dashboard)
        main = ttk.Frame(self.root, padding=24)
        main.pack(fill="both", expand=True)
        search = ttk.Frame(main)
        search.pack(fill="x", pady=(0, 12))
        ttk.Label(search, text="Booking reference:").pack(side="left")
        self.booking_search_entry = ttk.Entry(search, width=24)
        self.booking_search_entry.pack(side="left", padx=8)
        ttk.Button(search, text="Search", command=self.filter_bookings).pack(side="left")
        ttk.Button(search, text="Show All", command=self.load_bookings_table).pack(side="left", padx=6)
        frame = ttk.LabelFrame(main, text="Saved Bookings", padding=10)
        frame.pack(fill="both", expand=True)
        self.bookings_tree = self.create_tree(frame, [
            ("ref", "Reference", 125, "center"), ("flight", "Flight", 80, "center"),
            ("route", "Route", 190, "w"), ("date", "Date", 105, "center"),
            ("seat", "Seat", 60, "center"), ("total", "Total", 85, "center"),
            ("status", "Status", 100, "center"),
        ], 12)
        buttons = ttk.Frame(main)
        buttons.pack(fill="x", pady=(14, 0))
        ttk.Button(buttons, text="View Details", command=self.view_booking).pack(side="left")
        ttk.Button(buttons, text="Change Flight", command=self.open_change_booking).pack(side="left", padx=5)
        ttk.Button(buttons, text="Cancel Booking", style="Danger.TButton", command=self.cancel_selected_booking).pack(side="left", padx=5)
        ttk.Button(buttons, text="Check In", command=self.check_in_selected_booking).pack(side="right")
        ttk.Button(buttons, text="Boarding Pass", style="Primary.TButton", command=self.open_selected_boarding_pass).pack(side="right", padx=5)
        self.load_bookings_table()

    def load_bookings_table(self, bookings=None):
        """Load all or filtered passenger bookings into the table."""
        # Populate the booking table with either all user bookings or a filtered list.
        bookings = get_user_bookings(self.current_user["user_id"]) if bookings is None else bookings
        for row in self.bookings_tree.get_children():
            self.bookings_tree.delete(row)
        for booking in bookings:
            self.bookings_tree.insert("", "end", values=(booking["booking_reference"], booking["flight_id"], f"{booking['origin']} → {booking['destination']}", booking["departure_date"], booking["seat"], f"£{booking['total_price']:.2f}", booking["status"]))

    def filter_bookings(self):
        """Find and display a booking by its reference."""
        reference = self.booking_search_entry.get().strip().upper()  # Standardise the search key
        if not reference:
            messagebox.showerror("Reference Required", "Please enter a booking reference.")
            return
        booking = find_booking_by_reference(reference)
        if booking is None or booking.get("user_id") != self.current_user["user_id"]:
            self.load_bookings_table([])
            messagebox.showinfo("Booking Not Found", "No booking was found with that reference.")
            return
        self.load_bookings_table([booking])

    def get_selected_booking(self):
        """Return the booking selected in the bookings table."""
        # Return the currently selected booking entry from the table.
        selected = self.bookings_tree.selection()
        if not selected:
            messagebox.showerror("No Booking Selected", "Please select a booking.")
            return None
        reference = self.bookings_tree.item(selected[0], "values")[0]
        return find_booking_by_reference(reference)

    def view_booking(self):
        """Display complete details for the selected booking."""
        booking = self.get_selected_booking()
        if booking:
            messagebox.showinfo("Booking Details", f"Reference: {booking['booking_reference']}\nPassenger: {booking['passenger_name']}\nFlight: {booking['flight_id']} — {booking['airline']}\nRoute: {booking['origin']} to {booking['destination']}\nDate: {booking['departure_date']}\nDeparture: {booking['departure_time']}\nGate: {booking['gate']}\nSeat: {booking['seat']}\nTotal: £{booking['total_price']:.2f}\nStatus: {booking['status']}")

    def cancel_selected_booking(self):
        """Confirm and cancel the selected eligible booking."""
        booking = self.get_selected_booking()
        if booking is None or not messagebox.askyesno("Cancel Booking", f"Cancel booking {booking['booking_reference']}?"):
            return
        success, message = cancel_booking(self.current_user["user_id"], booking["booking_reference"])
        if not success:
            messagebox.showerror("Cancellation Failed", message)
            return
        messagebox.showinfo("Booking Cancelled", message)
        self.load_bookings_table()

    # ---------------- CHANGE FLIGHT ----------------

    def open_change_booking(self):
        """Validate eligibility and begin the booking-change process."""
        # Initiate the booking change flow for an eligible reservation.
        booking = self.get_selected_booking()
        if booking is None:
            return
        if booking.get("status") == "Cancelled" or booking.get("checked_in"):
            messagebox.showerror("Change Not Allowed", "This booking cannot be changed.")
            return
        self.selected_booking = booking
        self.show_change_booking_page()

    def show_change_booking_page(self):
        """Display alternative flights and replacement-seat controls."""
        self.clear_window()
        booking = self.selected_booking
        self.make_header("Change Flight", f"Booking {booking['booking_reference']}: {booking['origin']} to {booking['destination']}", self.show_my_bookings_page)
        main = ttk.Frame(self.root, padding=24)
        main.pack(fill="both", expand=True)
        frame = ttk.LabelFrame(main, text="Alternative Flights", padding=10)
        frame.pack(fill="both", expand=True)
        self.alternatives = get_change_alternatives(booking)  # Same route on other services
        self.change_tree = self.create_tree(frame, [
            ("id", "Flight", 80, "center"), ("airline", "Airline", 160, "w"),
            ("date", "Date", 105, "center"), ("depart", "Departure", 90, "center"),
            ("price", "Base Price", 90, "center"), ("seats", "Seats", 65, "center"),
        ], 9)
        self.change_tree.bind("<<TreeviewSelect>>", self.select_change_flight)
        for flight in self.alternatives:
            self.change_tree.insert("", "end", values=(flight["flight_id"], flight["airline"], flight["departure_date"], flight["departure_time"], f"£{flight['base_price']:.2f}", len(flight["available_seats"])))
        controls = ttk.LabelFrame(main, text="Replacement Seat and Price", padding=15)
        controls.pack(fill="x", pady=(15, 0))
        ttk.Label(controls, text="Seat:", style="Card.TLabel").grid(row=0, column=0, padx=(0, 8))
        self.change_seat_combobox = ttk.Combobox(controls, state="readonly", width=18)
        self.change_seat_combobox.grid(row=0, column=1)
        self.change_seat_combobox.bind("<<ComboboxSelected>>", self.update_change_price)
        self.change_price_label = ttk.Label(controls, text="Select an alternative flight and seat.", style="Card.TLabel")
        self.change_price_label.grid(row=1, column=0, columnspan=3, sticky="w", pady=(12, 0))
        ttk.Button(controls, text="Confirm Flight Change", style="Primary.TButton", command=self.confirm_change).grid(row=0, column=2, padx=(20, 0))
        if not self.alternatives:
            messagebox.showinfo("No Alternatives", "No alternative flights are currently available for this route.")

    def select_change_flight(self, _event=None):
        """Load available seats for the selected replacement flight."""
        selected = self.change_tree.selection()
        if not selected:
            return
        flight_id = self.change_tree.item(selected[0], "values")[0]
        self.selected_change_flight = next((flight for flight in self.alternatives if flight["flight_id"] == flight_id), None)
        if self.selected_change_flight:
            self.change_seat_combobox.configure(values=self.selected_change_flight["available_seats"])
            self.change_seat_combobox.set("")

    def update_change_price(self, _event=None):
        """Preview the new fare and any payment or refund difference."""
        # Update the price preview for the selected replacement flight and seat.
        if not getattr(self, "selected_change_flight", None) or not self.change_seat_combobox.get():
            return
        fare = calculate_total_fare(self.selected_change_flight, self.change_seat_combobox.get())
        difference = round(fare["total_price"] - float(self.selected_booking["total_price"]), 2)
        text = f"New total: £{fare['total_price']:.2f}\n"
        text += f"Additional amount: £{difference:.2f}" if difference > 0 else (f"Refund difference: £{abs(difference):.2f}" if difference < 0 else "No price difference.")
        self.change_price_label.configure(text=text)

    def confirm_change(self):
        """Confirm and save the selected flight change."""
        # Commit the booking change once the user confirms it.
        flight = getattr(self, "selected_change_flight", None)
        seat = self.change_seat_combobox.get()
        if flight is None or not seat:
            messagebox.showerror("Selection Required", "Please select a replacement flight and seat.")
            return
        if not messagebox.askyesno("Confirm Flight Change", f"Move this booking to flight {flight['flight_id']}?"):
            return
        success, message, difference = change_booking(self.current_user["user_id"], self.selected_booking["booking_reference"], flight["flight_id"], seat)
        if not success:
            messagebox.showerror("Change Failed", message)
            return
        if difference > 0:
            message += f"\nAdditional amount: £{difference:.2f}"
        elif difference < 0:
            message += f"\nRefund difference: £{abs(difference):.2f}"
        messagebox.showinfo("Booking Changed", message)
        self.show_my_bookings_page()

    # ---------------- CHECK-IN / BOARDING PASS ----------------

    def show_check_in_page(self):
        """Display reference-based and table-based check-in options."""
        # Display the online check-in screen with a reference entry and active bookings.
        self.clear_window()
        self.make_header("Online Check-In", "Enter a reference or select an active booking.", self.show_passenger_dashboard)
        main = ttk.Frame(self.root, padding=30)
        main.pack(fill="both", expand=True)
        form = ttk.LabelFrame(main, text="Booking Reference", padding=18)
        form.pack(fill="x", padx=120, pady=(20, 18))
        self.check_in_entry = ttk.Entry(form, width=25)
        self.check_in_entry.pack(side="left", padx=(0, 10))
        ttk.Button(form, text="Check In", style="Primary.TButton", command=lambda: self.perform_check_in(self.check_in_entry.get().strip().upper())).pack(side="left")
        frame = ttk.LabelFrame(main, text="Your Active Bookings", padding=10)
        frame.pack(fill="both", expand=True)
        self.check_in_tree = self.create_tree(frame, [
            ("ref", "Reference", 125, "center"), ("flight", "Flight", 80, "center"),
            ("route", "Route", 200, "w"), ("date", "Date", 105, "center"),
            ("seat", "Seat", 65, "center"), ("status", "Status", 100, "center"),
        ], 9)
        for booking in get_user_bookings(self.current_user["user_id"]):
            if booking.get("status") != "Cancelled":
                self.check_in_tree.insert("", "end", values=(booking["booking_reference"], booking["flight_id"], f"{booking['origin']} → {booking['destination']}", booking["departure_date"], booking["seat"], booking["status"]))
        ttk.Button(main, text="Check In Selected Booking", command=self.check_in_from_tree).pack(pady=14)

    def check_in_from_tree(self):
        """Check in the booking selected in the active-bookings table."""
        selected = self.check_in_tree.selection()
        if not selected:
            messagebox.showerror("No Booking Selected", "Please select a booking.")
            return
        self.perform_check_in(self.check_in_tree.item(selected[0], "values")[0])

    def check_in_selected_booking(self):
        """Check in the booking selected on the My Bookings page."""
        booking = self.get_selected_booking()
        if booking:
            self.perform_check_in(booking["booking_reference"])

    def perform_check_in(self, reference):
        """Validate the reference, save check-in and show the boarding pass."""
        # Validate and save check-in status, then show the boarding pass.
        if not reference:
            messagebox.showerror("Reference Required", "Please enter a booking reference.")
            return
        success, message, booking = check_in_booking(self.current_user["user_id"], reference)
        if not success:
            messagebox.showerror("Check-In Failed", message)
            return
        messagebox.showinfo("Check-In Complete", message)
        self.show_boarding_pass_page(booking)

    def open_selected_boarding_pass(self):
        """Open the boarding pass for a checked-in booking."""
        booking = self.get_selected_booking()
        if booking is None:
            return
        if not booking.get("checked_in"):
            messagebox.showerror("Boarding Pass Unavailable", "You must check in before viewing the boarding pass.")
            return
        self.show_boarding_pass_page(booking)

    def show_boarding_pass_page(self, booking):
        """Display formatted boarding-pass details."""
        # Show a boarding pass summary for a checked-in booking.
        self.clear_window()
        self.make_header("Boarding Pass", f"Booking {booking['booking_reference']}", self.show_my_bookings_page)
        outer = tk.Frame(self.root, bg=COLOURS["background"])
        outer.pack(fill="both", expand=True, padx=90, pady=45)
        card = tk.Frame(outer, bg=COLOURS["surface"], highlightbackground=COLOURS["border"], highlightthickness=1)
        card.pack(fill="both", expand=True)
        top = tk.Frame(card, bg=COLOURS["primary"], height=85)
        top.pack(fill="x")
        top.pack_propagate(False)
        tk.Label(top, text=booking["airline"], bg=COLOURS["primary"], fg="white", font=("Arial", 21, "bold")).pack(side="left", padx=28)
        tk.Label(top, text="BOARDING PASS", bg=COLOURS["primary"], fg=COLOURS["accent"], font=("Arial", 14, "bold")).pack(side="right", padx=28)
        body = tk.Frame(card, bg=COLOURS["surface"], padx=34, pady=28)
        body.pack(fill="both", expand=True)
        fields = [("Passenger", booking["passenger_name"]), ("Booking Reference", booking["booking_reference"]), ("Flight", booking["flight_id"]), ("From", booking["origin"]), ("To", booking["destination"]), ("Date", booking["departure_date"]), ("Departure", booking["departure_time"]), ("Gate", booking["gate"]), ("Seat", booking["seat"])]
        for index, (label, value) in enumerate(fields):
            field = tk.Frame(body, bg=COLOURS["surface"])
            field.grid(row=index // 3, column=index % 3, sticky="nsew", padx=15, pady=14)
            tk.Label(field, text=label.upper(), bg=COLOURS["surface"], fg=COLOURS["muted"], font=("Arial", 8, "bold")).pack(anchor="w")
            tk.Label(field, text=value, bg=COLOURS["surface"], fg=COLOURS["text"], font=("Arial", 14, "bold")).pack(anchor="w", pady=(3, 0))
        for column in range(3):
            body.grid_columnconfigure(column, weight=1)
        ttk.Button(outer, text="Save Boarding Pass as TXT", style="Primary.TButton", command=lambda: self.export_boarding_pass(booking)).pack(pady=18)

    def export_boarding_pass(self, booking):
        """Save the displayed boarding pass as a text file."""
        success, message, path = save_boarding_pass_file(booking)
        if not success:
            messagebox.showerror("Export Failed", message)
            return
        messagebox.showinfo("Boarding Pass Saved", f"{message}\n\nSaved to:\n{path}")

    # ---------------- ADMIN ----------------

    def show_admin_dashboard(self):
        """Display administrator navigation and management options."""
        # Display the administrator dashboard with management actions.
        self.clear_window()
        self.make_header("Administrator Dashboard", f"Signed in as {self.current_user['email']}")
        content = tk.Frame(self.root, bg=COLOURS["background"])
        content.pack(fill="both", expand=True, padx=70, pady=55)
        for index, (title, command) in enumerate((
            ("View Flights", self.show_admin_flights),
            ("View All Bookings", self.show_admin_bookings),
            ("Statistics", self.show_admin_statistics),
            ("Contact Us", self.open_contact_email),
        )):
            ttk.Button(content, text=title, command=command, style="AdminCard.TButton", cursor="hand2").grid(row=index // 2, column=index % 2, sticky="nsew", padx=12, pady=12)
        for column in range(2):
            content.grid_columnconfigure(column, weight=1)
        for row in range(2):
            content.grid_rowconfigure(row, weight=1)
        ttk.Button(content, text="Log Out", command=self.logout, style="Danger.TButton", cursor="hand2").grid(row=2, column=1, sticky="e", pady=(20, 0))

    def show_admin_flights(self):
        """Display all generated flight records."""
        # Show every generated flight for administrators.
        self.clear_window()
        self.make_header("All Flights", "Administrator view of every flight record.", self.show_admin_dashboard)
        main = ttk.Frame(self.root, padding=24)
        main.pack(fill="both", expand=True)
        frame = ttk.LabelFrame(main, text="Flight Records", padding=10)
        frame.pack(fill="both", expand=True)
        tree = self.create_tree(frame, [
            ("id", "Flight", 80, "center"), ("airline", "Airline", 150, "w"),
            ("route", "Route", 190, "w"), ("date", "Date", 105, "center"),
            ("depart", "Departure", 90, "center"), ("price", "Base Price", 90, "center"),
            ("seats", "Seats", 65, "center"),
        ], 15)
        for flight in load_json_file(FLIGHTS_FILE):
            tree.insert("", "end", values=(flight["flight_id"], flight["airline"], f"{flight['origin']} → {flight['destination']}", flight["departure_date"], flight["departure_time"], f"£{flight['base_price']:.2f}", len(flight.get("available_seats", []))))

    def show_admin_bookings(self):
        """Display all passenger booking records."""
        # Show every booking record for administrators.
        self.clear_window()
        self.make_header("All Bookings", "Administrator view of every booking.", self.show_admin_dashboard)
        main = ttk.Frame(self.root, padding=24)
        main.pack(fill="both", expand=True)
        frame = ttk.LabelFrame(main, text="Booking Records", padding=10)
        frame.pack(fill="both", expand=True)
        tree = self.create_tree(frame, [
            ("ref", "Reference", 125, "center"), ("passenger", "Passenger", 165, "w"),
            ("flight", "Flight", 80, "center"), ("route", "Route", 180, "w"),
            ("date", "Date", 105, "center"), ("total", "Total", 85, "center"),
            ("status", "Status", 100, "center"),
        ], 15)
        for booking in load_json_file(BOOKINGS_FILE):
            tree.insert("", "end", values=(booking["booking_reference"], booking["passenger_name"], booking["flight_id"], f"{booking['origin']} → {booking['destination']}", booking["departure_date"], f"£{booking['total_price']:.2f}", booking["status"]))

    def show_admin_statistics(self):
        """Display booking metrics and a bookings-by-airline chart."""
        # Show simple booking statistics and a bar chart for administrators.
        self.clear_window()
        self.make_header("Booking Statistics", "Simple data visualisation of bookings by airline.", self.show_admin_dashboard)
        bookings = load_json_file(BOOKINGS_FILE)
        flights = load_json_file(FLIGHTS_FILE)
        # Cancelled bookings are excluded from the active-airline chart.
        active = [booking for booking in bookings if booking.get("status") != "Cancelled"]
        counts = Counter(booking.get("airline", "Unknown") for booking in active)  # Bar-chart values
        content = tk.Frame(self.root, bg=COLOURS["background"])
        content.pack(fill="both", expand=True, padx=55, pady=30)
        metrics = tk.Frame(content, bg=COLOURS["background"])
        metrics.pack(fill="x")
        values = [("Flights", len(flights)), ("All Bookings", len(bookings)), ("Active", len(active)), ("Checked In", sum(1 for item in bookings if item.get("checked_in")))]
        for column, (label, value) in enumerate(values):
            card = tk.Frame(metrics, bg=COLOURS["surface"], highlightbackground=COLOURS["border"], highlightthickness=1, padx=20, pady=16)
            card.grid(row=0, column=column, sticky="nsew", padx=7)
            tk.Label(card, text=str(value), bg=COLOURS["surface"], fg=COLOURS["primary"], font=("Arial", 23, "bold")).pack()
            tk.Label(card, text=label, bg=COLOURS["surface"], fg=COLOURS["muted"], font=("Arial", 9, "bold")).pack()
            metrics.grid_columnconfigure(column, weight=1)
        chart = tk.Canvas(content, bg=COLOURS["surface"], highlightbackground=COLOURS["border"], highlightthickness=1, height=350)
        chart.pack(fill="both", expand=True, pady=(25, 0))
        chart.update_idletasks()
        if not counts:
            chart.create_text(500, 170, text="No active booking data is available yet.", fill=COLOURS["muted"], font=("Arial", 14))
            return
        width = max(chart.winfo_width(), 800)
        margin, bottom = 55, 305
        slot = (width - 2 * margin) / len(counts)
        maximum = max(counts.values())  # Scale bars to the largest count
        chart.create_text(margin, 25, anchor="w", text="Bookings by Airline", fill=COLOURS["text"], font=("Arial", 15, "bold"))
        for index, (airline, count) in enumerate(sorted(counts.items())):
            centre = margin + slot * index + slot / 2
            height = count / maximum * 220
            chart.create_rectangle(centre - slot * 0.25, bottom - height, centre + slot * 0.25, bottom, fill=COLOURS["secondary"], outline="")
            chart.create_text(centre, bottom - height - 12, text=str(count), fill=COLOURS["text"], font=("Arial", 10, "bold"))
            chart.create_text(centre, bottom + 18, text=airline, fill=COLOURS["muted"], font=("Arial", 9))


def main():
    """Prepare the data environment and launch the booking GUI."""
    # Initialize storage, sample accounts, and flight data before launching the GUI.
    create_data_files()
    ensure_default_admin()
    ensure_default_passenger()
    ensure_sample_flights()
    root = tk.Tk()  # Create the main application window
    AirlineBookingApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
