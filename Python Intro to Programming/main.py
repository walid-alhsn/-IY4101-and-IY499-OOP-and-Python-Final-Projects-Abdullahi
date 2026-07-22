# AIRLINE / FLIGHT BOOKING MANAGEMENT SYSTEM

import hashlib
import hmac
import json
import secrets
import tkinter as tk
import uuid

from datetime import datetime
from pathlib import Path
from tkinter import messagebox, ttk

# =========================================================
# FILE PATHS
# ========================================================

# The folder containing this Python file
BASE_DIR = Path(__file__).resolve().parent

# The folder where the JSON data files will be stored
DATA_DIR = BASE_DIR / "data"

# Individual JSON file locations
USERS_FILE = DATA_DIR / "users.json"
FLIGHTS_FILE = DATA_DIR / "flights.json"
BOOKINGS_FILE = DATA_DIR / "bookings.json"

# =========================================================
# FILE-HANDLING FUNCTIONS
# ========================================================

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

# ==========================================================
# FLIGHT DATA FUNCTIONS
# ==========================================================

def generate_seat_list(number_of_rows=3):
    """
    Generate seat numbers for an aircraft.

    Each row contains seats A, B, C and D.
    For example: 1A, 1B, 1C and 1D.
    """

    seats = []
    seat_letters = ["A", "B", "C", "D"]

    for row_number in range(1, number_of_rows + 1):
        for seat_letter in seat_letters:
            seat_number = f"{row_number}{seat_letter}"
            seats.append(seat_number)

    return seats

def create_sample_flights():
    """
    Add the initial flight records when flights.json is empty.

    Existing flight data is not overwritten.
    """

    flights = load_json_file(FLIGHTS_FILE)

    if not isinstance(flights, list):
        print("Error: flights.json must contain a list.")
        return False

    # Do not overwrite existing flight records
    if len(flights) > 0:
        return True

    all_seats = generate_seat_list(3)

    sample_flights = [
        {
            "flight_id": "SK101",
            "airline": "SkyLink Airways",
            "origin": "London",
            "destination": "Dubai",
            "departure_date": "2026-08-05",
            "departure_time": "09:30",
            "arrival_time": "19:20",
            "duration_minutes": 590,
            "gate": "A12",
            "base_price": 425.00,
            "airport_tax": 45.00,
            "total_seats": 12,
            "available_seats": all_seats.copy()
        },
        {
            "flight_id": "EA205",
            "airline": "Emerald Air",
            "origin": "London",
            "destination": "Dubai",
            "departure_date": "2026-08-05",
            "departure_time": "13:15",
            "arrival_time": "23:05",
            "duration_minutes": 590,
            "gate": "B07",
            "base_price": 390.00,
            "airport_tax": 45.00,
            "total_seats": 12,
            "available_seats": all_seats[2:]
        },
        {
            "flight_id": "AW318",
            "airline": "Atlantic Wings",
            "origin": "London",
            "destination": "Dubai",
            "departure_date": "2026-08-05",
            "departure_time": "18:40",
            "arrival_time": "04:30",
            "duration_minutes": 590,
            "gate": "C15",
            "base_price": 455.00,
            "airport_tax": 45.00,
            "total_seats": 12,
            "available_seats": all_seats[7:]
        },
        {
            "flight_id": "HA220",
            "airline": "Horizon Airlines",
            "origin": "Manchester",
            "destination": "Paris",
            "departure_date": "2026-08-05",
            "departure_time": "08:20",
            "arrival_time": "10:50",
            "duration_minutes": 90,
            "gate": "D04",
            "base_price": 175.00,
            "airport_tax": 30.00,
            "total_seats": 12,
            "available_seats": all_seats.copy()
        },
        {
            "flight_id": "SK150",
            "airline": "SkyLink Airways",
            "origin": "London",
            "destination": "New York",
            "departure_date": "2026-08-06",
            "departure_time": "11:10",
            "arrival_time": "14:20",
            "duration_minutes": 490,
            "gate": "A18",
            "base_price": 520.00,
            "airport_tax": 60.00,
            "total_seats": 12,
            "available_seats": all_seats[3:]
        },
        {
            "flight_id": "EA330",
            "airline": "Emerald Air",
            "origin": "Lagos",
            "destination": "Abuja",
            "departure_date": "2026-08-06",
            "departure_time": "07:30",
            "arrival_time": "08:45",
            "duration_minutes": 75,
            "gate": "B03",
            "base_price": 95.00,
            "airport_tax": 15.00,
            "total_seats": 12,
            "available_seats": all_seats.copy()
        },
        {
            "flight_id": "AW401",
            "airline": "Atlantic Wings",
            "origin": "Abuja",
            "destination": "Lagos",
            "departure_date": "2026-08-07",
            "departure_time": "15:20",
            "arrival_time": "16:35",
            "duration_minutes": 75,
            "gate": "C08",
            "base_price": 105.00,
            "airport_tax": 15.00,
            "total_seats": 12,
            "available_seats": all_seats[5:]
        },
        {
            "flight_id": "HA510",
            "airline": "Horizon Airlines",
            "origin": "Kano",
            "destination": "Lagos",
            "departure_date": "2026-08-07",
            "departure_time": "10:00",
            "arrival_time": "11:40",
            "duration_minutes": 100,
            "gate": "D10",
            "base_price": 120.00,
            "airport_tax": 18.00,
            "total_seats": 12,
            "available_seats": all_seats[1:]
        }
    ]

    if save_json_file(FLIGHTS_FILE, sample_flights):
        print("Sample flight data created successfully.")
        return True

    return False

