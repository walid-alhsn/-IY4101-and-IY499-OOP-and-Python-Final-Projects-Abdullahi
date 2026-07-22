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

        for flight in matching_flights:
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

        messagebox.showinfo(
            "Flight Selected",
            (
                f"You selected {selected_flight['flight_id']} "
                f"with {selected_flight['airline']}.\n\n"
                "Passenger details and seat selection will "
                "be added in the next stage."
            )
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