def search_flights(origin, destination, departure_date):
    """
    Search for flights matching an origin, destination and date.

    This function uses a linear search by examining every
    flight record one at a time.
    """

    flights = load_json_file(FLIGHTS_FILE)
    matching_flights = []

    if not isinstance(flights, list):
        return matching_flights

    cleaned_origin = origin.strip().lower()
    cleaned_destination = destination.strip().lower()
    cleaned_date = departure_date.strip()

    for flight in flights:
        flight_origin = flight.get("origin", "").lower()
        flight_destination = flight.get("destination", "").lower()
        flight_date = flight.get("departure_date", "")

        origin_matches = flight_origin == cleaned_origin
        destination_matches = (
            flight_destination == cleaned_destination
        )
        date_matches = flight_date == cleaned_date

        if origin_matches and destination_matches and date_matches:
            matching_flights.append(flight)

    return matching_flights

def bubble_sort_flights(flights, sort_option):
    """
    Sort flight records using the bubble sort algorithm.

    A copy of the supplied list is sorted so the original
    list is not changed.
    """

    sorted_flights = flights.copy()
    number_of_flights = len(sorted_flights)

    for pass_number in range(number_of_flights - 1):
        swapped = False

        for index in range(
            number_of_flights - 1 - pass_number
        ):
            current_flight = sorted_flights[index]
            next_flight = sorted_flights[index + 1]

            if sort_option == "Price: Low to High":
                current_value = current_flight.get(
                    "base_price",
                    0
                )
                next_value = next_flight.get(
                    "base_price",
                    0
                )

                should_swap = current_value > next_value

            elif sort_option == "Price: High to Low":
                current_value = current_flight.get(
                    "base_price",
                    0
                )
                next_value = next_flight.get(
                    "base_price",
                    0
                )

                should_swap = current_value < next_value

            elif sort_option == "Departure Time":
                current_value = current_flight.get(
                    "departure_time",
                    ""
                )
                next_value = next_flight.get(
                    "departure_time",
                    ""
                )

                should_swap = current_value > next_value

            elif sort_option == "Airline: A to Z":
                current_value = current_flight.get(
                    "airline",
                    ""
                ).lower()

                next_value = next_flight.get(
                    "airline",
                    ""
                ).lower()

                should_swap = current_value > next_value

            else:
                return sorted_flights

            if should_swap:
                sorted_flights[index] = next_flight
                sorted_flights[index + 1] = current_flight
                swapped = True

        # Stop early if no values were exchanged
        if not swapped:
            break

    return sorted_flights

# ==========================================================
# FARE CALCULATION FUNCTIONS
# ==========================================================

def calculate_demand_adjustment(flight):
    """
    Calculate a price increase based on the percentage
    of seats still available.

    Returns the adjustment amount and percentage rate.
    """

    base_price = float(flight.get("base_price", 0))
    total_seats = int(flight.get("total_seats", 0))
    available_seats = flight.get("available_seats", [])

    if total_seats <= 0:
        return 0.0, 0

    availability_percentage = (
        len(available_seats) / total_seats
    ) * 100

    if availability_percentage > 60:
        adjustment_rate = 0.00

    elif availability_percentage > 30:
        adjustment_rate = 0.10

    elif availability_percentage > 10:
        adjustment_rate = 0.20

    else:
        adjustment_rate = 0.30

    adjustment_amount = base_price * adjustment_rate

    return round(adjustment_amount, 2), int(
        adjustment_rate * 100
    )


def calculate_seat_charge(seat_number):
    """
    Calculate the additional charge for a selected seat.

    Seats A and D are window seats.
    Seats B and C are standard seats.
    """

    if seat_number == "":
        return 0.0

    seat_letter = seat_number[-1].upper()

    if seat_letter in ["A", "D"]:
        return 15.00

    return 5.00


def calculate_total_fare(flight, seat_number):
    """
    Calculate and return a complete fare breakdown.
    """

    base_price = float(flight.get("base_price", 0))
    airport_tax = float(flight.get("airport_tax", 0))

    demand_adjustment, demand_rate = (
        calculate_demand_adjustment(flight)
    )

    seat_charge = calculate_seat_charge(seat_number)

    total_price = (
        base_price
        + airport_tax
        + demand_adjustment
        + seat_charge
    )

    fare_details = {
        "base_price": round(base_price, 2),
        "airport_tax": round(airport_tax, 2),
        "demand_adjustment": round(
            demand_adjustment,
            2
        ),
        "demand_rate": demand_rate,
        "seat_charge": round(seat_charge, 2),
        "total_price": round(total_price, 2)
    }

    return fare_details

def validate_flight_search(origin, destination, departure_date):
    """
    Validate the information entered on the flight search form.

    Returns True and an empty message when valid.
    Returns False and an error message when invalid.
    """

    origin = origin.strip()
    destination = destination.strip()
    departure_date = departure_date.strip()

    if origin == "":
        return False, "Please select an origin."

    if destination == "":
        return False, "Please select a destination."

    if origin.lower() == destination.lower():
        return False, "Origin and destination cannot be the same."

    if departure_date == "":
        return False, "Please enter a departure date."

    try:
        selected_date = datetime.strptime(
            departure_date,
            "%Y-%m-%d"
        ).date()

    except ValueError:
        return False, "Date must use the format YYYY-MM-DD."

    today = datetime.now().date()

    if selected_date < today:
        return False, "Departure date cannot be in the past."

    return True, ""

# =========================================================
# VALIDATION FUNCTIONS
# ========================================================

def validate_name(name):
    """
    Check that a full name is valid.

    Returns:
        (True, "") when the name is valid.
        (False, error_message) when it is invalid.
    """

    name = name.strip()

    if name == "":
        return False, "Full name cannot be empty."

    if len(name) < 2:
        return False, "Full name must contain at least two characters."

    for character in name:
        if not (
            character.isalpha()
            or character.isspace()
            or character in "-'"
        ):
            return False, (
                "Full name can only contain letters, spaces, "
                "hyphens and apostrophes."
            )

    return True, ""


def validate_email(email):
    """
    Check that an email address has a reasonable format.
    """

    email = email.strip()

    if email == "":
        return False, "Email address cannot be empty."

    if " " in email:
        return False, "Email address cannot contain spaces."

    if email.count("@") != 1:
        return False, "Email address must contain one @ symbol."

    local_part, domain_part = email.split("@")

    if local_part == "":
        return False, "Email address must contain text before the @ symbol."

    if domain_part == "":
        return False, "Email address must contain a domain after the @ symbol."

    if "." not in domain_part:
        return False, "Email domain must contain a full stop."

    if domain_part.startswith(".") or domain_part.endswith("."):
        return False, "Email domain cannot start or end with a full stop."

    return True, ""


def validate_phone(phone):
    """
    Check that a telephone number has a reasonable format.
    """

    phone = phone.strip()

    if phone == "":
        return False, "Telephone number cannot be empty."

    # Remove permitted formatting characters
    cleaned_phone = phone.replace(" ", "")
    cleaned_phone = cleaned_phone.replace("-", "")
    cleaned_phone = cleaned_phone.replace("(", "")
    cleaned_phone = cleaned_phone.replace(")", "")

    # Permit one + symbol only at the beginning
    if cleaned_phone.startswith("+"):
        digits = cleaned_phone[1:]
    else:
        digits = cleaned_phone
    # Check if the remaining characters are all digits
    if not digits.isdigit():
        return False, "Telephone number can only contain numbers."
    # Check the length of the digits
    if len(digits) < 7 or len(digits) > 15:
        return False, "Telephone number must contain between 7 and 15 digits."

    return True, ""


def validate_password(password):
    """
    Check whether a password satisfies the account requirements.
    """

    if password == "":
        return False, "Password cannot be empty."

    if len(password) < 8:
        return False, "Password must contain at least eight characters."

    has_uppercase = False
    has_lowercase = False
    has_digit = False

    # check for at least one uppercase letter, one lowercase letter, and one digit
    for character in password:
        if character.isupper():
            has_uppercase = True
        elif character.islower():
            has_lowercase = True
        elif character.isdigit():
            has_digit = True

    if not has_uppercase:
        return False, "Password must contain at least one uppercase letter."

    if not has_lowercase:
        return False, "Password must contain at least one lowercase letter."

    if not has_digit:
        return False, "Password must contain at least one number."

    return True, ""

def get_flight_locations():
    """
    Return sorted lists of available origins and destinations.
    """

    flights = load_json_file(FLIGHTS_FILE)

    origins = []
    destinations = []

    if not isinstance(flights, list):
        return origins, destinations

    for flight in flights:
        origin = flight.get("origin", "")
        destination = flight.get("destination", "")

        if origin != "" and origin not in origins:
            origins.append(origin)

        if destination != "" and destination not in destinations:
            destinations.append(destination)

    origins.sort()
    destinations.sort()

    return origins, destinations

# ==========================================================
# AUTHENTICATION FUNCTIONS
# ==========================================================

def normalise_email(email):
    """
    Remove unnecessary spaces and convert an email address
    to lowercase.
    """

    return email.strip().lower()


def email_exists(email, users):
    """
    Check whether an email address is already registered.
    """

    email = normalise_email(email)

    for user in users:
        if normalise_email(user["email"]) == email:
            return True

    return False


def generate_user_id():
    """
    Generate a unique user ID.
    """

    random_part = uuid.uuid4().hex[:8].upper()
    return f"USR-{random_part}"


def create_password_hash(password, salt):
    """
    Create a secure password hash using the supplied salt.
    """

    salt_bytes = bytes.fromhex(salt)
    password_bytes = password.encode("utf-8")

    password_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password_bytes,
        salt_bytes,
        100000
    )

    return password_hash.hex()


def register_user(
    full_name,
    email,
    phone,
    password,
    confirm_password
):
    """
    Validate and register a new passenger account.

    Returns:
        True and a success message when registration succeeds.
        False and an error message when registration fails.
    """

    # Validate the passenger's name
    is_valid, message = validate_name(full_name)

    if not is_valid:
        return False, message

    # Validate the email address
    is_valid, message = validate_email(email)

    if not is_valid:
        return False, message

    # Validate the telephone number
    is_valid, message = validate_phone(phone)

    if not is_valid:
        return False, message

    # Validate the password
    is_valid, message = validate_password(password)

    if not is_valid:
        return False, message

    # Ensure both password fields match
    if password != confirm_password:
        return False, "Passwords do not match."

    users = load_json_file(USERS_FILE)

    # Ensure the loaded data is a list
    if not isinstance(users, list):
        return False, "The user data file has an invalid structure."

    cleaned_email = normalise_email(email)

    # Prevent duplicate accounts
    if email_exists(cleaned_email, users):
        return False, "An account already exists with this email address."

    # Generate a random salt and hash the password
    salt = secrets.token_hex(16)
    password_hash = create_password_hash(password, salt)

    new_user = {
        "user_id": generate_user_id(),
        "full_name": full_name.strip(),
        "email": cleaned_email,
        "phone": phone.strip(),
        "password_hash": password_hash,
        "salt": salt,
        "role": "passenger"
    }

    users.append(new_user)

    if save_json_file(USERS_FILE, users):
        return True, "Account created successfully."

    return False, "The account could not be saved."

def find_user_by_email(email, users):
    """
    Find and return a user with the supplied email address.

    Returns None if the email address is not registered.
    """

    cleaned_email = normalise_email(email)

    for user in users:
        saved_email = normalise_email(user.get("email", ""))

        if saved_email == cleaned_email:
            return user

    return None


def authenticate_user(email, password):
    """
    Authenticate a user using their email address and password.

    Returns:
        True, success message and user details when login succeeds.
        False, error message and None when login fails.
    """

    email = email.strip()

    if email == "" or password == "":
        return False, "Email and password are required.", None

    users = load_json_file(USERS_FILE)

    if not isinstance(users, list):
        return False, "The user data file has an invalid structure.", None

    user = find_user_by_email(email, users)

    if user is None:
        return False, "Invalid email address or password.", None

    stored_salt = user.get("salt", "")
    stored_hash = user.get("password_hash", "")

    if stored_salt == "" or stored_hash == "":
        return False, "The account data is incomplete.", None

    try:
        entered_hash = create_password_hash(
            password,
            stored_salt
        )

    except ValueError:
        return False, "The account data is invalid.", None

    if not hmac.compare_digest(entered_hash, stored_hash):
        return False, "Invalid email address or password.", None

    # Do not pass the password hash or salt to the GUI
    authenticated_user = {
        "user_id": user["user_id"],
        "full_name": user["full_name"],
        "email": user["email"],
        "phone": user["phone"],
        "role": user["role"]
    }

    return True, "Login successful.", authenticated_user

# ==========================================================
# GRAPHICAL USER INTERFACE
# ==========================================================

class AirlineBookingApp:
    """
    Main graphical user interface for the airline booking
    management system.
    """

    def __init__(self, root):
        """
        Set up the main application window.
        """

        self.root = root
        self.current_user = None

        self.root.title("Airline Booking Management System")
        self.root.geometry("900x650")
        self.root.minsize(850, 600)

        # Configure reusable widget styles
        self.style = ttk.Style()

        self.style.configure(
            "Title.TLabel",
            font=("Arial", 24, "bold")
        )

        self.style.configure(
            "Subtitle.TLabel",
            font=("Arial", 12)
        )

        self.style.configure(
            "Dashboard.TButton",
            font=("Arial", 12),
            padding=10
        )

        self.show_login_page()

    def clear_window(self):
        """
        Remove every widget currently displayed in the window.
        """

        # Remove page-specific mouse-wheel bindings
        self.root.unbind_all("<MouseWheel>")

        for widget in self.root.winfo_children():
            widget.destroy()

    # ======================================================
    # LOGIN PAGE
    # ======================================================

    def show_login_page(self):
        """
        Display the login page.
        """

        self.clear_window()

        main_frame = ttk.Frame(
            self.root,
            padding=40
        )
        main_frame.pack(expand=True)

        title_label = ttk.Label(
            main_frame,
            text="Airline Booking System",
            style="Title.TLabel"
        )
        title_label.grid(
            row=0,
            column=0,
            columnspan=2,
            pady=(0, 10)
        )

        subtitle_label = ttk.Label(
            main_frame,
            text="Log in to search, book and manage your flights",
            style="Subtitle.TLabel"
        )
        subtitle_label.grid(
            row=1,
            column=0,
            columnspan=2,
            pady=(0, 30)
        )

        email_label = ttk.Label(
            main_frame,
            text="Email address:"
        )
        email_label.grid(
            row=2,
            column=0,
            sticky="w",
            padx=(0, 15),
            pady=10
        )

        self.login_email_entry = ttk.Entry(
            main_frame,
            width=35
        )
        self.login_email_entry.grid(
            row=2,
            column=1,
            pady=10
        )

        password_label = ttk.Label(
            main_frame,
            text="Password:"
        )
        password_label.grid(
            row=3,
            column=0,
            sticky="w",
            padx=(0, 15),
            pady=10
        )

        self.login_password_entry = ttk.Entry(
            main_frame,
            width=35,
            show="*"
        )
        self.login_password_entry.grid(
            row=3,
            column=1,
            pady=10
        )

        login_button = ttk.Button(
            main_frame,
            text="Log In",
            command=self.handle_login
        )
        login_button.grid(
            row=4,
            column=0,
            columnspan=2,
            sticky="ew",
            pady=(20, 10)
        )

        signup_text = ttk.Label(
            main_frame,
            text="Do not have an account?"
        )
        signup_text.grid(
            row=5,
            column=0,
            columnspan=2,
            pady=(15, 5)
        )

        signup_button = ttk.Button(
            main_frame,
            text="Create an Account",
            command=self.show_signup_page
        )
        signup_button.grid(
            row=6,
            column=0,
            columnspan=2,
            sticky="ew"
        )

        self.login_email_entry.focus()

    def handle_login(self):
        """
        Read the login form and authenticate the user.
        """

        email = self.login_email_entry.get()
        password = self.login_password_entry.get()

        success, message, user = authenticate_user(
            email,
            password
        )

        if not success:
            messagebox.showerror(
                "Login Failed",
                message
            )
            return

        self.current_user = user

        messagebox.showinfo(
            "Login Successful",
            f"Welcome, {user['full_name']}!"
        )

        if user["role"] == "admin":
            self.show_admin_dashboard()
        else:
            self.show_passenger_dashboard()

    # ======================================================
    # SIGN-UP PAGE
    # ======================================================

    def show_signup_page(self):
        """
        Display the new-account registration page.
        """

        self.clear_window()

        main_frame = ttk.Frame(
            self.root,
            padding=35
        )
        main_frame.pack(expand=True)

        title_label = ttk.Label(
            main_frame,
            text="Create an Account",
            style="Title.TLabel"
        )
        title_label.grid(
            row=0,
            column=0,
            columnspan=2,
            pady=(0, 25)
        )

        full_name_label = ttk.Label(
            main_frame,
            text="Full name:"
        )
        full_name_label.grid(
            row=1,
            column=0,
            sticky="w",
            padx=(0, 15),
            pady=8
        )

        self.signup_name_entry = ttk.Entry(
            main_frame,
            width=35
        )
        self.signup_name_entry.grid(
            row=1,
            column=1,
            pady=8
        )

        email_label = ttk.Label(
            main_frame,
            text="Email address:"
        )
        email_label.grid(
            row=2,
            column=0,
            sticky="w",
            padx=(0, 15),
            pady=8
        )

        self.signup_email_entry = ttk.Entry(
            main_frame,
            width=35
        )
        self.signup_email_entry.grid(
            row=2,
            column=1,
            pady=8
        )

        phone_label = ttk.Label(
            main_frame,
            text="Telephone number:"
        )
        phone_label.grid(
            row=3,
            column=0,
            sticky="w",
            padx=(0, 15),
            pady=8
        )

        self.signup_phone_entry = ttk.Entry(
            main_frame,
            width=35
        )
        self.signup_phone_entry.grid(
            row=3,
            column=1,
            pady=8
        )

        password_label = ttk.Label(
            main_frame,
            text="Password:"
        )
        password_label.grid(
            row=4,
            column=0,
            sticky="w",
            padx=(0, 15),
            pady=8
        )

        self.signup_password_entry = ttk.Entry(
            main_frame,
            width=35,
            show="*"
        )
        self.signup_password_entry.grid(
            row=4,
            column=1,
            pady=8
        )

        confirm_password_label = ttk.Label(
            main_frame,
            text="Confirm password:"
        )
        confirm_password_label.grid(
            row=5,
            column=0,
            sticky="w",
            padx=(0, 15),
            pady=8
        )

        self.signup_confirm_entry = ttk.Entry(
            main_frame,
            width=35,
            show="*"
        )
        self.signup_confirm_entry.grid(
            row=5,
            column=1,
            pady=8
        )

        password_rule_label = ttk.Label(
            main_frame,
            text=(
                "Password must contain at least 8 characters, "
                "one uppercase letter,\none lowercase letter "
                "and one number."
            )
        )
        password_rule_label.grid(
            row=6,
            column=0,
            columnspan=2,
            pady=(10, 15)
        )

        create_account_button = ttk.Button(
            main_frame,
            text="Create Account",
            command=self.handle_signup
        )
        create_account_button.grid(
            row=7,
            column=0,
            columnspan=2,
            sticky="ew",
            pady=(5, 10)
        )

        back_button = ttk.Button(
            main_frame,
            text="Back to Login",
            command=self.show_login_page
        )
        back_button.grid(
            row=8,
            column=0,
            columnspan=2,
            sticky="ew"
        )

        self.signup_name_entry.focus()

    def handle_signup(self):
        """
        Read the sign-up form and attempt to create an account.
        """

        full_name = self.signup_name_entry.get()
        email = self.signup_email_entry.get()
        phone = self.signup_phone_entry.get()
        password = self.signup_password_entry.get()
        confirm_password = self.signup_confirm_entry.get()

        success, message = register_user(
            full_name,
            email,
            phone,
            password,
            confirm_password
        )

        if not success:
            messagebox.showerror(
                "Registration Failed",
                message
            )
            return

        messagebox.showinfo(
            "Account Created",
            message
        )

        self.show_login_page()

        # Automatically insert the newly registered email
        self.login_email_entry.insert(
            0,
            normalise_email(email)
        )

        self.login_password_entry.focus()

    # ======================================================
    # PASSENGER DASHBOARD
    # ======================================================

    def show_passenger_dashboard(self):
        """
        Display the main dashboard for a passenger.
        """

        self.clear_window()

        main_frame = ttk.Frame(
            self.root,
            padding=40
        )
        main_frame.pack(
            fill="both",
            expand=True
        )

        welcome_label = ttk.Label(
            main_frame,
            text=f"Welcome, {self.current_user['full_name']}",
            style="Title.TLabel"
        )
        welcome_label.pack(pady=(20, 10))

        email_label = ttk.Label(
            main_frame,
            text=self.current_user["email"],
            style="Subtitle.TLabel"
        )
        email_label.pack(pady=(0, 30))

        search_button = ttk.Button(
            main_frame,
            text="Search and Book a Flight",
            style="Dashboard.TButton",
            command=self.show_flight_search_page
        )

        search_button.pack(
            fill="x",
            padx=120,
            pady=8
        )

        bookings_button = ttk.Button(
            main_frame,
            text="My Bookings",
            style="Dashboard.TButton",
            command=lambda: self.show_feature_message(
                "My Bookings"
            )
        )
        bookings_button.pack(
            fill="x",
            padx=120,
            pady=8
        )

        check_in_button = ttk.Button(
            main_frame,
            text="Check In",
            style="Dashboard.TButton",
            command=lambda: self.show_feature_message(
                "Check In"
            )
        )
        check_in_button.pack(
            fill="x",
            padx=120,
            pady=8
        )

        logout_button = ttk.Button(
            main_frame,
            text="Log Out",
            style="Dashboard.TButton",
            command=self.logout
        )
        logout_button.pack(
            fill="x",
            padx=120,
            pady=(25, 8)
        )

    # ======================================================
    # FLIGHT SEARCH PAGE
    # ======================================================

    def show_flight_search_page(self):
        """
        Display the flight search form and results table.
        """

        self.clear_window()

        # Store the flights currently displayed in the table
        self.search_results = []

        main_frame = ttk.Frame(
            self.root,
            padding=25
        )
        main_frame.pack(
            fill="both",
            expand=True
        )

        title_label = ttk.Label(
            main_frame,
            text="Search Flights",
            style="Title.TLabel"
        )
        title_label.pack(pady=(0, 20))

        search_frame = ttk.LabelFrame(
            main_frame,
            text="Journey Details",
            padding=15
        )
        search_frame.pack(
            fill="x",
            pady=(0, 20)
        )

        origins, destinations = get_flight_locations()

        origin_label = ttk.Label(
            search_frame,
            text="Origin:"
        )
        origin_label.grid(
            row=0,
            column=0,
            sticky="w",
            padx=8,
            pady=8
        )

        self.origin_combobox = ttk.Combobox(
            search_frame,
            values=origins,
            state="readonly",
            width=20
        )
        self.origin_combobox.grid(
            row=1,
            column=0,
            padx=8,
            pady=8
        )

        destination_label = ttk.Label(
            search_frame,
            text="Destination:"
        )
        destination_label.grid(
            row=0,
            column=1,
            sticky="w",
            padx=8,
            pady=8
        )

        self.destination_combobox = ttk.Combobox(
            search_frame,
            values=destinations,
            state="readonly",
            width=20
        )
        self.destination_combobox.grid(
            row=1,
            column=1,
            padx=8,
            pady=8
        )

        date_label = ttk.Label(
            search_frame,
            text="Departure date:"
        )
        date_label.grid(
            row=0,
            column=2,
            sticky="w",
            padx=8,
            pady=8
        )

        self.departure_date_entry = ttk.Entry(
            search_frame,
            width=20
        )
        self.departure_date_entry.grid(
            row=1,
            column=2,
            padx=8,
            pady=8
        )

        date_format_label = ttk.Label(
            search_frame,
            text="Format: YYYY-MM-DD"
        )
        date_format_label.grid(
            row=2,
            column=2,
            padx=8,
            sticky="w"
        )

        search_button = ttk.Button(
            search_frame,
            text="Search Flights",
            command=self.handle_flight_search
        )
        search_button.grid(
            row=1,
            column=3,
            padx=15,
            pady=8
        )

        # Results section
        results_frame = ttk.LabelFrame(
            main_frame,
            text="Available Flights",
            padding=10
        )
        results_frame.pack(
            fill="both",
            expand=True
        )

        columns = (
            "flight_id",
            "airline",
            "departure",
            "arrival",
            "price",
            "available_seats"
        )

        self.flight_results_tree = ttk.Treeview(
            results_frame,
            columns=columns,
            show="headings",
            height=10,
            selectmode="browse"
        )

        self.flight_results_tree.heading(
            "flight_id",
            text="Flight"
        )
        self.flight_results_tree.heading(
            "airline",
            text="Airline"
        )
        self.flight_results_tree.heading(
            "departure",
            text="Departure"
        )
        self.flight_results_tree.heading(
            "arrival",
            text="Arrival"
        )
        self.flight_results_tree.heading(
            "price",
            text="Base Price"
        )
        self.flight_results_tree.heading(
            "available_seats",
            text="Seats"
        )

        self.flight_results_tree.column(
            "flight_id",
            width=80,
            anchor="center"
        )
        self.flight_results_tree.column(
            "airline",
            width=150
        )
        self.flight_results_tree.column(
            "departure",
            width=90,
            anchor="center"
        )
        self.flight_results_tree.column(
            "arrival",
            width=90,
            anchor="center"
        )
        self.flight_results_tree.column(
            "price",
            width=90,
            anchor="center"
        )
        self.flight_results_tree.column(
            "available_seats",
            width=70,
            anchor="center"
        )

        scrollbar = ttk.Scrollbar(
            results_frame,
            orient="vertical",
            command=self.flight_results_tree.yview
        )

        self.flight_results_tree.configure(
            yscrollcommand=scrollbar.set
        )

        self.flight_results_tree.pack(
            side="left",
            fill="both",
            expand=True
        )

        scrollbar.pack(
            side="right",
            fill="y"
        )

        sort_frame = ttk.Frame(main_frame)
        sort_frame.pack(
            fill="x",
            pady=(12, 0)
        )

        sort_label = ttk.Label(
            sort_frame,
            text="Sort results by:"
        )
        sort_label.pack(
            side="left",
            padx=(0, 8)
        )

        self.sort_combobox = ttk.Combobox(
            sort_frame,
            values=[
                "Price: Low to High",
                "Price: High to Low",
                "Departure Time",
                "Airline: A to Z"
            ],
            state="readonly",
            width=22
        )
        self.sort_combobox.pack(
            side="left",
            padx=(0, 8)
        )

        self.sort_combobox.set(
            "Price: Low to High"
        )

        sort_button = ttk.Button(
            sort_frame,
            text="Sort Flights",
            command=self.handle_flight_sort
        )
        sort_button.pack(side="left")

        button_frame = ttk.Frame(main_frame)
        button_frame.pack(
            fill="x",
            pady=(15, 0)
        )

        back_button = ttk.Button(
            button_frame,
            text="Back to Dashboard",
            command=self.show_passenger_dashboard
        )
        back_button.pack(side="left")

        select_button = ttk.Button(
            button_frame,
            text="Select Flight",
            command=self.handle_flight_selection
        )
        select_button.pack(side="right")

        self.origin_combobox.focus()

    def handle_flight_search(self):
        """
        Validate the form, search the flight records and
        display matching flights.
        """

        origin = self.origin_combobox.get()
        destination = self.destination_combobox.get()
        departure_date = self.departure_date_entry.get()

        is_valid, message = validate_flight_search(
            origin,
            destination,
            departure_date
        )

        if not is_valid:
            messagebox.showerror(
                "Invalid Search",
                message
            )
            return

        matching_flights = search_flights(
            origin,
            destination,
            departure_date
        )

        self.search_results = matching_flights

        # Remove old rows from the table
        for row in self.flight_results_tree.get_children():
            self.flight_results_tree.delete(row)

        if len(matching_flights) == 0:
            messagebox.showinfo(
                "No Flights Found",
                (
                    "No flights were found for the selected "
                    "route and date."
                )
            )
            return

        self.display_flight_results(matching_flights)

    def display_flight_results(self, flights):
        """
        Clear the results table and display the supplied
        flight records.
        """

        for row in self.flight_results_tree.get_children():
            self.flight_results_tree.delete(row)

        for flight in flights:
            available_seat_count = len(
                flight.get("available_seats", [])
            )

            self.flight_results_tree.insert(
                "",
                "end",
                values=(
                    flight.get("flight_id", ""),
                    flight.get("airline", ""),
                    flight.get("departure_time", ""),
                    flight.get("arrival_time", ""),
                    f"£{flight.get('base_price', 0):.2f}",
                    available_seat_count
                )
            )

    def handle_flight_sort(self):
        """
        Sort the current flight-search results using the
        option selected by the passenger.
        """

        if len(self.search_results) == 0:
            messagebox.showerror(
                "No Search Results",
                "Please search for flights before sorting."
            )
            return

        sort_option = self.sort_combobox.get()

        if sort_option == "":
            messagebox.showerror(
                "No Sort Option",
                "Please select a sorting option."
            )
            return

        sorted_results = bubble_sort_flights(
            self.search_results,
            sort_option
        )

        self.search_results = sorted_results

        self.display_flight_results(
            self.search_results
        )

    def handle_flight_selection(self):
        """
        Store the flight selected by the passenger.
        """

        selected_items = (
            self.flight_results_tree.selection()
        )

        if len(selected_items) == 0:
            messagebox.showerror(
                "No Flight Selected",
                "Please select a flight from the results table."
            )
            return

        selected_item = selected_items[0]

        selected_values = self.flight_results_tree.item(
            selected_item,
            "values"
        )

        selected_flight_id = selected_values[0]

        selected_flight = None

        for flight in self.search_results:
            if flight.get("flight_id") == selected_flight_id:
                selected_flight = flight
                break

        if selected_flight is None:
            messagebox.showerror(
                "Selection Error",
                "The selected flight could not be found."
            )
            return

        self.selected_flight = selected_flight

        if len(selected_flight.get("available_seats", [])) == 0:
            messagebox.showerror(
                "Flight Unavailable",
                "This flight has no available seats."
            )
            return

        self.show_booking_details_page()

    # ======================================================
    # BOOKING DETAILS PAGE
    # ======================================================

    def show_booking_details_page(self):
        """
        Display the selected flight, passenger information,
        seat options and fare calculation.
        """

        self.clear_window()

        flight = self.selected_flight

        # Main container for the canvas and scrollbar
        page_container = ttk.Frame(self.root)
        page_container.pack(
            fill="both",
            expand=True
        )

        # Canvas allows the page to scroll vertically
        canvas = tk.Canvas(
            page_container,
            highlightthickness=0,
            background=self.root.cget("background")
        )

        scrollbar = ttk.Scrollbar(
            page_container,
            orient="vertical",
            command=canvas.yview
        )

        # All booking-page widgets will be placed inside this frame
        main_frame = ttk.Frame(
            canvas,
            padding=25
        )

        canvas_window = canvas.create_window(
            (0, 0),
            window=main_frame,
            anchor="nw"
        )

        canvas.configure(
            yscrollcommand=scrollbar.set
        )

        def update_scroll_region(event):
            """
            Update the scrollable area whenever the size of the
            booking page changes.
            """

            canvas.configure(
                scrollregion=canvas.bbox("all")
            )


        def resize_booking_page(event):
            """
            Keep the booking page the same width as the canvas.
            """

            canvas.itemconfigure(
                canvas_window,
                width=event.width
            )


        main_frame.bind(
            "<Configure>",
            update_scroll_region
        )

        canvas.bind(
            "<Configure>",
            resize_booking_page
        )

        canvas.pack(
            side="left",
            fill="both",
            expand=True
        )

        scrollbar.pack(
            side="right",
            fill="y"
        )

        # Mouse-wheel scrolling for macOS and Windows
        def scroll_booking_page(event):
            if event.delta > 0:
                canvas.yview_scroll(-1, "units")
            elif event.delta < 0:
                canvas.yview_scroll(1, "units")


        canvas.bind_all(
            "<MouseWheel>",
            scroll_booking_page
        )

        title_label = ttk.Label(
            main_frame,
            text="Complete Your Booking",
            style="Title.TLabel"
        )
        title_label.pack(pady=(0, 20))

        # --------------------------------------------------
        # FLIGHT INFORMATION
        # --------------------------------------------------

        flight_frame = ttk.LabelFrame(
            main_frame,
            text="Selected Flight",
            padding=15
        )
        flight_frame.pack(
            fill="x",
            pady=(0, 15)
        )

        flight_information = (
            f"{flight['flight_id']} — {flight['airline']}\n"
            f"{flight['origin']} to {flight['destination']}\n"
            f"Date: {flight['departure_date']}\n"
            f"Departure: {flight['departure_time']}    "
            f"Arrival: {flight['arrival_time']}\n"
            f"Gate: {flight['gate']}"
        )

        flight_label = ttk.Label(
            flight_frame,
            text=flight_information,
            justify="left"
        )
        flight_label.pack(anchor="w")

        # --------------------------------------------------
        # PASSENGER INFORMATION
        # --------------------------------------------------

        passenger_frame = ttk.LabelFrame(
            main_frame,
            text="Passenger Details",
            padding=15
        )
        passenger_frame.pack(
            fill="x",
            pady=(0, 15)
        )

        ttk.Label(
            passenger_frame,
            text="Full name:"
        ).grid(
            row=0,
            column=0,
            sticky="w",
            padx=(0, 15),
            pady=5
        )

        name_entry = ttk.Entry(
            passenger_frame,
            width=35
        )
        name_entry.grid(
            row=0,
            column=1,
            pady=5
        )
        name_entry.insert(
            0,
            self.current_user["full_name"]
        )
        name_entry.configure(state="readonly")

        ttk.Label(
            passenger_frame,
            text="Email address:"
        ).grid(
            row=1,
            column=0,
            sticky="w",
            padx=(0, 15),
            pady=5
        )

        email_entry = ttk.Entry(
            passenger_frame,
            width=35
        )
        email_entry.grid(
            row=1,
            column=1,
            pady=5
        )
        email_entry.insert(
            0,
            self.current_user["email"]
        )
        email_entry.configure(state="readonly")

        ttk.Label(
            passenger_frame,
            text="Telephone:"
        ).grid(
            row=2,
            column=0,
            sticky="w",
            padx=(0, 15),
            pady=5
        )

        phone_entry = ttk.Entry(
            passenger_frame,
            width=35
        )
        phone_entry.grid(
            row=2,
            column=1,
            pady=5
        )
        phone_entry.insert(
            0,
            self.current_user["phone"]
        )
        phone_entry.configure(state="readonly")

        # --------------------------------------------------
        # SEAT SELECTION
        # --------------------------------------------------

        booking_frame = ttk.LabelFrame(
            main_frame,
            text="Seat and Fare",
            padding=15
        )
        booking_frame.pack(
            fill="x"
        )

        ttk.Label(
            booking_frame,
            text="Select an available seat:"
        ).grid(
            row=0,
            column=0,
            sticky="w",
            padx=(0, 15),
            pady=8
        )

        available_seats = flight.get(
            "available_seats",
            []
        )

        self.seat_combobox = ttk.Combobox(
            booking_frame,
            values=available_seats,
            state="readonly",
            width=20
        )
        self.seat_combobox.grid(
            row=0,
            column=1,
            sticky="w",
            pady=8
        )

        self.seat_combobox.bind(
            "<<ComboboxSelected>>",
            self.update_fare_summary
        )

        seat_information_label = ttk.Label(
            booking_frame,
            text=(
                "Window seats A and D: £15.00\n"
                "Standard seats B and C: £5.00"
            )
        )
        seat_information_label.grid(
            row=1,
            column=0,
            columnspan=2,
            sticky="w",
            pady=(5, 15)
        )

        self.fare_summary_label = ttk.Label(
            booking_frame,
            text="Select a seat to calculate the final fare.",
            justify="left"
        )
        self.fare_summary_label.grid(
            row=2,
            column=0,
            columnspan=2,
            sticky="w",
            pady=10
        )

        button_frame = ttk.Frame(main_frame)
        button_frame.pack(
            fill="x",
            pady=(15, 0)
        )

        back_button = ttk.Button(
            button_frame,
            text="Back to Search",
            command=self.show_flight_search_page
        )
        back_button.pack(side="left")

        continue_button = ttk.Button(
            button_frame,
            text="Review Booking",
            command=self.handle_booking_review
        )
        continue_button.pack(side="right")

        self.seat_combobox.focus()

    def update_fare_summary(self, event=None):
        """
        Recalculate and display the fare whenever a seat
        is selected.
        """

        selected_seat = self.seat_combobox.get()

        if selected_seat == "":
            self.fare_summary_label.configure(
                text="Select a seat to calculate the final fare."
            )
            return

        self.fare_details = calculate_total_fare(
            self.selected_flight,
            selected_seat
        )

        fare_text = (
            f"Base fare: £"
            f"{self.fare_details['base_price']:.2f}\n"

            f"Airport tax: £"
            f"{self.fare_details['airport_tax']:.2f}\n"

            f"Demand adjustment "
            f"({self.fare_details['demand_rate']}%): £"
            f"{self.fare_details['demand_adjustment']:.2f}\n"

            f"Seat charge: £"
            f"{self.fare_details['seat_charge']:.2f}\n"

            f"--------------------------------\n"

            f"Total price: £"
            f"{self.fare_details['total_price']:.2f}"
        )

        self.fare_summary_label.configure(
            text=fare_text
        )

    def handle_booking_review(self):
        """
        Validate the selected seat and display a temporary
        booking summary.
        """

        selected_seat = self.seat_combobox.get()

        if selected_seat == "":
            messagebox.showerror(
                "No Seat Selected",
                "Please select an available seat."
            )
            return

        current_flights = load_json_file(
            FLIGHTS_FILE
        )

        current_flight = None

        for flight in current_flights:
            if (
                flight.get("flight_id")
                == self.selected_flight.get("flight_id")
            ):
                current_flight = flight
                break

        if current_flight is None:
            messagebox.showerror(
                "Flight Error",
                "The selected flight no longer exists."
            )
            return

        if selected_seat not in current_flight.get(
            "available_seats",
            []
        ):
            messagebox.showerror(
                "Seat Unavailable",
                (
                    "The selected seat is no longer available. "
                    "Please choose another seat."
                )
            )

            self.selected_flight = current_flight
            self.show_booking_details_page()
            return

        self.selected_flight = current_flight

        self.fare_details = calculate_total_fare(
            current_flight,
            selected_seat
        )

        self.selected_seat = selected_seat

        summary = (
            f"Passenger: "
            f"{self.current_user['full_name']}\n"

            f"Flight: "
            f"{current_flight['flight_id']}\n"

            f"Airline: "
            f"{current_flight['airline']}\n"

            f"Route: "
            f"{current_flight['origin']} to "
            f"{current_flight['destination']}\n"

            f"Date: "
            f"{current_flight['departure_date']}\n"

            f"Seat: {selected_seat}\n"

            f"Total: £"
            f"{self.fare_details['total_price']:.2f}\n\n"

            "Booking confirmation and saving will be added "
            "in the next stage."
        )

        messagebox.showinfo(
            "Booking Summary",
            summary
        )

    # ======================================================
    # ADMINISTRATOR DASHBOARD
    # ======================================================

    def show_admin_dashboard(self):
        """
        Display a temporary administrator dashboard.
        """

        self.clear_window()

        main_frame = ttk.Frame(
            self.root,
            padding=40
        )
        main_frame.pack(
            fill="both",
            expand=True
        )

        title_label = ttk.Label(
            main_frame,
            text="Administrator Dashboard",
            style="Title.TLabel"
        )
        title_label.pack(pady=(40, 15))

        welcome_label = ttk.Label(
            main_frame,
            text=f"Welcome, {self.current_user['full_name']}",
            style="Subtitle.TLabel"
        )
        welcome_label.pack(pady=(0, 30))

        information_label = ttk.Label(
            main_frame,
            text="Administrator features will be added later."
        )
        information_label.pack(pady=20)

        logout_button = ttk.Button(
            main_frame,
            text="Log Out",
            command=self.logout
        )
        logout_button.pack(pady=20)

    # ======================================================
    # GENERAL GUI FUNCTIONS
    # ======================================================

    def show_feature_message(self, feature_name):
        """
        Display a temporary message for features that have
        not yet been implemented.
        """

        messagebox.showinfo(
            feature_name,
            f"The {feature_name} feature will be added next."
        )

    def logout(self):
        """
        Log out the current user and return to the login page.
        """

        self.current_user = None
        self.show_login_page()

# ==========================================================
# PROGRAM START
# ==========================================================

def main():
    """
    Prepare the files and start the graphical application.
    """

    create_data_files()
    create_sample_flights()

    root = tk.Tk()
    AirlineBookingApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
